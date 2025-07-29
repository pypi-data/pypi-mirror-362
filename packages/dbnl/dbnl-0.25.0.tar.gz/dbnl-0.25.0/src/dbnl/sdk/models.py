from __future__ import annotations

from dataclasses import dataclass, fields
from dataclasses import field as dataclass_field
from typing import Any, Generic, Literal, NamedTuple, Optional, TypedDict, TypeVar, Union

import pandas as pd
from dataclasses_json import DataClassJsonMixin, config
from typing_extensions import NotRequired, Self, override

from dbnl.sdk.types import (
    DataType,
    DataTypeDict,
    datatype_from_datatype_dict,
)

REPR_INDENT = 4

"""
When adding a new class that should be exposed in the documentation, make sure to update
/docs/classes.rst
"""


@dataclass(repr=False)
class DBNLObject(DataClassJsonMixin):
    def __repr__(self) -> str:
        return self._pretty_print()

    def _pretty_print(self, nested_indent: int = 0) -> str:
        field_reprs = []
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, list):
                value_repr = " " * (
                    2 * REPR_INDENT + nested_indent
                ) + f",\n{' ' * (2 * REPR_INDENT + nested_indent)}".join([f"{d}" for d in value])
                field_reprs.append(f"{field.name}=[\n{value_repr}\n{' ' * (REPR_INDENT + nested_indent)}]")
            elif isinstance(value, dict):
                value_repr = " " * (
                    2 * REPR_INDENT + nested_indent
                ) + f",\n{' ' * (2 * REPR_INDENT + nested_indent)}".join([
                    f"'{k}': {repr(v)}" for k, v in value.items()
                ])
                field_reprs.append(
                    f"{field.name}=" + "{" + f"\n{value_repr}\n{' ' * (REPR_INDENT + nested_indent)}" + "}"
                )
            elif isinstance(value, DBNLObject):
                field_reprs.append(f"{field.name}={value._pretty_print(nested_indent=REPR_INDENT)}")
            else:
                field_reprs.append(f"{field.name}={repr(value)}")
        return (
            f"{self.__class__.__name__}(\n{' ' * (REPR_INDENT + nested_indent)}"
            + f",\n{' ' * (REPR_INDENT + nested_indent)}".join(field_reprs)
            + f"\n{' ' * nested_indent})"
        )


class RunSchemaMetricDict(TypedDict):
    inputs: list[str]
    expression: NotRequired[str | None]


class AppContextDict(TypedDict):
    app_type: AppType
    mapped_name: str


class _BaseFieldSchemaDict(TypedDict):
    name: str
    description: NotRequired[str | None]
    component: NotRequired[str | None]
    greater_is_better: NotRequired[bool | None]
    metric: NotRequired[RunSchemaMetricDict | None]
    app_context: NotRequired[AppContextDict | None]


class _RunSchemaFieldSchemaDict(_BaseFieldSchemaDict):
    type: DataTypeDict


class RunSchemaColumnSchemaDict(_RunSchemaFieldSchemaDict):
    pass


class RunSchemaScalarSchemaDict(_RunSchemaFieldSchemaDict):
    pass


@dataclass(repr=False)
class Project(DBNLObject):
    id: str
    name: str
    description: Optional[str] = None


@dataclass(repr=False)
class ValueType(DBNLObject):
    type: str


@dataclass(repr=False)
class RunSchemaMetric(DBNLObject):
    inputs: list[str]
    expression: Optional[str] = dataclass_field(default=None, metadata=config(exclude=lambda x: x is None))


@dataclass(repr=False)
class Metric(DBNLObject):
    id: str
    project_id: str
    name: str
    expression_template: str
    description: Optional[str] = None
    greater_is_better: Optional[bool] = None


@dataclass(repr=False)
class AppContext(DBNLObject):
    app_type: AppType
    mapped_name: str


AppType = Literal["llm", "llm_question_answering", "llm_summarization"]


