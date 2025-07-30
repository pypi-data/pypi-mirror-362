"""Base Model Adapter."""

import inspect
from typing import Generic, cast

import ml_adapter.api.types as T
from ml_adapter.api.data.common import NO_PROTOCOL, DataType, Parameters
from ml_adapter.base.assets import PythonMLAdapter
from ml_adapter.base.model.access import WithModel

from .marshall import Marshaller, NoMarshaller


class ModelAdapter(Generic[T.MREQ, T.MRES, T.RREQ, T.RRES]):
    """Model Adapter base.

    Provides the basic contract for exposing
    a model to a waylay _plugin_ or _webscript_.
    * Delegates to a `marshaller` to map the remote,
      json-compatible python data structures
      from and to the native tensor data structures for the ML framework.
    * Delegates to a `invoker` to find the model method to be called.
    * The `call` method maps remote requests and invokes the model method.
    * The `call_remote` method tests the round trip serialization, encoding
      native data request to remotable and back before invoking `call`.
    """

    DEFAULT_MARSHALLER = NoMarshaller
    PROTOCOL = NO_PROTOCOL

    model_method = ""
    _invoker: T.ModelInvoker[T.MREQ, T.MRES] | None

    def __init__(
        self,
        marshaller: Marshaller[T.MREQ, T.MRES, T.RREQ, T.RRES] | None = None,
        invoker: T.ModelInvoker[T.MREQ, T.MRES] | None = None,
        model_method: str | None = None,
        output_params: bool = False,
        datatype: DataType | None = None,
        **kwargs,
    ):
        """Create a model adapter.

        Parameters
        ----------
        marshaller: Marshaller
            The marshaller that maps requests and response to the native tensor format.
        model_method: str
            The name of the method to invoke, normally ""
            if the model itself is callable.
        invoker: T.ModelInvoker
            Alternate method to invoke the model (if not a model method)
        output_params: bool
            If true, the invoked model is expected to return a tuple of
            (tensor_result, parameters), where the parameters are
            handed seperately to the `marshaller.map_response`
        datatype: Datatype | None
            if set, overrides the default scalar datatype used by the marshaller
        kwargs:
            Ignored parameters for mixed-in constructors.

        """
        super().__init__(**kwargs)
        self.marshaller = marshaller or self.DEFAULT_MARSHALLER()
        if datatype is not None:
            self.marshaller.set_scalar_type(datatype)
        if model_method is not None:
            self.model_method = model_method
        self._invoker = invoker
        self.output_params = output_params

    @property
    def invoker(self) -> T.ModelInvoker:
        """Get a method to natively invoke the model."""
        if self._invoker is not None:
            return self._invoker
        model = self.model
        if model_method := self.model_method:
            return getattr(model, model_method)
        return model

    async def call(self, request: T.RREQ, /, **kwargs) -> T.RRES:
        """Invoke the model with a remote inference request."""
        model_request = self.marshaller.map_request(request, **kwargs)
        await self.assure_model_loaded()
        model_response = self.invoker(model_request, **kwargs)
        if inspect.isawaitable(model_response):
            model_response = await model_response
        response_params = None
        if self.output_params:
            model_response, response_params = model_response
        return self.marshaller.map_response(
            request, model_response, response_params, **kwargs
        )

    async def assure_model_loaded(self):
        """Assures a model is loaded if this adapter provides loading."""
        if isinstance(self, WithModel):
            model_adapter = cast(WithModel, self)
            try:
                return model_adapter.model
            except Exception:
                if model_adapter.model_asset is not None:
                    return await model_adapter.model_asset.load()
                raise

    async def __call__(self, request: T.RREQ, /, **kwargs) -> T.RRES:
        """Invoke the model with a remote inference request."""
        return await self.call(request, **kwargs)

    async def call_remote(
        self, request: T.MREQ, parameters: T.Parameters | None = None, **kwargs
    ) -> tuple[T.MRES, T.Parameters]:
        """Test invoke a model with marshalled request and response data."""
        remote_request = self.marshaller.encode_request(request, parameters, **kwargs)
        remote_resp = await self.call(remote_request)
        return self.marshaller.decode_response(remote_resp, **kwargs)


class TensorModelAdapter(
    ModelAdapter[T.VorDict, T.VorDict, T.RREQ, T.RRES], Generic[T.V, T.RREQ, T.RRES]
):
    """Model adapter that uses (dicts of) tensors as inputs and outputs.

    Requests are mapped to the model invocation using named parameters,
    falling back to mapping the "main" entry to the first positional parameter.
    """

    @property
    def invoker(self) -> T.ModelInvoker:
        """Get a method to natively invoke the model."""
        invoker = super().invoker
        return as_tensor_dict_callable(invoker)


class ModelAdapterBase(
    TensorModelAdapter[T.V, T.RREQ, T.RRES],
    PythonMLAdapter,
    WithModel[T.MI],
    Generic[T.V, T.RREQ, T.RRES, T.MI],
):
    """Generic model adapter for plugs and webscripts.

    - supports creation of waylay webscript and plug functions
    - pluggable tensor marshalling (`DEFAULT_MARSHALLER = NoMarshaller`)
    - pluggable model loading (dill, joblib, selfserializing, custom) configured by
       `MODEL_ASSET_CLASSES` and `MODEL_CLASS`
    """


def as_tensor_dict_callable(
    tensor_callable: T.ModelInvoker[T.V, T.VorDict],
) -> (
    T.AsyncModelInvoker[T.VorDict, T.VorDict]
    | T.AsyncModelInvokerWithParams[T.VorDict, T.VorDict]
):
    """Expose a callable with tensor parameters as a dict callable."""
    parameters = inspect.signature(tensor_callable).parameters.values()

    async def _tensor_dict_callable(
        data: T.VorDict, **kwargs
    ) -> T.VorDict | tuple[T.VorDict, Parameters]:
        if not isinstance(data, dict):
            return tensor_callable(data)
        not_bound = {**data}
        positional_arguments = []
        keyword_arguments = {}
        for parameter in parameters:
            named_data = not_bound.pop(parameter.name, None)
            if named_data is None:
                named_data = kwargs.pop(parameter.name, None)
            if parameter.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            ):
                # undefaulted positional arguments
                # can use the 'main' argument as fallback
                if named_data is None and not _has_default(parameter):
                    named_data = not_bound.pop("main", None)
                positional_arguments.append(_require_default(named_data, parameter))
                continue
            if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                if "main" in not_bound:
                    positional_arguments.append(not_bound.pop("main"))
                continue
            if parameter.kind == inspect.Parameter.VAR_KEYWORD:
                keyword_arguments.update(kwargs)
                keyword_arguments.update(not_bound)
                not_bound = {}
                continue
            if parameter.kind == inspect.Parameter.KEYWORD_ONLY:
                if named_data is not None:
                    keyword_arguments[parameter.name] = named_data
                continue
        return tensor_callable(*positional_arguments, **keyword_arguments)

    return _tensor_dict_callable


_EMPTY_DEFAULT = inspect.Parameter("_", inspect.Parameter.KEYWORD_ONLY).default


def _has_default(parameter):
    return parameter.default is not _EMPTY_DEFAULT


def _require_default(value, parameter):
    if value is not None:
        return value
    if _has_default(parameter):
        return parameter.default
    raise ValueError(
        f'Model invocation has unbound "{parameter.name}" input without default.'
    )
