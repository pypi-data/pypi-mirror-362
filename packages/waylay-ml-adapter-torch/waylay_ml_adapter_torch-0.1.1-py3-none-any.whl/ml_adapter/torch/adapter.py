"""Torch ML adapter."""

import logging
from typing import Any, Self

import ml_adapter.api.types as T
import ml_adapter.base as A
import ml_adapter.base.model as M
import torch
from ml_adapter.api.data import v1 as V1
from ml_adapter.api.data.common import V1_PROTOCOL
from ml_adapter.base.assets import AssetsFolder, FunctionType
from ml_adapter.base.assets.script import (
    default_plug_v1_script,
    default_webscript_script,
)
from torch import nn

from .marshall import TorchTensor, V1TorchMarshaller

TorchModelInvoker = T.ModelInvoker[TorchTensor, TorchTensor]

# if True, new adapters will use the runtimes with preloaded torch libraries
USE_TORCH_RUNTIMES_DEFAULT = False

TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_LOAD_DOC = "https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-state-dict-recommended"

LOG = logging.getLogger(__name__)


class TorchModelAsset(M.ModelAsset[nn.Module]):
    """Model asset for pytorch models (fully serialized)."""

    PATH_INCLUDES = ["*.pt", "*.pth"]
    DEFAULT_PATH = "model.pt"

    async def load_content(self, **kwargs):
        """Load a dill model."""
        with open(self.location, "rb") as f:
            LOG.warning(
                "loading a serialized torch model from %s. "
                "Please prefer using model weights by setting a `model_path` "
                "ending in `weigths.pt(h)` (see %s).",
                self.location,
                TORCH_LOAD_DOC,
            )
            model = torch.load(f, weights_only=False)  # type: ignore
            # torch evaluation mode
            model.eval()
            model.to(TORCH_DEVICE)
            self.content = model

    async def save_content(self, **kwargs):
        """Save a dill model."""
        with open(self.location, "wb") as f:
            torch.save(self.content, f)


class TorchModelWeightsAsset(M.ModelAsset[nn.Module]):
    """Model asset for pytorch models (only weights serialized)."""

    PATH_INCLUDES = ["*weights.pt", "*weights.pth", "*Weights.pt", "*Weights.pth"]
    DEFAULT_PATH = "model_weights.pt"
    MODEL_CLASS: type[nn.Module] | None = None

    model_class: type[nn.Module]

    def __init__(
        self,
        parent: AssetsFolder,
        model_class: type[nn.Module] | None = None,
        **kwargs,
    ):
        """Create a model loading weights."""
        super().__init__(parent, **kwargs)
        model_class = model_class or self.MODEL_CLASS
        if not model_class:
            raise TypeError(
                'Loading a torch model using weights requires a "model_class" argument.'
            )
        self.model_class = model_class

    async def load_content(self, **kwargs):
        """Load a dill model."""
        with open(self.location, "rb") as f:
            LOG.info("loading torch model weights from %s", self.location)
            weights = torch.load(f, weights_only=True)  # type: ignore
            LOG.info("creating torch model with class %s", self.model_class.__name__)
            model = self.model_class()
            model.load_state_dict(weights)
            model.eval()
            model.to(TORCH_DEVICE)
            # torch evaluation mode
            self.content = model

    async def save_content(self, **kwargs):
        """Save a dill model."""
        model = self.content
        if model is None:
            return
        with open(self.location, "wb") as f:
            torch.save(model.state_dict(), f)


