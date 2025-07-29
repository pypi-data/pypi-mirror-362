from __future__ import annotations

import json
import time
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from functools import wraps
from http import HTTPStatus
from io import BytesIO
from typing import Any, Callable, Optional, TypeVar, Union

import pandas as pd
from typing_extensions import ParamSpec

from dbnl import api
from dbnl.config import CONFIG
from dbnl.errors import (
    DBNLAPIError,
    DBNLAPIValidationError,
    DBNLConflictingProjectError,
    DBNLDuplicateError,
    DBNLError,
    DBNLInputValidationError,
    DBNLNotLoggedInError,
    DBNLProjectNotFoundError,
    DBNLResourceNotFoundError,
    DBNLRunError,
    DBNLRunNotFoundError,
    DBNLRunQueryNotFoundError,
    DBNLTagNotFoundError,
)
from dbnl.print_logging import dbnl_logger

from .models import (
    Metric,
    Project,
    ResultData,
    Run,
    RunQuery,
    RunSchema,
    RunSchemaColumnSchema,
    RunSchemaColumnSchemaDict,
    RunSchemaScalarSchema,
    RunSchemaScalarSchemaDict,
    TestSession,
    TestSessionInput,
)
from .util import (
    get_column_schemas_from_dataframe,
    get_scalar_schemas_from_dataframe,
    make_test_session_input,
)
from .validate import (
    validate_column_data,
    validate_project,
    validate_run,
    validate_run_id,
    validate_run_schema_for_creation,
    validate_scalar_data,
    validate_tags,
    validate_test_session_inputs,
)

T = TypeVar("T")
P = ParamSpec("P")


@contextmanager
def handle_api_validation_error() -> Iterator[None]:
    """
    Context manager to handle API validation errors
    """
    try:
        yield
    except DBNLAPIError as e:
        if e.status_code == HTTPStatus.BAD_REQUEST:
            resp_data = json.loads(e.response.text)
            if not isinstance(resp_data, dict):
                raise
            if resp_data.get("code") != "invalid_data":
                raise
            message = resp_data.get("message")
            if not isinstance(message, dict):
                raise
            error_info = message.get("json")
            if not isinstance(error_info, dict):
                raise
            raise DBNLAPIValidationError(error_info)
        raise


def login(
    *,
    api_token: Optional[str] = None,
    namespace_id: Optional[str] = None,
    api_url: Optional[str] = None,
    app_url: Optional[str] = None,
) -> None:
    """
    Setup dbnl SDK to make authenticated requests. After login is run successfully, the dbnl client
    will be able to issue secure and authenticated requests against hosted endpoints of the dbnl service.


    :param api_token: dbnl API token for authentication; token can be found at /tokens page of the dbnl app.
        If None is provided, the environment variable `DBNL_API_TOKEN` will be used by default.
    :param namespace_id: The namespace ID to use for the session; available namespaces can be found with `get_my_namespaces()`.
    :param api_url: The base url of the Distributional API. For SaaS users, set this variable to api.dbnl.com.
        For other users, please contact your sys admin. If None is provided, the environment variable `DBNL_API_URL` will be used by default.
    :param app_url: An optional base url of the Distributional app. If this variable is not set, the app url is inferred from the DBNL_API_URL
        variable. For on-prem users, please contact your sys admin if you cannot reach the Distributional UI.
    """
    CONFIG.clear_mutable_config()
    if api_url:
        CONFIG.dbnl_api_url = api_url

    if app_url:
        CONFIG.dbnl_app_url = app_url

    if api_token:
        CONFIG.dbnl_api_token = api_token

    api._ensure_valid_token()
    api._maybe_warn_invalid_version()

    if namespace_id:
        CONFIG.dbnl_namespace_id = namespace_id
        api._ensure_valid_namespace()
    else:
        CONFIG.dbnl_namespace_id = api.get_default_namespace()["id"]

    # set config that login() was successful
    CONFIG.dbnl_logged_in = True


