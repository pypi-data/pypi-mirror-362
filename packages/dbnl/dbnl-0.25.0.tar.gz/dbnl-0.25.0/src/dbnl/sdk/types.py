from dataclasses import dataclass
from typing import Literal, TypedDict, Union

import pyarrow as pa
from dataclasses_json import dataclass_json

PrimitiveTypeLiteral = Literal["boolean", "int", "long", "float", "double", "string", "category"]
ContainerTypeLiteral = Literal["list", "map", "struct"]


class ListTypeDict(TypedDict):
    type: Literal["list"]
    value_type: "DataTypeDict"


class MapTypeDict(TypedDict):
    type: Literal["map"]
    key_type: "DataTypeDict"
    value_type: "DataTypeDict"


class FieldDict(TypedDict):
    name: str
    type: "DataTypeDict"


class StructTypeDict(TypedDict):
    type: Literal["struct"]
    fields: list[FieldDict]


DataTypeDict = Union[PrimitiveTypeLiteral, ListTypeDict, MapTypeDict, StructTypeDict]


@dataclass_json
@dataclass(repr=False)
class ListType:
    value_type: "DataType"
    type: str = "list"

    def __str__(self) -> str:
        return f"list<{self.value_type}>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.type!r}, value_type={self.value_type!r})"


@dataclass_json
@dataclass(repr=False)
class MapType:
    key_type: "DataType"
    value_type: "DataType"
    type: str = "map"

    def __str__(self) -> str:
        return f"map<{self.key_type}, {self.value_type}>"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(type={self.type!r}, key_type={self.key_type!r}, value_type={self.value_type!r})"
        )


@dataclass_json
@dataclass(repr=False)
class Field:
    name: str
    type: "DataType"

    def __str__(self) -> str:
        return f"{self.name}: {self.type}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, type={self.type!r})"


@dataclass_json
@dataclass(repr=False)
class StructType:
    fields: list[Field]
    type: str = "struct"

    def __str__(self) -> str:
        return f"struct<{', '.join([str(f) for f in self.fields])}>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.type!r}, fields=[{', '.join([repr(f) for f in self.fields])}])"


DataType = Union[PrimitiveTypeLiteral, ListType, MapType, StructType]


def datatype_dict_from_arrow(dtype: pa.DataType) -> DataTypeDict:
    if pa.types.is_integer(dtype):
        return "int"
    elif pa.types.is_floating(dtype):
        return "float"
    elif pa.types.is_boolean(dtype):
        return "boolean"
    elif pa.types.is_string(dtype):
        return "string"
    elif pa.types.is_dictionary(dtype):
        return "category"
    elif pa.types.is_list(dtype):
        assert isinstance(dtype, pa.ListType)
        value_type = dtype.value_type
        return {
            "type": "list",
            "value_type": datatype_dict_from_arrow(value_type),
        }
    elif pa.types.is_map(dtype):
        assert isinstance(dtype, pa.MapType)
        key_type = dtype.key_type
        value_type = dtype.item_type
        return {
            "type": "map",
            "key_type": datatype_dict_from_arrow(key_type),
            "value_type": datatype_dict_from_arrow(value_type),
        }
    elif pa.types.is_struct(dtype):
        assert isinstance(dtype, pa.StructType)
        return {
            "type": "struct",
            "fields": [
                {
                    "name": dtype.field(i).name,
                    "type": datatype_dict_from_arrow(dtype.field(i).type),
                }
                for i in range(dtype.num_fields)
            ],
        }
    else:
        raise ValueError(f"Unsupported data type: {dtype}")


def datatype_from_datatype_dict(d: DataTypeDict) -> DataType:
    if isinstance(d, str):
        return d
    elif d["type"] == "list":
        return ListType(value_type=datatype_from_datatype_dict(d["value_type"]))
    elif d["type"] == "map":
        return MapType(
            key_type=datatype_from_datatype_dict(d["key_type"]), value_type=datatype_from_datatype_dict(d["value_type"])
        )
    elif d["type"] == "struct":
        return StructType(
            fields=[Field(name=f["name"], type=datatype_from_datatype_dict(f["type"])) for f in d["fields"]]
        )
    else:
        raise ValueError(f"Unsupported data type: {d}")