S = TypeVar("S", bound=Union[RunSchemaColumnSchemaDict, RunSchemaScalarSchemaDict])


@dataclass(repr=False)
class _RunSchemaFieldSchema(DBNLObject, Generic[S]):
    name: str
    type: DataType = dataclass_field(metadata=config(decoder=datatype_from_datatype_dict))
    description: Optional[str] = dataclass_field(default=None, metadata=config(exclude=lambda x: x is None))
    component: Optional[str] = dataclass_field(default=None, metadata=config(exclude=lambda x: x is None))
    greater_is_better: Optional[bool] = dataclass_field(default=None, metadata=config(exclude=lambda x: x is None))
    metric: Optional[RunSchemaMetric] = dataclass_field(default=None, metadata=config(exclude=lambda x: x is None))
    app_context: Optional[AppContext] = dataclass_field(default=None, metadata=config(exclude=lambda x: x is None))

    @classmethod
    def from_dict(
        cls,
        kvs: S,  # type: ignore[override]
        *,
        infer_missing: Any = False,
    ) -> Self:
        if isinstance(kvs, dict):
            return super().from_dict(dict(kvs), infer_missing=infer_missing)
        raise ValueError(f"Unsupported type for {cls.__name__}: {type(kvs)}")


@dataclass(repr=False)
class RunSchemaColumnSchema(_RunSchemaFieldSchema[RunSchemaColumnSchemaDict]):
    pass


@dataclass(repr=False)
class RunSchemaScalarSchema(_RunSchemaFieldSchema[RunSchemaScalarSchemaDict]):
    pass


@dataclass(repr=False)
class RunSchema(DBNLObject):
    columns: list[RunSchemaColumnSchema]
    scalars: Optional[list[RunSchemaScalarSchema]] = dataclass_field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    index: Optional[list[str]] = dataclass_field(default=None, metadata=config(exclude=lambda x: x is None))
    components_dag: Optional[dict[str, list[str]]] = dataclass_field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )


@dataclass(repr=False)
class Run(DBNLObject):
    id: str
    project_id: str
    run_schema: RunSchema = dataclass_field(metadata=config(field_name="schema"))
    display_name: Optional[str] = None
    metadata: Optional[dict[str, str]] = None
    status: Optional[Literal["pending", "closing", "closed", "canceled", "errored"]] = None
    completed_at: Optional[str] = None


@dataclass(repr=False)
class RunQuery(DBNLObject):
    id: str
    project_id: str
    name: str
    query: dict[str, Any]


class AssertionDict(TypedDict):
    name: str
    params: dict[str, float | int | str]


class TestSpecDict(TypedDict):
    project_id: str
    name: str
    statistic_name: str
    statistic_params: dict[str, float | int | str]
    statistic_inputs: list[dict[str, Any]]
    assertion: AssertionDict
    description: NotRequired[str]
    tag_ids: NotRequired[list[str]]


class ResultData(NamedTuple):
    columns: pd.DataFrame
    scalars: Union[pd.DataFrame, None] = None


@dataclass(repr=False)
class TestSessionInput(DBNLObject):
    run_alias: str
    run_id: Optional[str] = None
    run_query_id: Optional[str] = None

    @override
    def to_dict(self, encode_json: bool = False) -> dict[str, Any]:
        return {k: v for k, v in super().to_dict(encode_json).items() if v is not None}


@dataclass(repr=False)
class TestSession(DBNLObject):
    id: str
    project_id: str
    inputs: list[TestSessionInput]
    status: Literal["PENDING", "RUNNING", "PASSED", "FAILED"]
    failure: Optional[str] = None
    num_tests_passed: Optional[int] = None
    num_tests_failed: Optional[int] = None
    num_tests_errored: Optional[int] = None
    include_tag_ids: Optional[list[str]] = None
    exclude_tag_ids: Optional[list[str]] = None
    require_tag_ids: Optional[list[str]] = None
