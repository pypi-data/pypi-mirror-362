# waylay-ml-adapter-base

Provides the `ml_adapter.base` module for the [Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) solution.

To use an _ML Adapter_ in a Waylay _plugin_ or _webscript_, use the adapter relevant to your machine learning framework:
* [waylay-ml-adapter-numpy](https://pypi.org/project/waylay-ml-adapter-numpy/) for generic models that use [numpy](https://numpy.org/) data representation
* [waylay-ml-adapter-sklearn](https://pypi.org/project/waylay-ml-adapter-sklearn/) for [scikit-learn](https://scikit-learn.org/stable/) models.
* [waylay-ml-adapter-torch](https://pypi.org/project/waylay-ml-adapter-torch/) for [pytorch](https://pytorch.org/) models.

This `waylay-ml-adapter-base` module provides the framework for these adapters.
Only if you would need to create an adapter utility for another
framework, you would install this module separately:

```
pip install waylay-ml-adapter-base
```


## Classes exported by `ml_adapter.base`

The module `ml_adapter.base` exports the following classes
    
### `PythonMLAdapter`
`ml_adapter.base.assets.python_ml.PythonMLAdapter` extending `ml_adapter.base.assets.python.PythonFunctionAdapter`
> Base adapter for a python ML function.

Adds methods to intialize the _manifest_ and _script_
for a python  _plugin_ or _webscript_.

* `as_webscript()` initializes the manifest
    and script for a _webscript_ that uses an ML Adapter.
* `as_plug()` initializes the manifest and script for
    a rule _plugin_ that uses an ML Adapter.



### `PythonFunctionAdapter`
`ml_adapter.base.assets.python.PythonFunctionAdapter` extending `ml_adapter.base.assets.manifest.WithManifest`
> Adapter for python based plugs or webscripts.

* `requirements` handles the dependency file (at `requirements.txt`)
* `lib` handles the libraries that are uploaded with
   the function archive itself. (at `lib/*.tar.gz`)
* `main_script` handles the main script of the function (`main.py`)
* `scripts` handles other utility scripts of the function (`*.py`)



### `NodeFunctionAdapter`
`ml_adapter.base.assets.node.NodeFunctionAdapter` extending `ml_adapter.base.assets.manifest.WithManifest`
> Adapter for node based plugs or webscripts.

* `package` handles the project file (at `package.json`)
* `main_script` handles the main script of the function (`index.js` or `index.ts`)
* `scripts` handles other utility scripts of the function (`*.js`,`*.ts`)



### `WithManifest`
`ml_adapter.base.assets.manifest.WithManifest` extending `ml_adapter.base.assets.mixin.WithAssets`
> Mixin for a configuration that has a waylay _function_ manifest file.

Adds methods to manage the function _manifest_ of a waylay _plugin_ or _webscript_.
* `manifest` returns the manifest asset of the function archive
    at `plug.json` or `webscript.json`.



### `ModelAdapter`
`ml_adapter.base.adapter.ModelAdapter`
> Model Adapter base.

Provides the basic contract for exposing
a model to a waylay _plugin_ or _webscript_.
* Delegates to a `marshaller` to map the remote,
  json-compatible python data structures
  from and to the native tensor data structures for the ML framework.
* Delegates to a `invoker` to find the model method to be called.
* The `call` method maps remote requests and invokes the model method.
* The `call_remote` method tests the round trip serialization, encoding
  native data request to remotable and back before invoking `call`.



### `TensorModelAdapter`
`ml_adapter.base.adapter.TensorModelAdapter` extending `ml_adapter.base.adapter.ModelAdapter`
> Model adapter that uses (dicts of) tensors as inputs and outputs.

Requests are mapped to the model invocation using named parameters,
falling back to mapping the "main" entry to the first positional parameter.



### `ModelAdapterBase`
`ml_adapter.base.adapter.ModelAdapterBase` extending `ml_adapter.base.adapter.TensorModelAdapter`, `ml_adapter.base.assets.python_ml.PythonMLAdapter`, `ml_adapter.base.model.access.WithModel`
> Generic model adapter for plugs and webscripts.

- supports creation of waylay webscript and plug functions
- pluggable tensor marshalling (`DEFAULT_MARSHALLER = NoMarshaller`)
- pluggable model loading (dill, joblib, selfserializing, custom) configured by
   `MODEL_ASSET_CLASSES` and `MODEL_CLASS`



### `WithAssets`
`ml_adapter.base.assets.mixin.WithAssets`
> Mixin for a configuration backed by assets.

Manages _assets_ of the the _plugin_ or _webscript_.

Used read-only within a deployed _adapter_ to e.g. load the model definition.

Used read/write within the `ml_tool` to edit
the assets of a _plugin_ or _webscript_.



### `WithOpenapi`
`ml_adapter.base.assets.openapi.WithOpenapi` extending `ml_adapter.base.assets.mixin.WithAssets`
> Mixin for a configuration that has an openapi description.

Adds methods to a `WithAssets` adapter to manage the
openapi description of waylay _plugin_ or _webscript_.

* `openapi` returns an asset of type `OpenApiAsset` (normally at `openapi.json`)




### `WithModel`
`ml_adapter.base.model.access.WithModel` extending `ml_adapter.base.assets.mixin.WithAssets`
> Holder of model assets.

Adds methods to a `WithAssets` adapter to manage the model instance.
A model can either be:
* given as `model` in the constructor of the adapter
* loaded from `model_path` in the assets
* loaded with a `model_class` (using an optional `model_path`)

The `MODEL_ASSET_CLASSES` configured on the adapter
define the methods to load a model.
Defaults are
* `DillModelAsset` ("*.dill", "*.pkl", "*.pickle" files)
* `JoblibModelAsset` ("*.joblib", "*.joblib.gz" files)
* `SelfSerializingModelAsset` ("*.sav" files)

If no `MODEL_ASSET_CLASSES` are configured, the model can only
be set by the contructor (using the `model` or `model_class` parameters)



### `SelfSerializingModelAsset`
`ml_adapter.base.model.serialize.SelfSerializingModelAsset` extending `ml_adapter.base.model.base.ModelAsset`
> Model asset with own serialization methods.

Reads/writes the model from `model.sav` using the `save` and `load` methods
defined on the `model_class`.



### `DillModelAsset`
`ml_adapter.base.model.dill.DillModelAsset` extending `ml_adapter.base.model.base.ModelAsset`
> Model asset for dill-serialized models.

Reads/writes the model from paths like `model.dill`, `model.pkl`, `model.pickle`
using [dill](https://pypi.org/project/dill/) serialisation.



### `JoblibModelAsset`
`ml_adapter.base.model.joblib.JoblibModelAsset` extending `ml_adapter.base.model.base.ModelAsset`
> Model asset with joblib serialization.

Reads/writes the model from `model.joblib` or `model.joblib.gz`
using [joblib](https://pypi.org/project/joblib/) serialisation.



### `Marshaller`
`ml_adapter.base.marshall.base.Marshaller` extending `ml_adapter.base.marshall.base.RequestMarshaller`, `ml_adapter.base.marshall.base.ResponseMarshaller`
> Abstract base class to marshall inference requests and responses.

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



