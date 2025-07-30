# waylay-ml-adapter-torch

Provides the `ml_adapter.sklearn` module as [Waylay ML Adapter](https://docs.waylay.io/#/api/sdk/python?id=ml_adapter) for [pytorch](https://pytorch.org/).


## Installation
```
pip install waylay-ml-adapter-torch
```

The `torch` module is needed, but **NOT** declared as a package dependency, to leave the user full control over the way the (rather heavy) pytorch installation is done.
Use `pip install waylay-ml-adapter-torch[torch]` to include it.

You might want to install additional libraries such as `torchaudio` or `torchvision`.


## Usage
This _ML Adapter_ uses the standard torch mechanisms to [save and load models](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-and-loading-models) within a waylay _plugin_ or _webscript_.
The `model_path` argument defines the file name of the serialized model in the function archive:
* A `model_path` ending in `weights.pt` or `weights.pth` save/loads the model weights using its [state_dict](https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-state-dict-recommended).
  It is a recommended, more robust method, but requires you to also specifiy a `model_class`.
* Any other `model_path` with `.pt` or `.pth` suffix save/loads the [entire model](https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-entire-model).
  It implicitly saves (references to) the used model class. You'll have to make sure that all dependencies used are also included or declared in the archive. 
* You can also pass an instantiated the `model` directly to the adapter.


### Creating a model for a _webscript_
```python
from ml_adapter.torch import V1TorchAdapter

# assuming we save a AutoEncoder torch.nn.Module class in a `autoencoder.py` file
from autoencoder import AutoEncoder
model = AutoEncoder()
# ... train the model ...

# a local directory to prepare the webscript archive
ARCHIVE_LOC='~/webscripts/autoencoder-pytorch'
# use a `weights` model path to use _weights_ serialization
MODEL_PATH='autoencoder.weights.pt'

adapter = V1TorchAdapter(
    model=model,
    model_path='model-weights.pt',
    location=ARCHIVE_LOC,
)

# add our model script to the webscript archive
await adapter.add_script('autoencoder.py')
# write the archive
await adapter.save()
# inspect the archive:
list(adapter.assets)
#> [requirements.txt <ml_adapter.base.assets.python.PythonRequirementsAsset>,
#> main.py <ml_adapter.base.assets.python.PythonScriptAsset>,
#> model-weights.pt <ml_adapter.torch.adapter.TorchModelWeightsAsset>,
#> autoencoder.py <ml_adapter.base.assets.python.PythonScriptAsset>]
```

Upload the adapter archive as webscript using the [`ml_tool` SDK plugin](https://pypi.org/project/waylay-ml-adapter-sdk/)
```
from waylay.sdk import WaylayClient
client = WaylayClient.from_profile('staging')
ref = await client.ml_tool.create_webscript(adapter, name='MyAutoEncoder', version='0.0.1')
ref = await client.ml_tool.wait_until_ready(ref)
await client.ml_tool.test_webscript(ref, [2,3,4])
```

The generated code in `main.py` uses the following to load your model:
```python
MODEL_PATH = os.environ.get('MODEL_PATH', 'model-weights.pt')
MODEL_CLASS = os.environ.get('MODEL_CLASS', 'autoencoder.AutoEncoder')
adapter = V1TorchAdapter(model_path=MODEL_PATH, model_class=MODEL_CLASS)
```
You can modify that loading mechanism, e.g. by creating the model your self, and providing it as
```
adapter = V1TorchAdapter(model=model)
```


When you want additional processing before or after the model invocation that prevents
your model to be loadable by the default `torch.load` mechanisms, you can alternatively
use the `ml_adapter.torch.V1TorchNoLoadAdapter`. 

This _wrapper_ model class is then responsible for the loading of the model.


## Classes exported by `ml_adapter.torch`

The module `ml_adapter.torch` exports the following classes
    
### `V1TorchAdapter`
`ml_adapter.torch.adapter.V1TorchAdapter` extending `ml_adapter.base.adapter.ModelAdapterBase`
> Adapts a torch model with torch arrays as input and output.

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




### `V1TorchNoLoadAdapter`
`ml_adapter.torch.adapter.V1TorchNoLoadAdapter` extending `ml_adapter.torch.adapter.V1TorchAdapter`
> Adapts a callable with torch arrays as input and output.

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



### `V1TorchMarshaller`
`ml_adapter.torch.marshall.V1TorchMarshaller` extending `ml_adapter.base.marshall.v1.base.V1ValueOrDictRequestMarshallerBase`, `ml_adapter.base.marshall.v1.base.V1ValueOrDictResponseMarshallerBase`, `ml_adapter.torch.marshall.V1TorchNativeEncoding`
> Convert v1 payload from and to torch tensors.



## See also

* [waylay-ml-adapter-sklearn](https://pypi.org/project/waylay-ml-adapter-sklearn/) _ML adapter_ for [scikit-learn](https://scikit-learn.org/stable/) models.
* [waylay-ml-adapter-sdk](https://pypi.org/project/waylay-ml-adapter-sdk/) provides the `ml_tool` extension to the [waylay-sdk](https://pypi.org/project/waylay-sdk/)
* [waylay-ml-adapter-base](https://pypi.org/project/waylay-ml-adapter-base/) provides the basic _ML adapter_ infrastructure.
* [waylay-ml-adapter-api](https://pypi.org/project/waylay-ml-adapter-api/) defines the remote data interfaces.
