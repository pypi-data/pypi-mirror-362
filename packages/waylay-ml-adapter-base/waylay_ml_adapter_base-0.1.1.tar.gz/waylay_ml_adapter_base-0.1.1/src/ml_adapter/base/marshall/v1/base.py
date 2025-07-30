"""V1 marshaller base."""

import abc
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any, Generic, cast

from ml_adapter.api import types as T
from ml_adapter.api.data import common as C
from ml_adapter.api.data import v1 as V1

from ..base import Marshaller, RequestMarshaller, ResponseMarshaller, WithScalarEncoding

V1Marshaller = Marshaller[T.MREQ, T.MRES, V1.V1Request, V1.V1PredictionResponse]
V1RequestMarshaller = RequestMarshaller[T.MREQ, V1.V1Request]
V1ResponseMarshaller = ResponseMarshaller[T.MRES, V1.V1Request, V1.V1PredictionResponse]

V1DictRequestMarshaller = V1RequestMarshaller[T.VDict]
V1DictResponseMarshaller = V1ResponseMarshaller[T.VDict]

V1ValueOrDictRequestMarshaller = V1RequestMarshaller[T.VorDict]
V1ValueOrDictResponseMarshaller = V1ResponseMarshaller[T.VorDict]

V1Marshaller = Marshaller[T.MREQ, T.MRES, V1.V1Request, V1.V1PredictionResponse]
V1DictMarshaller = Marshaller[T.VDict, T.VDict, V1.V1Request, V1.V1PredictionResponse]
V1ValueOrDictMarshaller = Marshaller[
    T.VorDict, T.VorDict, V1.V1Request, V1.V1PredictionResponse
]


class WithV1Encoding(WithScalarEncoding):
    """Extraction of encoding of decoding parameters."""

    SINGLE_MAIN_AS_VALUE = True
    DEFAULT_INPUT_NAME = "main"
    DEFAULT_OUTPUT_NAME = "main"

    def map_decoding_kwargs(
        self, parameters: C.Parameters | None, **kwargs
    ) -> Mapping[str, Any]:
        """Extract arguments for mapping V1 requests."""
        if parameters is not None and len(parameters) > 0:
            return {**kwargs, **parameters}
        return kwargs

    def map_encoding_kwargs(
        self, parameters: C.Parameters | None, **kwargs
    ) -> Mapping[str, Any]:
        """Extract arguments for mapping V1 requests."""
        if parameters is not None and len(parameters) > 0:
            kwargs = {**kwargs, **parameters}
        return kwargs

    def as_single_main_input(self, named_tensors: V1.NamedValues):
        """Return the single main input tensor, if present."""
        if self.SINGLE_MAIN_AS_VALUE and self.has_single_key(
            self.DEFAULT_INPUT_NAME, named_tensors
        ):
            return named_tensors[self.DEFAULT_INPUT_NAME]
        return None

    def as_single_main_output(self, named_tensors: V1.NamedValues):
        """Return the single main output, if present."""
        if self.SINGLE_MAIN_AS_VALUE and self.has_single_key(
            self.DEFAULT_OUTPUT_NAME, named_tensors
        ):
            return named_tensors[self.DEFAULT_OUTPUT_NAME]
        return None

    def has_single_key(self, key: str, value: Any):
        """Check wether a value has this single key."""
        return isinstance(value, dict) and key in value and len(value) == 1