def validate_login(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator to validate that the user has logged in before making a request
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        if not CONFIG.dbnl_logged_in:
            raise DBNLNotLoggedInError()
        return func(*args, **kwargs)

    return wrapper


@validate_login
def get_project(
    *,
    name: str,
) -> Project:
    """
    Retrieve a Project by name.

    :param name: The name for the existing Project.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLProjectNotFoundError: Project with the given name does not exist.

    :return: Project

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj_1 = dbnl.create_project(name="test_p1")
        proj_2 = dbnl.get_project(name="test_p1")

        # Calling get_project will yield same Project object
        assert proj_1.id == proj_2.id

        # DBNLProjectNotFoundError: A dnnl Project with name not_exist does not exist
        proj_3 = dbnl.get_project(name="not_exist")
    """
    try:
        resp_dict = api.get_project_by_name(name=name)
    except DBNLResourceNotFoundError:
        raise DBNLProjectNotFoundError(name)

    return Project.from_dict(resp_dict)


@validate_login
def create_project(
    *,
    name: str,
    description: Optional[str] = None,
) -> Project:
    """
    Create a new Project

    :param name: Name for the Project
    :param description: Description for the Project, defaults to None. Description is limited to 255 characters.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLAPIValidationError: dbnl API failed to validate the request
    :raises DBNLConflictingProjectError: Project with the same name already exists

    :return: Project

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj_1 = dbnl.create_project(name="test_p1")

        # DBNLConflictingProjectError: A Project with name test_p1 already exists.
        proj_2 = dbnl.create_project(name="test_p1")
    """
    try:
        with handle_api_validation_error():
            resp_dict = api.post_projects(name=name, description=description)
    except DBNLDuplicateError:
        raise DBNLConflictingProjectError(name)

    namespace_param = f"ns/{CONFIG.dbnl_namespace_id}/" if CONFIG.dbnl_namespace_id else ""
    dbnl_logger.info(
        "View Project %s at: %s%sprojects/%s",
        name,
        CONFIG.dbnl_app_url,
        namespace_param,
        resp_dict["id"],
    )
    return Project.from_dict(resp_dict)


@validate_login
def get_or_create_project(
    *,
    name: str,
    description: Optional[str] = None,
) -> Project:
    """
    Get the Project with the specified name or create a new one if it does not exist

    :param name: Name for the Project
    :param description: Description for the Project, defaults to None

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLAPIValidationError: dbnl API failed to validate the request

    :return: Newly created or matching existing Project

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj_1 = dbnl.create_project(name="test_p1")
        proj_2 = dbnl.get_or_create_project(name="test_p1")

        # Calling get_or_create_project will yield same Project object
        assert proj_1.id == proj_2.id
    """

    try:
        return get_project(name=name)
    except DBNLProjectNotFoundError:
        try:
            return create_project(name=name, description=description)
        except DBNLConflictingProjectError:
            return get_project(name=name)


@validate_login
def export_project_as_json(
    *,
    project: Project,
) -> dict[str, Any]:
    """
    Export a Project alongside its Test Specs, Tags, and Notification Rules as a JSON object

    :param project: The Project to export as JSON.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in

    :return: JSON object representing the Project

    #### Sample Project JSON

    .. code-block:: python

        {
            "project": {
                "name": "My Project",
                "description": "This is my project."
            },
            "notification_rules": [
                {
                    "conditions": [
                        {
                            "assertion_name": "less_than",
                            "assertion_params": { "other": 0.85 },
                            "query_name": "test_status_percentage_query",
                            "query_params": {
                                "exclude_tag_ids": [],
                                "include_tag_ids": [],
                                "require_tag_ids": [],
                                "statuses": ["PASSED"]
                            }
                        }
                    ],
                    "name": "Alert if passed tests are less than 85%",
                    "notification_integration_names": ["Notification channel"],
                    "status": "ENABLED",
                    "trigger": "test_session.failed"
                }
            ],
            "tags": [
                {
                    "name": "my-tag",
                    "description" :"This is my tag."
                }
            ],
            "test_specs": [
                {
                    "assertion": { "name": "less_than", "params": { "other": 0.5 } },
                    "description": "Testing the difference in the example statistic",
                    "name": "Gr.0: Non Parametric Difference: Example_Statistic",
                    "statistic_inputs": [
                        {
                            "select_query_template": {
                                "filter": null,
                                "select": "{EXPERIMENT}.Example_Statistic"
                            }
                        },
                        {
                            "select_query_template": {
                                "filter": null,
                                "select": "{BASELINE}.Example_Statistic"
                            }
                        }
                    ],
                    "statistic_name": "my_stat",
                    "statistic_params": {},
                    "tag_names": ["my-tag"]
                }
            ]
        }

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj = dbnl.get_or_create_project(name="test_proj")
        export_json = dbnl.export_project_as_json(project=proj)

        assert export_json["project"]["name"] == "test_proj"
    """
    try:
        return api.get_project_export(project_id=project.id)
    except DBNLResourceNotFoundError:
        raise DBNLProjectNotFoundError(project.name)


@validate_login
def import_project_from_json(
    *,
    params: dict[str, Any],
) -> Project:
    """
    Create a new Project from a JSON object

    :param params: JSON object representing the Project, generally based on a Project exported via
                     `export_project_as_json()`. See `export_project_as_json()` for the expected format.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLAPIValidationError: dbnl API failed to validate the request
    :raises DBNLConflictingProjectError: Project with the same name already exists

    :return: Project created from the JSON object

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_proj1")
        export_json = dbnl.export_project_as_json(project=proj1)
        export_json["project"]["name"] = "test_proj2"
        proj2 = dbnl.import_project_from_json(params=export_json)

        assert proj2.name == "test_proj2"
    """
    if not params.get("project"):
        raise DBNLInputValidationError("`project` is required in params")
    if not params["project"].get("name"):
        raise DBNLInputValidationError("`project.name` is required in params")

    try:
        with handle_api_validation_error():
            resp_dict = api.post_project_import(params=params)
    except DBNLDuplicateError:
        raise DBNLConflictingProjectError(params["project"]["name"])

    project = Project.from_dict(resp_dict)

    namespace_param = f"ns/{CONFIG.dbnl_namespace_id}/" if CONFIG.dbnl_namespace_id else ""
    dbnl_logger.info(
        "View Project %s at: %s%sprojects/%s",
        project.name,
        CONFIG.dbnl_app_url,
        namespace_param,
        resp_dict["id"],
    )

    return project


@validate_login
def copy_project(
    *,
    project: Project,
    name: str,
    description: Optional[str] = None,
) -> Project:
    """
    Copy a Project; a convenience method wrapping exporting and importing a project with a new name and description

    :param project: The project to copy
    :param name: A name for the new Project
    :param description: An optional description for the new Project. Description is limited to 255 characters.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    :raises DBNLConflictingProjectError: Project with the same name already exists

    :return: The newly created Project

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_proj1")
        proj2 = dbnl.copy_project(project=proj1, name="test_proj2")

        assert proj2.name == "test_proj2"
    """
    if name == project.name:
        raise DBNLInputValidationError("New project name must be different from the original project name")

    params = export_project_as_json(project=project)
    params["project"]["name"] = name
    params["project"]["description"] = description
    return import_project_from_json(params=params)


@validate_login
def create_run(
    *,
    project: Project,
    run_schema: RunSchema,
    display_name: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> Run:
    """
    Create a new Run

    :param project: The Project this Run is associated with.
    :param run_schema: The schema for data that will be associated with this run. dbnl will validate data
        you upload against this schema.
    :param display_name: An optional display name for the Run, defaults to None. `display_name` does not have to be unique.
    :param metadata: Additional key-value pairs you want to track, defaults to None.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Newly created Run
    """

    try:
        validate_project(project)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    assert run_schema is not None
    try:
        validate_run_schema_for_creation(run_schema)
        with handle_api_validation_error():
            resp_dict = api.post_runs(
                project_id=project.id,
                run_schema=run_schema.to_dict(encode_json=True),
                display_name=display_name,
                metadata=metadata,
            )
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    return Run.from_dict(resp_dict)


@validate_login
def report_column_results(
    *,
    run: Run,
    data: pd.DataFrame,
) -> None:
    """
    Report all column results to dbnl

    :param run: The Run that the results will be reported to
    :param data: A pandas DataFrame with all the results to report to dbnl.
        The columns of the DataFrame must match the columns of the Run's schema.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    .. important::

        All data should be reported to dbnl at once. Calling `dbnl.report_column_results` more than once will overwrite the previously uploaded data.

    .. warning::

        Once a Run is closed, you can no longer call `report_column_results` to send data to dbnl.

    #### Examples:

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_p1")
        schema1 = dbnl.create_run_schema(columns=[{"name": "error", "type": "float"}])
        run1 = dbnl.create_run(project=proj1, run_schema=schema1)

        data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})
        dbnl.report_column_results(run=run1, data=data)

    """
    try:
        validate_run(run)
        validate_column_data(data, run.run_schema.columns, run.run_schema.index)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    api.post_results(run_id=run.id, data=data, scalar=False)


@validate_login
def report_scalar_results(
    *,
    run: Run,
    data: Union[dict[str, Any], pd.DataFrame],
) -> None:
    """
    Report scalar results to dbnl

    :param run: The Run that the scalars will be reported to
    :param data: A dictionary or single-row pandas DataFrame with the scalar results to report to dbnl.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    .. important::

        All data should be reported to dbnl at once. Calling `dbnl.report_scalar_results` more than once will overwrite the previously uploaded data.

    .. warning::

        Once a Run is closed, you can no longer call `report_scalar_results` to send data to dbnl.

    #### Examples:

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_p1")
        schema1 = dbnl.create_run_schema(
            columns=[{"name": "error", "type": "float"}],
            scalars=[{"name": "rmse": "type": "float"}],
        )
        run1 = dbnl.create_run(project=proj1, run_schema=schema1)
        dbnl.report_scalar_results(run=run1, data={"rmse": 0.37})
    """
    if isinstance(data, dict):
        data = pd.DataFrame([data])

    try:
        validate_run(run)
        scalar_defs = run.run_schema.scalars

        if scalar_defs:
            for scalar_schema in scalar_defs:
                if scalar_schema.type == "category":
                    data[scalar_schema.name] = data[scalar_schema.name].astype("category")
            validate_scalar_data(data, scalar_defs)
        elif data.empty:
            return  # if this is part of an automated workflow it would be better not to fail here
        else:
            raise DBNLInputValidationError("No scalars expected in run schema")
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    api.post_results(run_id=run.id, data=data, scalar=True)


@validate_login
def report_results(
    *,
    run: Run,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
) -> None:
    """
    Report all results to dbnl

    :param run: The Run that the results will be reported to
    :param column_data: A pandas DataFrame with all the results to report to dbnl.
        The columns of the DataFrame must match the columns of the Run's schema.
    :param scalar_data: A dictionary or single-row pandas DataFrame with the scalar results to report to dbnl, defaults to None.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    .. important::

        All data should be reported to dbnl at once. Calling `dbnl.report_results` more than once will overwrite the previously uploaded data.

    .. warning::

        Once a Run is closed, you can no longer call `report_results` to send data to dbnl.

    #### Examples:

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_p1")
        schema1 = dbnl.create_run_schema(
            columns=[{"name": "error", "type": "float"}],
            scalars=[{"name": "rmse": "type": "float"}],
        )
        run1 = dbnl.create_run(project=proj1, run_schema=schema1)
        data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})
        dbnl.report_results(run=run1, column_data=data, scalar_data={"rmse": 0.37})
    """
    report_column_results(run=run, data=column_data)
    if scalar_data is not None:
        report_scalar_results(run=run, data=scalar_data)


@validate_login
def get_column_results(
    *,
    run: Run,
) -> pd.DataFrame:
    """
    Get column results for a Run

    :param run: The Run from which to retrieve the results.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    :raises DBNLDownloadResultsError: Failed to download results (e.g. Run is not closed)

    :return: A pandas DataFrame of the column results for the Run.

    .. important::

        You can only retrieve results for a Run that has been closed.

    #### Examples:

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj = dbnl.get_or_create_project(name="test_p1")
        uploaded_data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})
        run = dbnl.report_run_with_results(
            project=proj,
            column_results=test_data,
        )

        downloaded_data = dbnl.get_column_results(run=run)
        assert downloaded_data.equals(uploaded_data)
    """

    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    content = api.get_results(run_id=run.id, scalar=False)
    return pd.read_parquet(BytesIO(content), engine="pyarrow", dtype_backend="pyarrow")


@validate_login
def get_scalar_results(
    *,
    run: Run,
) -> pd.DataFrame:
    """
    Get scalar results for a Run

    :param run: The Run from which to retrieve the scalar results.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    :raises DBNLDownloadResultsError: Failed to download results (e.g. Run is not closed)

    :return: A pandas DataFrame of the scalar results for the Run.


    .. important::

        You can only retrieve results for a Run that has been closed.

    #### Examples:

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()

        proj1 = dbnl.get_or_create_project(name="test_p1")

        data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})
        run = dbnl.report_run_with_results(
            project=proj,
            column_results=data,
            scalar_results={"rmse": 0.37}
        )

        downloaded_scalars = dbnl.get_scalar_results(run=run)

    """

    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    content = api.get_results(run_id=run.id, scalar=True)
    return pd.read_parquet(BytesIO(content), engine="pyarrow", dtype_backend="pyarrow")


@validate_login
def get_results(
    *,
    run: Run,
) -> ResultData:
    """
    Get all results for a Run

    :param run: The Run from which to retrieve the results.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    :raises DBNLDownloadResultsError: Failed to download results (e.g. Run is not closed)

    :return: A named tuple comprised of `columns` and `scalars` fields. These
        are the pandas DataFrames of the uploaded data for the Run.

    .. important::

        You can only retrieve results for a Run that has been closed.

    #### Examples:

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj = dbnl.get_or_create_project(name="test_p1")

        uploaded_data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})
        run = dbnl.report_run_with_results(
            project=proj,
            column_results=uploaded_data,
        )

        downloaded_data = dbnl.get_results(run=run)
        assert downloaded_data.columns.equals(uploaded_data)
    """
    columns = get_column_results(run=run)
    scalar_defs = run.run_schema.scalars

    scalars = get_scalar_results(run=run) if scalar_defs else None
    return ResultData(columns=columns, scalars=scalars)


@validate_login
def get_run(
    *,
    run_id: str,
) -> Run:
    """
    Retrieve a Run with the given ID

    :param run_id: The ID of the dbnl Run. Run ID starts with the prefix `run_`. Run ID can be
        found at the Run detail page.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    :raises DBNLRunNotFoundError: A Run with the given ID does not exist.

    :return: The Run with the given run_id.

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_p1")
        schema1 = dbnl.create_run_schema(project=proj1, columns=[{"name": "error", "type": "float"}])
        run1 = dbnl.create_run(project=proj1, run_schema=schema1)

        # Retrieving the Run by ID
        run2 = dbnl.get_run(run_id=run1.id)
        assert run1.id == run2.id

        # DBNLRunNotFoundError: A Run with id run_0000000 does not exist.
        run3 = dbnl.get_run(run_id="run_0000000")
    """

    try:
        validate_run_id(run_id)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    try:
        resp_dict = api.get_run_by_id(run_id=run_id)
    except DBNLResourceNotFoundError:
        raise DBNLRunNotFoundError(run_id)

    return Run.from_dict(resp_dict)


def _get_tag_id(
    *,
    project_id: str,
    name: str,
) -> str:
    """
    Retrieve a Tag ID by name

    :param project_id: The ID of the Project to search for the Tag
    :param name: The unique name for the Test Tag.

    :return: Tag ID
    """
    try:
        tag = api.api_stubs.get_tag_by_name(project_id=project_id, name=name)
    except DBNLResourceNotFoundError:
        raise DBNLTagNotFoundError(tag_name=name, project_id=project_id)

    return str(tag["id"])


def _get_tag_ids(
    *,
    project_id: str,
    names: Optional[list[str]] = None,
) -> Optional[list[str]]:
    """
    Retrieve a list of Tag IDs by name

    :param project_id: The ID of the Project to search for the Tag
    :param names: List of names for the Test Tags. Names for Tags must be unique.

    :return: List of Tag IDs
    """
    if not names:
        return None
    return [_get_tag_id(project_id=project_id, name=tag_name) for tag_name in names]


@validate_login
def close_run(
    *,
    run: Run,
    wait_for_close: bool = True,
) -> None:
    """
    Mark the specified dbnl Run status as closed. A closed run is finalized and considered complete.
    Once a Run is marked as closed, it can no longer be used for reporting Results.

    Note that the Run will not be closed immediately. It will transition into a closing state
    and will be closed in the background. If `wait_for_close` is set to True, the function will
    block for up to 3 minutes until the Run is closed.

    :param run: The Run to be closed
    :param wait_for_close: If True, the function will block for up to 3 minutes until the Run is closed, defaults to True

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    :raises DBNLError: Run did not close after waiting for 3 minutes

    .. important::

        A run must be closed for uploaded results to be shown on the UI.
    """

    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    api.post_runs_close(run_id=run.id)
    namespace_param = f"ns/{CONFIG.dbnl_namespace_id}/" if CONFIG.dbnl_namespace_id else ""
    dbnl_logger.info(
        "Initiated run close. View results at: %s%sprojects/%s/runs/%s",
        CONFIG.dbnl_app_url,
        namespace_param,
        run.project_id,
        run.id,
    )

    if wait_for_close:
        dbnl_logger.info("Waiting for run to close...")
        run = wait_for_run_close(run=run)
        dbnl_logger.info("Run closed successfully")
    else:
        dbnl_logger.info("Run should close shortly")


@validate_login
def get_my_namespaces() -> list[Any]:
    """
    Get all the namespaces that the user has access to

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in

    :return: List of namespaces
    """
    return api.get_my_namespaces()


@validate_login
def get_latest_run(*, project: Project) -> Run:
    """
    Get the latest Run for a project

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLResourceNotFoundError: Run not found

    :param project: The Project to get the latest Run for
    :return: The latest Run
    """
    try:
        resp_dict = api.get_latest_run(project_id=project.id)
    except DBNLResourceNotFoundError:
        raise DBNLRunNotFoundError("latest")

    return Run.from_dict(resp_dict)


def create_run_schema(
    *,
    columns: Sequence[RunSchemaColumnSchemaDict],
    scalars: Optional[Sequence[RunSchemaScalarSchemaDict]] = None,
    index: Optional[list[str]] = None,
    components_dag: Optional[dict[str, list[str]]] = None,
) -> RunSchema:
    """
    Create a new RunSchema

    :param columns: List of column schema specs for the uploaded data, required keys `name` and `type`,
        optional keys `component`, `description` and `greater_is_better`.
    :param scalars: List of scalar schema specs for the uploaded data, required keys `name` and `type`,
        optional keys `component`, `description` and `greater_is_better`.
    :param index: Optional list of column names that are the unique identifier.
    :param components_dag: Optional dictionary representing the DAG of components.

    :return: The RunSchema

    #### Supported Types
    - `int`
    - `float`
    - `boolean`
    - `string`
    - `category`
    - `list`

    #### Components
    The optional component key is for specifying the source of the data column in relationship to
    the AI/ML app subcomponents. Components are used in visualizing the components DAG.

    The components_dag dictionary specifies the topological layout of the AI/ML app. For each key-value
    pair, the key represents the source component, and the value is a list of the leaf components.
    The following code snippet describes the DAG shown above.

    .. code-block:: python

        components_dags={
            "TweetSource": ["EntityExtractor", "SentimentClassifier"],
            "EntityExtractor": ["TradeRecommender"],
            "SentimentClassifier": ["TradeRecommender"],
            "TradeRecommender": [],
            "Global": [],
        }

    #### Examples:

    **Basic**

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj = dbnl.get_or_create_project(name="test_p1")
        schema = dbnl.create_run_schema(
            project=proj,
            columns=[
                {"name": "error_type", "type": "category"},
                {"name": "email", "type": "string", "description": "raw email text content from source"},
                {"name": "spam-pred", "type": "boolean"},
            ],
        )

    **With `scalars`, `index`, and `components_dag`**

    .. code-block:: python

        import dbnl
        dbnl.login()

        proj = dbnl.get_or_create_project(name="test_p1")
        schema = dbnl.create_run_schema(
            columns=[
                {"name": "error_type", "type": "category", "component": "classifier"},
                {"name": "email", "type": "string", "description": "raw email text content from source", "component": "input"},
                {"name": "spam-pred", "type": "boolean", "component": "classifier"},
                {"name": "email_id", "type": "string", "description": "unique id for each email"},
            ],
            scalars=[
                {"name": "model_F1", "type": "float"},
                {"name": "model_recall", "type": "float"},
            ],
            index=["email_id"],
            components_dag={
                "input": ["classifier"],
                "classifier": [],
            },
        )

    """
    cols = []
    for col in columns:
        cols.append(RunSchemaColumnSchema.from_dict(col))

    scals = None
    if scalars:
        scals = []
        for scalar in scalars:
            scals.append(RunSchemaScalarSchema.from_dict(scalar))

    return RunSchema(columns=cols, scalars=scals, index=index, components_dag=components_dag)


def create_run_schema_from_results(
    *,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    index: Optional[list[str]] = None,
) -> RunSchema:
    """
    Create a new RunSchema from the column results, as well as scalar results if provided

    :param column_data: A pandas DataFrame with all the column results for which we want
        to generate a RunSchema.
    :param scalar_data: A dict or pandas DataFrame with all the scalar results for which
        we want to generate a RunSchema.
    :param index: An optional list of the column names that can be used as unique identifiers.

    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: The RunSchema based on the provided results

    #### Examples:

    .. code-block:: python

        import dbnl
        impodt pandas as pd

        dbnl.login()

        column_data = pd.DataFrame({
            "id": [1, 2, 3],
            "question": [
                "What is the meaning of life?",
                "What is the airspeed velocity of an unladen swallow?",
                "What is the capital of Assyria?",
            ],
        })
        scalar_data = {"int_scalar": 42, "string_scalar": "foobar"}

        run_schema = dbnl.create_run_schema_from_results(
            column_data=column_data,
            scalar_data=scalar_data,
            index=["id"],
        )
    """
    try:
        columns = get_column_schemas_from_dataframe(column_data)
        if isinstance(scalar_data, dict):
            scalar_data = pd.DataFrame([scalar_data])
        scalars = get_scalar_schemas_from_dataframe(scalar_data) if scalar_data is not None else None
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    return create_run_schema(columns=columns, scalars=scalars, index=index, components_dag=None)


@validate_login
def report_run_with_results(
    *,
    project: Project,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    display_name: Optional[str] = None,
    index: Optional[list[str]] = None,
    run_schema: Optional[RunSchema] = None,
    metadata: Optional[dict[str, str]] = None,
    wait_for_close: bool = True,
) -> Run:
    """
    Create a new Run, report results to it, and close it.

    :param project: The Project to create the Run in.
    :param column_data: A pandas DataFrame with the results for the columns.
    :param scalar_data: An optional dictionary or DataFrame with the results for the scalars, if any.
    :param display_name: An optional display name for the Run.
    :param index: An optional list of column names to use as the unique identifier for rows in the column data.
    :param run_schema: An optional RunSchema to use for the Run. Will be inferred from the data if not provided.
    :param metadata: Any additional key:value pairs you want to track.
    :param wait_for_close: If True, the function will block for up to 3 minutes until the Run is closed, defaults to True.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: The closed Run with the uploaded data.

    .. important::

        If no schema is provided, the schema will be inferred from the data. If provided,
        the schema will be used to validate the data.

    #### Examples:

    **Implicit Schema**

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj = dbnl.get_or_create_project(name="test_p1")
        test_data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})

        run = dbnl.report_run_with_results(
            project=proj,
            column_data=test_data,
        )

    **Explicit Schema**

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj = dbnl.get_or_create_project(name="test_p1")
        test_data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})
        run_schema = dbnl.create_run_schema(columns=[
        {"name": "error", "type": "float"}
        ])

        run = dbnl.report_run_with_results(
            project=proj,
            column_data=test_data,
            run_schema=run_schema
        )

        try:
        run_schema = dbnl.create_run_schema(columns=[
            {"name": "error", "type": "string"}
        ])
        dbnl.report_run_with_results(
            project=proj,
            column_data=test_data,
            run_schema=run_schema
        )
        except DBNLInputValidationError:
        # We expect DBNLInputValidationError because the type of
        # `error` in the input data is "float", but we provided a `RunSchema`
        # which specifies the columm type as "string".
        assert True
        else:
        # should not get here
        assert False
    """

    if run_schema is None:
        run_schema = create_run_schema_from_results(column_data=column_data, scalar_data=scalar_data, index=index)
    validate_column_data(column_data, run_schema.columns, run_schema.index)
    if scalar_data is not None:
        if isinstance(scalar_data, dict):
            scalar_data = pd.DataFrame([scalar_data])
        validate_scalar_data(scalar_data, run_schema.scalars)

    run = create_run(project=project, run_schema=run_schema, display_name=display_name, metadata=metadata)

    # We don't need to validate the data again, as we've already done so above
    # So we can directly post the results
    api.post_results(run_id=run.id, data=column_data, scalar=False)
    if scalar_data is not None:
        api.post_results(run_id=run.id, data=scalar_data, scalar=True)

    close_run(run=run, wait_for_close=wait_for_close)
    return run


def _validate_run_query_query(query: dict[str, Any]) -> None:
    # currently, only 1 query is supported; we can iterate on how to support different queries in the future
    if (
        not isinstance(query, dict)
        or len(query) != 1
        or "offset_from_now" not in query
        or not isinstance(query["offset_from_now"], int)
        or query["offset_from_now"] < 1
    ):
        raise DBNLInputValidationError(
            "Query must be a dictionary, containing only 'offset_from_now' key with a positive integer value"
        )


@validate_login
def create_run_query(
    *,
    project: Project,
    name: str,
    query: dict[str, Any],
) -> RunQuery:
    """
    Create a new RunQuery for a project to use as a baseline Run.
    Currently supports key="offset_from_now" with value as a positive integer, representing
    the number of runs to go back for the baseline. For example, query={"offset_from_now": 1} will
    use the latest run as the baseline, so that each run compares against the previous run.

    :param project: The Project to create the RunQuery for
    :param name: A name for the RunQuery
    :param query: A dict describing how to find a Run dynamically. Currently, only supports
        `"offset_from_now": int` as a key-value pair.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return:  A new dbnl RunQuery, typically used for finding a Dynamic Baseline for a Test Session

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_p1")
        run_query1 = dbnl.create_run_query(
            project=project,
            name="look back 3",
            query={
                "offset_from_now": 3,
            },
        )
    """
    try:
        validate_project(project)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))
    _validate_run_query_query(query)

    with handle_api_validation_error():
        resp_dict = api.post_run_query(project_id=project.id, name=name, query=query)
    return RunQuery.from_dict(resp_dict)