class V1TorchAdapter(
    A.ModelAdapterBase[
        TorchTensor, V1.V1Request, V1.V1PredictionResponse, TorchModelInvoker
    ]
):
    """Adapts a torch model with torch arrays as input and output.

    When initialized with a trained model (using a `model` parameter):
    * will store the model weights as `model_weights.pt`
      (alt: set the `model_path` parameter)
    * requires that the model class in a library or asset file
      (e.g. a class extending `torch.nn.Module` in an `mymodel.py` script asset)
      The generated server script will use this name as as `model_class`

    To load from a serialized model, use the `model_path` (default `model_weights.pt`)
    and `model_class` (no default).

    Alternatively, when the `model_path` does not have a `weights.pt` or `weights.pth`
    extension, the adapter will try to load it as a dill-serialized model.
    This is not recommended because of the brittleness of this serialization method
    with respect to versions.

    """

    DEFAULT_MARSHALLER = V1TorchMarshaller
    MODEL_ASSET_CLASSES = [TorchModelWeightsAsset, TorchModelAsset]
    DEFAULT_MODEL_PATH = "model_weights.pth"
    PROTOCOL = V1_PROTOCOL
    DEFAULT_SCRIPT = {
        "webscripts": default_webscript_script,
        "plugs": default_plug_v1_script,
    }
    TORCH_RUNTIME_REQUIREMENTS = [
        *A.PythonMLAdapter.DEFAULT_REQUIREMENTS,
        "waylay-ml-adapter-torch",
    ]
    TORCH_RUNTIMES = {
        "webscripts": "web-pytorch",
        "plugs": "plug-pytorch",
    }
    DEFAULT_REQUIREMENTS = [*TORCH_RUNTIME_REQUIREMENTS, "torch"]

    def __init__(self, *args, use_torch_runtimes=False, **kwargs):
        """Create a function adapter for pytorch models."""
        super().__init__(*args, **kwargs)
        self.use_torch_runtimes = use_torch_runtimes

    @property
    def invoker(self) -> T.ModelInvoker:
        """Natively invoke the torch model without gradients calculation."""
        return torch.no_grad(super().invoker)

    def default_requirements(self) -> list[str]:
        """Get the default requirements for this archive."""
        if self.use_torch_runtimes:
            return self.TORCH_RUNTIME_REQUIREMENTS
        return super().default_requirements()

    def default_runtime(self, function_type: FunctionType = "plugs") -> str:
        """Get the default runtime for this archive."""
        if self.use_torch_runtimes:
            return self.TORCH_RUNTIMES[function_type]
        return super().default_runtime(function_type)

    def _as_function(
        self, manifest: dict[str, Any], function_type: FunctionType
    ) -> Self:
        rt = manifest.get("runtime")
        if rt is not None and rt in self.TORCH_RUNTIMES.values():
            self.use_torch_runtimes = True
        return super()._as_function(manifest, function_type)


class V1TorchNoLoadAdapter(V1TorchAdapter):
    """Adapts a callable with torch arrays as input and output.

    This adapter does not manage the model as a standard asset.
    It relies on the `model` or `model_class` constructor arguments
    to define and load the model.
    When `model` is not provided, any `model_path` is passed as a constructor
    argument to `model_class` if the signature allows it.

    Note that if you internally rely on torch models, the model constructor is
    responsible for
    * setting that wrapped model to
     [evaluation mode](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval)
    * setting the model to the
    [correct device and/or dtype](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.to)
    (normally  to `"cuda" if torch.cuda.is_available() else "cpu"`)

    The model adapter will still enforce a
    [`torch.no_grad`](https://pytorch.org/docs/stable/generated/torch.no_grad.html#no-grad)
    context around model invocations.

    ```python

    def load_my_model(weights_file='my_weights.pt'):
        wrapped_model = AWrappedTorchModel()
        wrapped_model.load_state_dict(torch.load(weights_file))
        wrapped_model.eval()
        wrapped_model.to('cpu')
        return wrapped_model

    class MyTorchWrappingModel():
        def __init__(self, model_file):
            self.torch_model = load_my_model(model_file)

        # custom pre/postprocessing
        def __call__(self, x, y, z):
            # preprocess
            x = x + y + z
            result = this.torch_model(x)
            # postprocess
            return result[0]
    ```

    ```
    adapter = V1TorchNoLoadAdapter(model_class=MyTorchWrappingModel)
    ```

    If all you need is add pre- and post-processing of torch tensors,
    you can still use V1TorchAdapter to load the wrapped model,
    but might want to wrap the `__call__` method or set another _model_method_

    ```python
    class MyTorchModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            # ... initialize layers

        def forward(self, x):
            # ... inference

        # custom pre/postprocessing
        def __call__(self, x, y, z):
            # preprocess
            x = x + y + z
            result = super().__call__(x)
            # postprocess
            return result[0]
    ```
    """

    MODEL_ASSET_CLASSES = []
    DEFAULT_MODEL_PATH: str | None = None
