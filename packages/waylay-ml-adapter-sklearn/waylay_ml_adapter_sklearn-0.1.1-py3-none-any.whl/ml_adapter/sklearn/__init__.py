"""ML Adapter for sklearn."""

import importlib.metadata

from ml_adapter.base.assets.script import (
    default_plug_v1_script,
    default_webscript_script,
)
from ml_adapter.numpy import V1NumpyModelAdapter

__version__ = importlib.metadata.version("waylay-ml-adapter-sklearn")

SKLEARN_REQUIREMENTS = [
    *V1NumpyModelAdapter.DEFAULT_REQUIREMENTS,
    "scikit-learn",
    "waylay-ml-adapter-sklearn",
]


class V1SklearnPredictAdapter(V1NumpyModelAdapter):
    """ModelAdapter for sklearn models with a `predict` method."""

    model_method = "predict"
    DEFAULT_SCRIPT = {
        "webscripts": default_webscript_script,
        "plugs": default_plug_v1_script,
    }
    DEFAULT_REQUIREMENTS = SKLEARN_REQUIREMENTS


class V1SklearnPredictProbaAdapter(V1NumpyModelAdapter):
    """ModelAdapter for sklearn models with a `predict_proba` method."""

    model_method = "predict_proba"
    DEFAULT_SCRIPT = {
        "webscripts": default_webscript_script,
        "plugs": default_plug_v1_script,
    }
    DEFAULT_REQUIREMENTS = SKLEARN_REQUIREMENTS


__all__ = [
    "V1SklearnPredictAdapter",
    "V1SklearnPredictProbaAdapter",
]