@validate_login
def get_run_query(
    *,
    project: Project,
    name: str,
) -> RunQuery:
    """
    Retrieve a RunQuery with the given name, unique to a project

    :param project: The Project from which to retrieve the RunQuery.
    :param name: The name of the RunQuery to retrieve.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLRessourceNotFoundError: RunQuery not found

    :return: RunQuery with the given name.

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()


        proj1 = dbnl.get_or_create_project(name="test_p1")
        run_query1 = dbnl.get_run_query(
            project=project,
            name="look back 3"
        )
    """
    try:
        resp_dict = api.get_run_query_by_name(project_id=project.id, name=name)
    except DBNLResourceNotFoundError:
        raise DBNLRunQueryNotFoundError(name)

    return RunQuery.from_dict(resp_dict)


@validate_login
def set_run_as_baseline(
    *,
    run: Run,
) -> None:
    """
    Set the given Run as the Baseline Run in the Project's Test Config

    :param run: The Run to set as the Baseline Run.

    :raises DBNLResourceNotFoundError: If the test configurations are not found for the project.
    """
    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))
    try:
        test_config_dict = api.get_test_configs(project_id=run.project_id)
    except DBNLResourceNotFoundError:
        raise DBNLResourceNotFoundError(f"Test Configs not found for Project {run.project_id}")

    test_config_id = test_config_dict["id"]
    api.patch_test_configs(test_config_id=test_config_id, baseline_run_id=run.id)