class V1RequestMarshallerBase(
    V1RequestMarshaller[T.MREQ], WithV1Encoding, Generic[T.MREQ], abc.ABC
):
    """Base Marshaller from/to the V1 protocol requests."""

    def map_request(self, request: V1.V1Request, /, **kwargs) -> T.MREQ:
        """Convert a remote request to an model inference request."""
        kwargs = self.map_decoding_kwargs(request.get("parameters"), **kwargs)
        if "instances" in request:
            return self.map_request_instances(request["instances"], **kwargs)
        if "inputs" in request:
            return self.map_request_inputs(request["inputs"], **kwargs)
        return self.map_request_inputs({}, **kwargs)

    def map_request_inputs(self, inputs: V1.ColumnData, /, **kwargs) -> T.MREQ:
        """Map input tensor in columnar format."""
        if is_v1_named_value(inputs):
            main_input = self.as_single_main_input(inputs)
            if main_input is None:
                return self.map_named_inputs(inputs, **kwargs)
            inputs = main_input
        return self.map_value_input(cast(V1.ValueOrTensor, inputs), **kwargs)

    def map_request_instances(self, instances: V1.RowData, /, **kwargs) -> T.MREQ:
        """Map input tensors in row format."""
        if (
            isinstance(instances, list)
            and len(instances) > 0
            and is_v1_named_value(instances[0])
        ):
            return self.map_named_instances(
                cast(list[V1.NamedValues], instances), **kwargs
            )
        return self.map_value_input(cast(V1.ValueOrTensor, instances), **kwargs)

    @abc.abstractmethod
    def map_named_inputs(self, data: V1.NamedValues, /, **kwargs) -> T.MREQ:
        """Create named inputs."""

    @abc.abstractmethod
    def map_value_input(self, data: V1.ValueOrTensor, /, **kwargs) -> T.MREQ:
        """Create value inputs."""

    @abc.abstractmethod
    def map_named_instances(self, instances: list[V1.NamedValues]) -> T.MREQ:
        """Map named instances request."""

    @abc.abstractmethod
    def encode_as_named(self, request: T.MREQ, **kwargs) -> V1.NamedValues:
        """Encode an inference request as a dict of V1 tensors."""

    def encode_request(
        self,
        request: T.MREQ,
        parameters: C.Parameters | None = None,
        as_instances: bool | None = None,
        **kwargs,
    ) -> V1.V1Request:
        """Encode a V1 inference request."""
        req: V1.V1Request = {}
        if parameters is not None and len(parameters) > 0:
            req["parameters"] = parameters
            kwargs = self.map_encoding_kwargs(parameters, **kwargs)
        named_tensors = self.encode_as_named(request, **kwargs)
        # use 'instances' request if requested or only a default input is
        # given .. except if multiple inputs have different dimensions
        main_input = self.as_single_main_input(named_tensors)
        encode_as_instances = (
            as_instances is not False
            and (as_instances is True or main_input is not None)
            and same_0th_dimension(named_tensors.values())
        )
        if encode_as_instances:
            req["instances"] = self._encode_named_as_instances(named_tensors)
        elif len(named_tensors) > 0:
            if main_input is not None:
                req["inputs"] = main_input
            else:
                req["inputs"] = named_tensors
        return req

    def _encode_named_as_instances(self, named_tensors: V1.NamedValues) -> V1.RowData:
        if len(named_tensors) == 0:
            return []
        main_input = self.as_single_main_input(named_tensors)
        if main_input is not None:
            return main_input
        keys = named_tensors.keys()
        evidence = next(iter(named_tensors.values()))
        if not isinstance(evidence, list):
            return [{k: named_tensors[k] for k in keys}]
        return [{k: named_tensors[k][i] for k in keys} for i in range(len(evidence))]


class V1ResponseMarshallerBase(
    V1ResponseMarshaller[T.MRES], WithV1Encoding, Generic[T.MRES], abc.ABC
):
    """Base Marshaller from/to the V1 protocol."""

    def map_response_parameters(
        self, output_params: C.Parameters | None, /, **kwargs
    ) -> C.Parameters:
        """Extract all request params."""
        if output_params:
            return {**output_params, **kwargs}
        return kwargs

    def map_response(
        self,
        request: V1.V1Request,
        response: T.MRES,
        output_params: C.Parameters | None = None,
        /,
        **kwargs,
    ) -> V1.V1PredictionResponse:
        """Convert a model inference response to the remote protocol."""
        kwargs = self.map_encoding_kwargs(request.get("parameters"), **kwargs)
        kwargs = self.map_encoding_kwargs(output_params, **kwargs)

        mapped_response: V1.V1PredictionResponse = {}
        parameters = self.map_response_parameters(output_params, **kwargs)
        if parameters is not None and len(parameters) > 0:
            mapped_response["parameters"] = parameters

        enc_resp = self.map_response_data(response, **kwargs)
        keys = enc_resp.keys()
        if len(keys) == 0:
            return mapped_response
        map_columnar = "inputs" in request or not same_0th_dimension(enc_resp.values())
        output_key = "outputs" if map_columnar else "predictions"
        if (main_output := self.as_single_main_output(enc_resp)) is not None:
            mapped_response[output_key] = main_output
            return mapped_response
        if map_columnar:
            mapped_response[output_key] = enc_resp
            return mapped_response
        # return list of dicts in 'predictions'
        main_key = next(iter(keys))
        main_data = enc_resp[main_key]
        if not isinstance(main_data, list):
            enc_resp = [enc_resp]
        else:
            _0th_dimension = len(main_data)
            enc_resp = [
                {key: cast(V1.Tensor, enc_resp[key])[idx] for key in keys}
                for idx in range(_0th_dimension)
            ]
        mapped_response[output_key] = enc_resp
        return mapped_response

    @abc.abstractmethod
    def map_response_data(self, response: T.MRES, /, **params) -> V1.NamedValues:
        """Map model response to named values."""

    @abc.abstractmethod
    def decode_empty_response(self, /, **kwargs) -> T.MRES:
        """Create an empty request."""

    @abc.abstractmethod
    def decode_named_values(
        self, response: list[V1.NamedValues], /, **params
    ) -> T.MRES:
        """Decode a v1 list of named values."""

    @abc.abstractmethod
    def decode_response_value(self, response: V1.ValueOrTensor, /, **params) -> T.MRES:
        """Decode a v1 tensor value."""

    @abc.abstractmethod
    def decode_output_response(self, response: V1.ColumnData, /, **kwargs) -> T.MRES:
        """Decode a V1 output response."""

    def decode_predictions(self, response: V1.RowData, /, **kwargs) -> T.MRES:
        """Decode a V1 prediction response."""
        if (
            isinstance(response, list)
            and len(response) > 0
            and is_v1_named_value(response[0])
        ):
            return self.decode_named_values(
                cast(list[V1.NamedValues], response), **kwargs
            )
        return self.decode_response_value(cast(V1.ValueOrTensor, response), **kwargs)

    def decode_response(
        self, response: V1.V1PredictionResponse, /, **kwargs
    ) -> (T.MRES, T.Parameters | None):
        """Decode a V1 inference response."""
        response_params = self.decode_response_parameters(
            response.get("parameters"), **kwargs
        )
        kwargs = self.map_decoding_kwargs(response_params, **kwargs)
        if "predictions" in response:
            decoded = self.decode_predictions(response["predictions"], **kwargs)
        elif "outputs" in response:
            decoded = self.decode_output_response(response["outputs"], **kwargs)
        else:
            decoded = self.decode_empty_response(**kwargs)

        return decoded, response_params

    def decode_response_parameters(
        self, parameters: C.Parameters | None, **_kwargs
    ) -> T.Parameters:
        """Decode V1 response parameters."""
        return parameters or {}


