import pyarrow as pa
from numpy.typing import DTypeLike

from dbnl.sdk.types import DataTypeDict


def rag_context_dtype() -> DataTypeDict:
    """
    Get the data type for RAG context.

    :return: Data type.
    """
    return {
        "type": "list",
        "value_type": {
            # Document.
            "type": "struct",
            "fields": [
                # Document id (optional).
                {"name": "id", "type": "string"},
                # Document content (required).
                {"name": "content", "type": "string"},
                # Document metadata (optional).
                {"name": "metadata", "type": {"type": "map", "key_type": "string", "value_type": "string"}},
            ],
        },
    }


def rag_context_pyarrow_dtype() -> pa.DataType:
    """
    Get the PyArrow data type for RAG context.

    :return: PyArrow data type.
    """
    return pa.list_(
        # Document.
        pa.struct([
            # Document id (optional).
            pa.field("id", pa.string()),
            # Document content (required).
            pa.field("content", pa.string()),
            # Document metadata (optional).
            pa.field("metadata", pa.map_(pa.string(), pa.string())),
        ])
    )


def rag_context_pandas_dtype() -> DTypeLike:
    """
    Get the Pandas data type for RAG context.

    :return: Pandas data type.
    """
    return rag_context_pyarrow_dtype().to_pandas_dtype()
