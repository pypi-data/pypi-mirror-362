"""V1 Marshaller to python lists."""

import base64
from typing import Any, cast

from ml_adapter.api.data import common as C
from ml_adapter.api.data import v1 as V1

from .base import (
    V1DictRequestMarshallerBase,
    V1DictResponseMarshallerBase,
    V1ValueOrDictRequestMarshallerBase,
    V1ValueOrDictResponseMarshallerBase,
    WithV1TensorEncoding,
)


def decode_binary(value: Any) -> C.ScalarOrTensor:
    """Decode a base64 binary value."""
    if isinstance(value, str):
        return base64.b64decode(value)
    if isinstance(value, dict):
        return base64.b64decode(value["b64"])
    if not isinstance(value, list):
        return value
    evidence = value[0]
    if isinstance(evidence, dict):
        return [
            base64.b64decode(cast(V1.EncodedBinaryValue, v).get("b64", ""))
            for v in value
        ]
    if isinstance(evidence, str):
        return [base64.b64decode(cast(str, v)) for v in value]
    if isinstance(evidence, list):
        return [decode_binary(t) for t in value]
    return value


def encode_binary(value: C.BytesTensor, wrap=False) -> V1.Tensor:
    """Encode a base64 binary tensor."""
    if isinstance(value, list):
        return [encode_binary(cast(C.BytesTensor, t), wrap=wrap) for t in value]
    if isinstance(value, bytes):
        enc = base64.b64encode(value).decode("utf-8")
        return {"b64": enc} if wrap else enc
    return value


class V1ScalarOrBytesEncoder(WithV1TensorEncoding):
    """Encoding of V1 payloads as plain python values or lists."""

    def encode(self, data: C.ScalarOrBytes, **kwargs) -> V1.ValueOrTensor:
        """Map a value or tensor, encoding binary data."""
        if V1.is_binary(data, **kwargs):
            wrap = kwargs.get("datatype") != C.DataTypes.BYTES
            return encode_binary(cast(C.BytesTensor, data), wrap=wrap)
        return cast(V1.ValueOrTensor, data)

    def decode(self, data: V1.ValueOrTensor, **kwargs) -> C.ScalarOrBytes:
        """Map a value or tensor, decoding binary data."""
        if V1.is_binary(data, **kwargs):
            return decode_binary(data)
        if isinstance(data, list):
            return cast(C.Tensor, data)
        return cast(C.Scalar, data)


class V1ListMarshaller(
    V1ScalarOrBytesEncoder,
    V1ValueOrDictRequestMarshallerBase[C.ScalarOrBytes],
    V1ValueOrDictResponseMarshallerBase[C.ScalarOrBytes],
):
    """V1 Marshaller to and from python values or dicts."""


class V1DictMarshaller(
    V1ScalarOrBytesEncoder,
    V1DictRequestMarshallerBase[C.ScalarOrBytes],
    V1DictResponseMarshallerBase[C.ScalarOrBytes],
):
    """V1 Marshaller to and from dicts of python values."""
