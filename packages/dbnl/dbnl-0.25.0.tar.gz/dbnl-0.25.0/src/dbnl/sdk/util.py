from __future__ import annotations

from collections.abc import Sequence
from typing import Optional, TypedDict

import pandas as pd
import pyarrow as pa

from dbnl.errors import DBNLInputValidationError
from dbnl.sdk.types import datatype_dict_from_arrow

from .models import (
    Run,
    RunQuery,
    RunSchemaColumnSchema,
    RunSchemaColumnSchemaDict,
    RunSchemaScalarSchema,
    RunSchemaScalarSchemaDict,
    TestSessionInput,
    _RunSchemaFieldSchemaDict,
)


def _get_schemas_from_dataframe(
    df: pd.DataFrame,
) -> list[_RunSchemaFieldSchemaDict]:
    """
    Get the column schemas for the columns in the provided dataframe.

    :param df: Dataframe from which to extract columns.
    :return: List of field schemas.
    """
    fields: list[RunSchemaColumnSchemaDict] = []
    schema = pa.Schema.from_pandas(df)
    for f in schema:
        try:
            dtype = datatype_dict_from_arrow(f.type)
        except ValueError as e:
            raise ValueError(f"Field '{f.name}' has unsupported data type: {f.type}") from e
        fields.append({
            "name": f.name,
            "type": dtype,
        })
    return fields


def get_column_schemas_from_dataframe(df: pd.DataFrame) -> list[RunSchemaColumnSchemaDict]:
    return _get_schemas_from_dataframe(df)


def get_scalar_schemas_from_dataframe(df: pd.DataFrame) -> list[RunSchemaScalarSchemaDict]:
    return _get_schemas_from_dataframe(df)


def get_run_schema_columns_from_dataframe(df: pd.DataFrame) -> list[RunSchemaColumnSchema]:
    column_schema_dict = get_column_schemas_from_dataframe(df)
    return [RunSchemaColumnSchema.from_dict(d) for d in column_schema_dict]


def get_run_schema_scalars_from_dataframe(df: pd.DataFrame) -> list[RunSchemaScalarSchema]:
    scalar_schema_dict = get_scalar_schemas_from_dataframe(df)
    return [RunSchemaScalarSchema.from_dict(d) for d in scalar_schema_dict]


def make_test_session_input(
    *,
    run: Optional[Run] = None,
    run_query: Optional[RunQuery] = None,
    run_alias: str = "EXPERIMENT",
) -> TestSessionInput:
    """
    Create a TestSessionInput object from a Run or a RunQuery. Useful for creating TestSessions right after closing a Run.

    :param run: The Run to create the TestSessionInput from
    :param run_query: The RunQuery to create the TestSessionInput from
    :param run_alias: Alias for the Run, must be 'EXPERIMENT' or 'BASELINE', defaults to "EXPERIMENT"

    :raises DBNLInputValidationError: If both run and run_query are None

    :return: TestSessionInput object
    """
    if run_alias not in ["EXPERIMENT", "BASELINE"]:
        raise DBNLInputValidationError("run_alias must be 'EXPERIMENT' or 'BASELINE'")
    if bool(run) == bool(run_query):
        raise DBNLInputValidationError("Exactly one of `run` or `run_query` must be provided")
    if run:
        return TestSessionInput(run_alias=run_alias, run_id=run.id)
    assert run_query
    return TestSessionInput(run_alias=run_alias, run_query_id=run_query.id)


class ColumnSchemaDict(TypedDict, total=False):
    component: Optional[str]


def get_default_components_dag_from_column_schemas(
    column_schemas: Sequence[ColumnSchemaDict],
) -> Optional[dict[str, list[str]]]:
    """
    Gets the unconnected components DAG from a list of column schemas. If there are no components, returns None.
    The default components dag is of the form
    {
        "component1": [],
        "component2": [],
        ...}

    :param column_schemas: list of column schemas

    :return: dictionary of components DAG or None
    """
    components_dag: dict[str, list[str]] = {
        c["component"]: [] for c in column_schemas if "component" in c and c["component"] is not None
    }
    if not components_dag:
        return None
    return components_dag
