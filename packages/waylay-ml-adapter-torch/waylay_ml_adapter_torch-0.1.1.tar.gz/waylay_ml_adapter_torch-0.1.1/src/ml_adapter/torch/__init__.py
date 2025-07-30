"""ML Adapter for torch."""

import importlib.metadata

from .adapter import V1TorchAdapter, V1TorchNoLoadAdapter
from .marshall import V1TorchMarshaller

__version__ = importlib.metadata.version("waylay-ml-adapter-torch")

__all__ = ["V1TorchAdapter", "V1TorchNoLoadAdapter", "V1TorchMarshaller"]
