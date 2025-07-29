from __future__ import annotations

import time
from copy import deepcopy
from typing import Any, Optional, TypedDict

from typing_extensions import NotRequired

import dbnl.api
from dbnl.errors import DBNLDuplicateError, DBNLError, DBNLInputValidationError, DBNLResourceNotFoundError

from .core import handle_api_validation_error, validate_login
from .models import (
    AssertionDict,
    Project,
    TestSession,
    TestSpecDict,
)


@validate_login
def get_tests(*, test_session_id: str) -> list[dict[str, Any]]:
    """
    Get all Tests executed in the given Test Session

    :param test_session_id: Test Session ID

    :return: List of test JSONs

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in.

    #### Sample Test JSON

    .. code-block:: python

        {
            # Test metadata
            "id": string,
            "org_id": string,
            "created_at": timestamp,
            "updated_at": timestamp,
            "test_session_id": string,

            # Test data
            "author_id": string,
            "value": any?,
            "failure": string?,
            "status": enum(PENDING, RUNNING, PASSED, FAILED),
            "started_at": timestamp?,
            "completed_at": timestamp?,

            # Test Spec data
            "test_spec_id": id,
            "name": string,
            "description": string?,
            "statistic_name": string,
            "statistic_params": map[string, any],
            "assertion": {
                "name": string,
                "params": map[string, any]
                "status": enum(...),
                "failure": string?
            },
            "statistic_inputs": list[
                {
                "select_query_template": {
                    "select": string
                }
                }
            ],
            "tag_ids": string[]?,
            }

    """
    all_tests: list[dict[Any, Any]] = []
    tests = dbnl.api.get_tests(test_session_id=test_session_id)
    all_tests += tests["data"]
    total_count = tests["total_count"]

    while len(all_tests) < total_count:
        cur_offset = len(all_tests)
        tests = dbnl.api.get_tests(test_session_id=test_session_id, offset=cur_offset)
        all_tests += tests["data"]

    return all_tests


@validate_login
def get_test_sessions(*, project: Project) -> list[TestSession]:
    """
    Get all Test Sessions in the given Project

    :param project: Project from which to retrieve Test Sessions

    :return: List of Test Sessions

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in.
    """
    all_test_sessions: list[dict[Any, Any]] = []
    test_sessions = dbnl.api.get_test_sessions(project_id=project.id)
    all_test_sessions += test_sessions["data"]
    total_count = test_sessions["total_count"]

    while len(all_test_sessions) < total_count:
        cur_offset = len(all_test_sessions)
        test_sessions = dbnl.api.get_test_sessions(project_id=project.id, offset=cur_offset)
        all_test_sessions += test_sessions["data"]

    return [TestSession.from_dict(ts) for ts in all_test_sessions]


@validate_login
def wait_for_test_session(
    *,
    test_session: TestSession,
    timeout_s: int = 180,
) -> TestSession:
    """
    Wait for a Test Session to finish. Polls every 3 seconds until it is completed.

    :param test_session: The TestSession to wait for
    :param timeout_s: The total wait time (in seconds) for Test Session to complete, defaults to 180.

    :return: The completed TestSession

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in.
    :raises DBNLError: Test Session did not complete after waiting for the `timeout_s` seconds
    """
    start = time.time()
    while test_session.status not in ["PASSED", "FAILED"] and (time.time() - start) < timeout_s:
        test_session = TestSession.from_dict(dbnl.api.get_test_session(test_session_id=test_session.id))
        time.sleep(3)

    if test_session.status not in ["PASSED", "FAILED"]:
        raise DBNLError(f"Test Session {test_session} did not complete after waiting {timeout_s} seconds")

    return test_session