@validate_login
def set_run_query_as_baseline(
    *,
    run_query: RunQuery,
) -> None:
    """
    Set a given RunQuery as the Baseline Run in a Project's Test Config

    :param run_query: The RunQuery to set as the Baseline RunQuery.

    :raises DBNLResourceNotFoundError: If the test configurations are not found for the project.
    """
    try:
        test_config_dict = api.get_test_configs(project_id=run_query.project_id)
    except DBNLResourceNotFoundError:
        raise DBNLResourceNotFoundError(f"Test Configs not found for Project {run_query.project_id}")

    test_config_id = test_config_dict["id"]
    api.patch_test_configs(test_config_id=test_config_id, baseline_run_query_id=run_query.id)


@validate_login
def _get_default_baseline_input(project_id: str) -> TestSessionInput:
    test_config = api.get_test_configs(project_id=project_id)
    if test_config["baseline_type"] == "RUN_ID":
        return TestSessionInput(
            run_alias="BASELINE",
            run_id=test_config["baseline_run_id"],
        )
    if test_config["baseline_type"] == "RUN_QUERY":
        return TestSessionInput(
            run_alias="BASELINE",
            run_query_id=test_config["baseline_run_query_id"],
        )
    raise ValueError(f"No baseline input found in test config: {test_config}.")


