"""Mapping and validation of remote data to and from model inference."""

import abc
from abc import ABC
from typing import Any, Generic

import ml_adapter.api.data.common as C
import ml_adapter.api.types as T


class WithScalarEncoding:
    """Algorithm to decide on the scalar tensor encoding."""

    scalar_data_type: C.DataType | None = None

    def set_scalar_type(self, datatype: C.DataType | None):
        """Configure the default scalar type."""
        self.scalar_data_type = datatype


class RequestMarshaller(WithScalarEncoding, Generic[T.MREQ, T.RREQ], ABC):
    """Base class to marshall inference requests."""

    @abc.abstractmethod
    def map_request(self, request: T.RREQ, /, **kwargs) -> T.MREQ:
        """Convert a remote request to an model inference request."""

    @abc.abstractmethod
    def encode_request(
        self, request: T.MREQ, parameters: T.Parameters | None = None, **kwargs
    ) -> T.RREQ:
        """Convert a model inference request to the remote protocol."""


class ResponseMarshaller(WithScalarEncoding, Generic[T.MRES, T.RREQ, T.RRES], ABC):
    """Base class to marshall inference responses."""

    @abc.abstractmethod
    def map_response(
        self,
        request: T.RREQ,
        response: T.MRES,
        output_params: dict[str, Any] | None = None,
        /,
        **kwargs,
    ) -> T.RRES:
        """Convert a model inference response to the remote protocol."""

    @abc.abstractmethod
    def decode_response(
        self, response: T.RRES, /, **kwargs
    ) -> (T.MRES, T.Parameters | None):
        """Decode a remote model inference response."""


class Marshaller(
    RequestMarshaller[T.MREQ, T.RREQ],
    ResponseMarshaller[T.MRES, T.RREQ, T.RRES],
    Generic[T.MREQ, T.MRES, T.RREQ, T.RRES],
    ABC,
):
    """Abstract base class to marshall inference requests and responses.

    Methods used to invoke the model in a _plugin_ or _webscript_:
    * `map_request()` maps remote requests (generic type `RREQ`)
    to native requests (generic type `MREQ`)
    * `map_response()` maps native responses (generic type `MRES`)
    to remote a response (generic type `RRES`)

    Methods used to test roundtrip encoding in a client:
    * `encode_request()` encodes a native request
    to a remote request that can be sent to a waylay function.
    * `decode_response()` decodes a remote response from a function
    to native a response.

    """


class NoMarshaller(
    RequestMarshaller[T.MREQ, T.MREQ],
    ResponseMarshaller[T.MRES, T.MREQ, T.MREQ],
    Generic[T.MREQ, T.MRES],
):
    """Identity marshaller."""

    def map_request(self, request: T.MREQ, /, **kwargs) -> T.MREQ:
        """Convert a remote request to an model inference request."""
        return request

    def encode_request(
        self, request: T.MREQ, parameters: T.Parameters | None = None, **kwargs
    ) -> T.MREQ:
        """Encode a tensor request with default input name."""
        return request

    def decode_response(
        self, response: T.MRES, /, **kwargs
    ) -> (T.MRES, T.Parameters | None):
        """Decode the default tensor from a V1 response."""
        return response, {}

    def map_response(
        self,
        request: T.MREQ,
        response: T.MRES,
        output_params: dict[str, Any] | None = None,
        /,
        **kwargs,
    ) -> T.MRES:
        """Convert a model inference response to the remote protocol."""
        return response