@validate_login
def create_test(*, test_spec_dict: TestSpecDict) -> dict[str, Any]:
    """
    Create a new Test Spec

    :param test_spec_dict: A dictionary containing the Test Spec schema.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in.
    :raises DBNLAPIValidationError: Test Spec does not conform to expected format.
    :raises DBNLDuplicateError: Test Spec with the same name already exists in the Project.

    :return: The JSON dict of the created Test Spec object. The return JSON will contain the id of the Test Spec.

    #### Test Spec JSON Structure

    .. code-block:: json

        {
            "project_id": string,

            # Test data
            "name": string, // must be unique to Project
            "description": string | null,
            "statistic_name": string,
            "statistic_params": map[string, any],
            "statistic_inputs": list[
                {
                    "select_query_template": {
                        "select": string, // a column or a function on column(s)
                        "filter": string | null
                    }
                }
            ],
            "assertion": {
                "name": string,
                "params": map[string, any]
            },
            "tag_ids": string[] | null
        }

    """
    with handle_api_validation_error():
        try:
            test_spec = dbnl.api.post_test_specs(test_spec_dict=dict(test_spec_dict))
        except DBNLDuplicateError:
            raise DBNLDuplicateError(
                f"Test with the name {test_spec_dict['name']} already exists in Project {test_spec_dict['project_id']}"
            )

    return test_spec


class IncompleteTestSpecDict(TypedDict, total=False):
    project_id: NotRequired[str]
    name: str
    statistic_name: str
    statistic_params: dict[str, float | int | str]
    statistic_inputs: list[dict[str, Any]]
    assertion: AssertionDict
    description: NotRequired[str]
    tag_names: NotRequired[list[str]]
    tag_ids: NotRequired[list[str]]


def prepare_incomplete_test_spec_payload(
    *,
    test_spec_dict: IncompleteTestSpecDict,
    project_id: Optional[str] = None,
) -> TestSpecDict:
    """
    Formats a Test Spec payload for the API. Add `project_id` if it is not present. Replace `tag_names` with `tag_ids`.

    :param test_spec_dict: A dictionary containing the Test Spec schema.
    :param project_id: The Project ID, defaults to None. If `project_id` does not exist in `test_spec_dict`, it is required as an argument.

    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: The dictionary containing the newly formatted Test Spec payload.

    """
    test_spec_dict = deepcopy(test_spec_dict)
    if "project_id" not in test_spec_dict:
        if project_id is None:
            raise DBNLInputValidationError("`project_id` is required in `test_spec_dict` or as an argument")
        test_spec_dict["project_id"] = project_id

    if "tag_ids" not in test_spec_dict and "tag_names" in test_spec_dict:
        tag_ids = []
        for tag_name in test_spec_dict["tag_names"]:
            tag = get_or_create_tag(project_id=test_spec_dict["project_id"], name=tag_name)
            tag_ids.append(tag["id"])
        test_spec_dict["tag_ids"] = tag_ids
        test_spec_dict.pop("tag_names")

    complete_test_spec = TestSpecDict(
        project_id=test_spec_dict["project_id"],
        name=test_spec_dict["name"],
        statistic_name=test_spec_dict["statistic_name"],
        statistic_params=test_spec_dict["statistic_params"],
        statistic_inputs=test_spec_dict["statistic_inputs"],
        assertion=test_spec_dict["assertion"],
    )
    if "description" in test_spec_dict:
        complete_test_spec["description"] = test_spec_dict["description"]
    if "tag_ids" in test_spec_dict:
        complete_test_spec["tag_ids"] = test_spec_dict["tag_ids"]
    return complete_test_spec


@validate_login
def get_or_create_tag(
    *,
    project_id: str,
    name: str,
    description: Optional[str] = None,
) -> dict[str, Any]:
    """
    Get the specified Test Tag or create a new one if it does not exist

    :param project_id: The id of the Project that this Test Tag is associated with.
    :param name: The name of the Test Tag to create or retrieve.
    :param description: An optional description of the Test Tag. Limited to 255 characters.

    :return: The dictionary containing the Test Tag

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in.

    #### Sample Test Tag JSON

    .. code-block:: python

        {
            # Tag metadata
            "id": string,
            "org_id": string,
            "created_at": timestamp,
            "updated_at": timestamp,

            # Tag data
            "name": string,
            "author_id": string,
            "description": string?,
            "project_id": string,
        }
    """
    try:
        tag_dict = dbnl.api.api_stubs.get_tag_by_name(project_id=project_id, name=name)
    except DBNLResourceNotFoundError:
        tag_dict = dbnl.api.api_stubs.post_tags(project_id=project_id, name=name, description=description)
    return tag_dict