@validate_login
def create_test_session(
    *,
    experiment_run: Run,
    baseline: Optional[Union[Run, RunQuery]] = None,
    include_tags: Optional[list[str]] = None,
    exclude_tags: Optional[list[str]] = None,
    require_tags: Optional[list[str]] = None,
) -> TestSession:
    """
    Create a new TestSession with the given Run as the Experiment Run, and the given Run or RunQuery as the baseline if provided

    :param experiment_run: The Run to create the TestSession for
    :param baseline: The Run or RunQuery to use as the Baseline Run, defaults to None. If None, the Baseline set for the Project is used.
    :param include_tags: Optional list of Test Tag names to include in the Test Session.
    :param exclude_tags: Optional list of Test Tag names to exclude in the Test Session.
    :param require_tags: Optional list of Test Tag names to require in the Test Session.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: The newly created TestSession

    Calling this will start evaluating Tests associated with a Run. Typically, the Run you just completed will be the "Experiment"
    and you'll compare it to some earlier "Baseline Run".

    .. important::

        Referenced Runs must already be closed before a Test Session can begin.

    #### Managing Tags

    Suppose we have the following Tests with the associated Tags in our Project
    - Test1 with tags ["A", "B"]
    - Test2 with tags ["A"]
    - Test3 with tags ["B"]

    `include_tags=["A", "B"]` will trigger Tests 1, 2, and 3.
    `require_tags=["A", "B"]` will only trigger Test 1.
    `exclude_tags=["A"]` will only trigger Test 3.
    `include_tags=["A"]` and `exclude_tags=["B"]` will only trigger Test 2.

    #### Examples:

    .. code-block:: python

        import dbnl
        dbnl.login()

        run = dbnl.get_run(run_id="run_0000000")
        # Will default baseline to the Project's Baseline
        dbnl.create_test_session(
            experiment_run=run,
        )

    """
    test_session_inputs = [make_test_session_input(run=experiment_run)]
    if isinstance(baseline, Run):
        baseline_input = make_test_session_input(run=baseline, run_alias="BASELINE")
        test_session_inputs.append(baseline_input)
    elif isinstance(baseline, RunQuery):
        baseline_input = make_test_session_input(run_query=baseline, run_alias="BASELINE")
        test_session_inputs.append(baseline_input)
    else:
        baseline_input = _get_default_baseline_input(project_id=experiment_run.project_id)
        test_session_inputs.append(baseline_input)

    try:
        validate_tags(include_tags, exclude_tags, require_tags)
        validate_test_session_inputs(test_session_inputs)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    include_tag_ids = _get_tag_ids(project_id=experiment_run.project_id, names=include_tags)
    exclude_tag_ids = _get_tag_ids(project_id=experiment_run.project_id, names=exclude_tags)
    require_tag_ids = _get_tag_ids(project_id=experiment_run.project_id, names=require_tags)

    with handle_api_validation_error():
        resp_dict = api.post_test_session(
            project_id=experiment_run.project_id,
            inputs=[input_.to_dict() for input_ in test_session_inputs],
            include_tag_ids=include_tag_ids,
            exclude_tag_ids=exclude_tag_ids,
            require_tag_ids=require_tag_ids,
        )
    return TestSession.from_dict(resp_dict)