class WithV1TensorEncoding(Generic[T.V], abc.ABC):
    """Provides encoding and decoding of V1 tensors."""

    @abc.abstractmethod
    def decode(self, data: V1.ValueOrTensor, **kwargs) -> T.V:
        """Decode a V1 value or tensor."""

    @abc.abstractmethod
    def encode(self, data: T.V, **kwargs) -> V1.ValueOrTensor:
        """Encode a V1 value or tensor."""


class V1DictRequestMarshallerBase(
    V1RequestMarshallerBase[T.VDict], WithV1TensorEncoding[T.V], Generic[T.V], abc.ABC
):
    """V1 Request Marshaller all requests to a Dict of tensors.

    Uses DEFAULT_INPUT_NAME as key for non-dict inputs.
    """

    def map_named_inputs(self, data: V1.NamedValues, /, **kwargs) -> T.VDict:
        """Map V1 tensor dict to a tensor dict."""
        return {name: self.decode(values, **kwargs) for name, values in data.items()}

    def map_value_input(self, data: V1.ValueOrTensor, /, **kwargs) -> T.VDict:
        """Map a V1 tensor to a tensor dict."""
        return {self.DEFAULT_INPUT_NAME: self.decode(data, **kwargs)}

    def map_named_instances(self, instances: list[V1.NamedValues], **kwargs) -> T.VDict:
        """Map a V1 row-oriented list to a tensor dict."""
        # uses intermediate list objects, to be optimized in concrete classes.
        request: V1.NamedValues = defaultdict(list)
        for instance in instances:
            for name, value in instance.items():
                request[name].append(value)
        return self.map_named_inputs(request, **kwargs)

    def encode_as_named(self, request: T.VDict, **kwargs) -> V1.NamedValues:
        """Encode a tensor dict to a v1 dict."""
        return {name: self.encode(value, **kwargs) for name, value in request.items()}


