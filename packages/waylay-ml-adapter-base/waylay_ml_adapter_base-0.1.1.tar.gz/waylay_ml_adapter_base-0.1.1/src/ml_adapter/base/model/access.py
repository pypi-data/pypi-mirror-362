"""Model asset holder."""

import importlib
import inspect
from typing import Generic, Self, cast

import ml_adapter.api.types as T
from ml_adapter.base.assets.base import Asset

from ..assets import WithAssets
from .base import ModelAsset
from .dill import DillModelAsset
from .joblib import JoblibModelAsset
from .serialize import SelfSerializingModelAsset

ModelAssetTypeList = list[type[ModelAsset]]


class WithModel(WithAssets, Generic[T.MI]):
    """Holder of model assets.

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
    """

    MODEL_ASSET_CLASSES = [DillModelAsset, JoblibModelAsset, SelfSerializingModelAsset]
    DEFAULT_MODEL_PATH: str | None = "model.dill"
    MODEL_CLASS: type[T.MI] | None = None

    _model: T.MI | None = None  # model if not managed by an asset
    _model_path: str | None = None  # model path if not default
    _model_class: type | None = None  # model construtor if not an asset
    _model_is_dir: bool = False

    def __init__(
        self,
        model: T.MI | None = None,
        model_path: str | None = None,
        model_class: type[T.MI] | str | None = None,
        is_dir: bool = False,
        **kwargs,
    ):
        """Register a model asset.

        Parameters
        ----------
        model :  T.MI (model instance)
            A model instance
        model_path : str
            The asset path to or from which the model istance is serialized.
        model_class: type | str
            Sets the class of the model instance.
        is_dir: bool
            Whether the model_path is a directory.
        **kwargs:
            Passed on to parent constructor:
            - location: path of the assets root directory

        """
        super().__init__(**kwargs)
        self.assets.asset_classes.extend(self.MODEL_ASSET_CLASSES)
        self._model_path = model_path
        model_class = _model_class_for(model_class, model, self.MODEL_CLASS)
        self._model_class = model_class
        self._model_is_dir = is_dir
        self._init_model_asset(model_class=model_class)
        if model:
            self.model = model

    @property
    def model_class(self) -> type[T.MI] | None:
        """Return the current or supported model class.

        This is either:
            * the `model_class` constructor argument
            * the class of the `model` instance constructor argument
            * a default `MODEL_CLASS` set on the adapter class
        """
        if self._model_class:
            return self._model_class
        try:
            clazz = self.model.__class__
            if _is_allowed_model_clazz(clazz):
                return clazz
        except ValueError:
            pass
        if self.MODEL_CLASS:
            return self.MODEL_CLASS
        return None

    @property
    def model_path(self) -> str | None:
        """Model path."""
        if self._model_path:
            return self._model_path
        if self.DEFAULT_MODEL_PATH:
            return self.DEFAULT_MODEL_PATH
        if len(self.MODEL_ASSET_CLASSES) == 0:
            return None
        patterns = ",".join(
            set(f"'{p}'" for ac in self.MODEL_ASSET_CLASSES for p in ac.PATH_INCLUDES)
        )
        raise AttributeError(
            "No default model_path provided. "
            f"Please provide a path that matches any of {patterns}"
        )

    def _init_model_asset(self, model_class: type[T.MI] | None) -> ModelAsset | None:
        model_path = self.model_path
        if model_path is None:
            return None
        model_asset_class = self.assets.asset_class_for(
            model_path, is_dir=self._model_is_dir
        )
        if model_asset_class is None:
            return None
        return cast(
            ModelAsset,
            self.assets.add(
                model_asset_class,
                model_path,
                model_class=model_class,
            ),
        )

    @property
    def model_asset(self) -> ModelAsset | None:
        """The asset holding the model instance."""
        model_asset = self.assets.get(asset_type=ModelAsset)
        if model_asset is not None:
            return model_asset

        # lazy init
        return self._init_model_asset(self._model_class or self.MODEL_CLASS)

    @property
    def model(self) -> T.MI:
        """Get the model instance."""
        if self._model is not None:
            return self._model
        model_asset = self.model_asset
        if model_asset is not None:
            return model_asset.model
        if self._model_class is not None:
            return self._init_model_from_class()
        raise ValueError("no model available")

    def _init_model_from_class(self) -> T.MI:
        if self._model_class is None:
            raise ValueError("no model class available")
        kwargs = {}
        if self.model_path:
            # if there is a positional path, use it to bind `model_path`
            cstr_param = next(
                (
                    p
                    for p in inspect.signature(self._model_class).parameters.values()
                    if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                ),
                None,
            )
            if cstr_param:
                kwargs = {cstr_param.name: self.model_path}
        model = self._model_class(**kwargs)
        self.model = model
        return model

    @model.setter
    def model(self, model: T.MI):
        """Set the model instance."""
        if model is not None and _is_allowed_model_clazz(model.__class__):
            self._model_class = model.__class__
        model_asset = self.model_asset
        if model_asset is None:
            self._model = model
        else:
            model_asset.model = model

    async def load(
        self,
        *asset_classes: type[Asset],
        model_class: type[T.MI] | str | None = None,
        **kwargs,
    ) -> Self:
        """Load and assure that model is present."""
        prev_model = self._model
        model_class = load_class(model_class) or self._model_class
        loaded = await super().load(*asset_classes, model_class=model_class, **kwargs)
        # assert model present
        if self.model_asset is None or self.model_asset.model is None:
            self._model = prev_model
        return loaded


def load_class(spec: str | type | None) -> type | None:
    """Load a class by fully qualified module and class name."""
    if not isinstance(spec, str):
        return spec
    spec_els = spec.split(".")
    module_path = ".".join(spec_els[:-1])
    class_name = spec_els[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def class_fqn(clazz: type) -> str:
    """Render the fully qualified class name."""
    return f"{clazz.__module__}.{clazz.__name__}"


def _is_allowed_model_clazz(clazz: type) -> bool:
    """Return true if we can set the 'model_class' in the adapter to this value."""
    return clazz.__module__ not in ["builtins", "__main__"]


def _model_class_for(fqn_or_clazz, instance, default):
    clazz = load_class(fqn_or_clazz)
    if clazz:
        return clazz
    if instance and _is_allowed_model_clazz(instance.__class__):
        return instance.__class__
    return default
