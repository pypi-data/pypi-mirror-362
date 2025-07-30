"""ML Adapter for numpy."""

import importlib.metadata

from .adapter import V1NumpyModelAdapter, V1NumpyNoLoadAdapter
from .marshall import V1NumpyMarshaller

__version__ = importlib.metadata.version("waylay-ml-adapter-numpy")

__all__ = ["V1NumpyModelAdapter", "V1NumpyMarshaller", "V1NumpyNoLoadAdapter"]