@validate_login
def report_run_with_results_and_start_test_session(
    *,
    project: Project,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    display_name: Optional[str] = None,
    index: Optional[list[str]] = None,
    run_schema: Optional[RunSchema] = None,
    metadata: Optional[dict[str, str]] = None,
    baseline: Optional[Union[Run, RunQuery]] = None,
    include_tags: Optional[list[str]] = None,
    exclude_tags: Optional[list[str]] = None,
    require_tags: Optional[list[str]] = None,
) -> Run:
    """
    Create a new Run, report results to it, and close it. Wait for close to finish and start
    a TestSession with the given inputs.

    :param project: The Project to create the Run in.
    :param column_data: A pandas DataFrame with the results for the columns.
    :param scalar_data: An optional dictionary or DataFrame with the results for the scalars, if any.
    :param display_name: An optional display name for the Run.
    :param index: An optional list of column names to use as the unique identifier for rows in the column data.
    :param run_schema: An optional RunSchema to use for the Run. Will be inferred from the data if not provided.
    :param metadata: Any additional key:value pairs you want to track.
    :param wait_for_close: If True, the function will block for up to 3 minutes until the Run is closed, defaults to True.
    :param baseline: The Run or RunQuery to use as the baseline run, defaults to None. If None, the baseline defined in the TestConfig is used.
    :param include_tags: Optional list of Test Tag names to include in the Test Session.
    :param exclude_tags: Optional list of Test Tag names to exclude in the Test Session.
    :param require_tags: Optional list of Test Tag names to require in the Test Session.

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: The closed Run with the uploaded data.

    .. important::

        If no schema is provided, the schema will be inferred from the data. If provided,
        the schema will be used to validate the data.

    #### Examples:

    .. code-block:: python

        import dbnl
        import pandas as pd
        dbnl.login()


        proj = dbnl.get_or_create_project(name="test_p1")
        test_data = pd.DataFrame({"error": [0.11, 0.33, 0.52, 0.24]})

        run = dbnl.report_run_with_results_and_start_test_session(
            project=proj,
            column_data=test_data,
        )
    """
    run = report_run_with_results(
        project=project,
        column_data=column_data,
        scalar_data=scalar_data,
        display_name=display_name,
        index=index,
        run_schema=run_schema,
        metadata=metadata,
        wait_for_close=True,  # we must wait for the run to close before starting the test session
    )
    create_test_session(
        experiment_run=run,
        baseline=baseline,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        require_tags=require_tags,
    )
    return run


