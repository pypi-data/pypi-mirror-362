"""Numpy ML adapter."""

import ml_adapter.api.types as T
import ml_adapter.base as A
import numpy.typing as npt
from ml_adapter.api.data import v1 as V1
from ml_adapter.api.data.common import V1_PROTOCOL
from ml_adapter.base.assets.script import (
    default_plug_v1_script,
    default_webscript_script,
)
from ml_adapter.base.model.dill import DillModelAsset
from ml_adapter.base.model.joblib import JoblibModelAsset
from ml_adapter.base.model.serialize import SelfSerializingModelAsset

from .marshall import V1NumpyMarshaller

NumpyModelInvoker = T.ModelInvoker[npt.ArrayLike, npt.ArrayLike]


NUMPY_REQUIREMENTS = [
    *A.PythonMLAdapter.DEFAULT_REQUIREMENTS,
    "numpy>=1.25.0",
    "waylay-ml-adapter-numpy",
    "dill",
    "joblib",
]


class V1NumpyModelAdapter(
    A.ModelAdapterBase[
        npt.ArrayLike, V1.V1Request, V1.V1PredictionResponse, NumpyModelInvoker
    ]
):
    """Adapts a callable with numpy arrays as input and output.

    Supports dill, joblib or selfserializing model assets.
    """

    DEFAULT_MARSHALLER = V1NumpyMarshaller
    MODEL_ASSET_CLASSES = [DillModelAsset, JoblibModelAsset, SelfSerializingModelAsset]
    DEFAULT_MODEL_PATH: str | None = "model.dill"
    PROTOCOL = V1_PROTOCOL
    DEFAULT_REQUIREMENTS = NUMPY_REQUIREMENTS
    DEFAULT_SCRIPT = {
        "webscripts": default_webscript_script,
        "plugs": default_plug_v1_script,
    }


class V1NumpyNoLoadAdapter(V1NumpyModelAdapter):
    """Adapts a callable with numpy arrays as input and output.

    This adapter does not manage the model as a standard asset.
    Relies on the `model` or `model_class` constructor arguments
    to define the model.
    When `model` is not provided, any `model_path` is passed as a constructor
    argument to `model_class` if the signature allows it.
    """

    MODEL_ASSET_CLASSES = []
    DEFAULT_MODEL_PATH: str | None = None