class V1ValueOrDictRequestMarshallerBase(
    V1RequestMarshallerBase[T.V | T.VDict],
    WithV1TensorEncoding[T.V],
    Generic[T.V],
    abc.ABC,
):
    """V1 Request Marshaller all requests to a tensor or Dict of tensors."""

    def map_named_inputs(self, data: V1.NamedValues, /, **kwargs) -> T.VorDict:
        """Map a V1 dict to a tensor or tensor dict."""
        if (main_input := self.as_single_main_input(data)) is not None:
            return self.decode(main_input, **kwargs)
        return {name: self.decode(values, **kwargs) for name, values in data.items()}

    def map_value_input(self, data: V1.ValueOrTensor, /, **kwargs) -> T.VorDict:
        """Map a v1 tensor to a tensor or dict."""
        return self.decode(data, **kwargs)

    def map_named_instances(
        self, instances: list[V1.NamedValues], **kwargs
    ) -> T.VorDict:
        """Map a V1 row-oriented list to a tensor or dict."""
        # uses intermediate list objects, to be optimized in concrete classes.
        request: V1.NamedValues = defaultdict(list)
        for instance in instances:
            for name, value in instance.items():
                request[name].append(value)
        return self.map_named_inputs(request, **kwargs)

    def encode_as_named(self, request: T.VorDict, **kwargs) -> V1.NamedValues:
        """Encode a tensor or dict to a V1 row-oriented request."""
        if isinstance(request, dict):
            return {
                name: self.encode(value, **kwargs) for name, value in request.items()
            }
        return {self.DEFAULT_INPUT_NAME: self.encode(request, **kwargs)}


class V1DictResponseMarshallerBase(
    V1ResponseMarshallerBase[T.VDict], WithV1TensorEncoding[T.V], Generic[T.V], abc.ABC
):
    """V1 Response Marshaller for dict of tensors."""

    def map_response_data(self, response: T.VDict, /, **kwargs) -> V1.NamedValues:
        """Map model response to named values."""
        return {name: self.encode(value, **kwargs) for name, value in response.items()}

    def decode_empty_response(self, /, **kwargs) -> T.VDict:
        """Construct an empty response."""
        return {}

    def decode_named_values(
        self, response: list[V1.NamedValues], /, **kwargs
    ) -> T.VDict:
        """Decode a V1 row-formatted response."""
        assert len(response) > 0
        evidence = response[0]
        keys = evidence.keys()
        return {
            key: self.decode([entry[key] for entry in response], **kwargs)
            for key in keys
        }

    def decode_response_value(self, response: V1.ValueOrTensor, /, **kwargs) -> T.VDict:
        """Decode a response tensor value."""
        return {self.DEFAULT_OUTPUT_NAME: self.decode(response, **kwargs)}

    def decode_output_response(self, response: V1.ColumnData, /, **kwargs) -> T.VDict:
        """Decode a columnar data response."""
        if is_v1_named_value(response):
            return {
                key: self.decode(value, **kwargs) for key, value in response.items()
            }
        return self.decode_response_value(response, **kwargs)


class V1ValueOrDictResponseMarshallerBase(
    V1ResponseMarshallerBase[T.VorDict],
    WithV1TensorEncoding[T.V],
    Generic[T.V],
    abc.ABC,
):
    """V1 Response Marshaller for tensors or dict of tensors."""

    def map_response_data(self, response: T.VorDict, /, **kwargs) -> V1.NamedValues:
        """Map model response to named values."""
        if is_v1_named_value(response):
            return {
                name: self.encode(value, **kwargs) for name, value in response.items()
            }
        return {self.DEFAULT_OUTPUT_NAME: self.encode(response, **kwargs)}

    def decode_empty_response(self, /, **_kwargs) -> T.VorDict:
        """Construct an empty response."""
        return {}

    def decode_named_values(
        self, response: list[V1.NamedValues], /, **kwargs
    ) -> T.VorDict:
        """Decode a V1 row-formatted response."""
        assert len(response) > 0
        evidence = response[0]
        keys = evidence.keys()
        return {
            key: self.decode([entry[key] for entry in response], **kwargs)
            for key in keys
        }

    def decode_response_value(
        self, response: V1.ValueOrTensor, /, **kwargs
    ) -> T.VorDict:
        """Decode a response tensor value."""
        return self.decode(response, **kwargs)

    def decode_output_response(self, response: V1.ColumnData, /, **kwargs) -> T.VorDict:
        """Decode a columnar data response."""
        decoded = None
        if is_v1_named_value(response):
            decoded = {
                key: self.decode(value, **kwargs) for key, value in response.items()
            }
        else:
            decoded = self.decode_response_value(response, **kwargs)
        if (main_output := self.as_single_main_output(decoded)) is not None:
            return main_output
        return decoded


def is_v1_named_value(value: Any) -> bool:
    """Check if a value is a named tensor input."""
    # a dict that is not a encoded binary value
    return isinstance(value, dict) and "b64" not in value


def same_0th_dimension(list_of_tensors: Iterable[V1.ValueOrTensor]) -> bool:
    """Return false if not all tensor have same 0th length."""
    tensor_it = iter(list_of_tensors)
    t0 = next(tensor_it, None)
    len_0 = len(t0) if isinstance(t0, list) else 0
    return all(len_0 == (len(t) if isinstance(t, list) else 0) for t in tensor_it)