@validate_login
def wait_for_run_close(
    *,
    run: Run,
    timeout_s: float = 180.0,
    polling_interval_s: float = 3.0,
) -> Run:
    """
    Wait for a Run to close. Polls every polling_interval_s seconds until it is closed.

    :param run: Run to wait for
    :param timeout_s: Total wait time (in seconds) for Run to close, defaults to 180.0
    :param polling_interval_s: Time between polls (in seconds), defaults to 3.0

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLError: Run did not close after waiting for the `timeout_s` seconds
    :raises DBNLRunError: Run ended in ERRORED state
    """
    start = time.time()
    while run.completed_at is None and (time.time() - start) < timeout_s:
        run = get_run(run_id=run.id)
        time.sleep(polling_interval_s)

    if run.completed_at is None:
        raise DBNLError(
            f"Run {run} status is in non-terminal state '{run.status}' after waiting for {timeout_s} seconds"
        )

    if run.status != "closed":
        raise DBNLRunError(f"Run {run} ended in '{run.status}' state")

    return run


@validate_login
def create_metric(
    *,
    project: Project,
    name: str,
    expression_template: str,
    description: Optional[str] = None,
    greater_is_better: Optional[bool] = None,
) -> Metric:
    """
    Create a new Metric

    :param project: The Project to create the Metric for
    :param name: Name for the Metric
    :param expression_template: Expression template string e.g. `token_count({RUN}.question)`
    :param description: Optional description of what computation the metric is performing
    :param greater_is_better: Flag indicating whether greater values are semantically 'better' than lesser values

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Created Metric
    """
    try:
        validate_project(project)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    with handle_api_validation_error():
        resp_dict = api.post_metrics(
            project_id=project.id,
            name=name,
            expression_template=expression_template,
            description=description,
            greater_is_better=greater_is_better,
        )
    return Metric.from_dict(resp_dict)


@validate_login
def delete_metric(
    *,
    metric_id: str,
) -> None:
    """
    Delete a Metric by ID

    :param metric_id: ID of the metric to delete

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLAPIValidationError: dbnl API failed to validate the request

    :return: None
    """
    with handle_api_validation_error():
        api.delete_metric(metric_id=metric_id)


@validate_login
def get_metric_by_id(
    *,
    metric_id: str,
) -> Metric:
    """
    Get a Metric by ID

    :param metric_id: ID of the metric to get

    :raises DBNLNotLoggedInError: dbnl SDK is not logged in
    :raises DBNLAPIValidationError: dbnl API failed to validate the request

    :return: The requested metric
    """
    with handle_api_validation_error():
        resp_dict = api.get_metric_by_id(metric_id=metric_id)
    return Metric.from_dict(resp_dict)
