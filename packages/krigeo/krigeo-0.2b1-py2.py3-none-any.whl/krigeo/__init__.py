try:
	from krigeo.__version__ import (
		__version__,
		__version_tuple__,
		version,
		version_tuple,
	)
except ImportError:
	__version__ = version = None
	__version_tuple__ = version_tuple = ()

from .covariance import covariance_models, fit_covariance_model, variogram
from .drifts import Drift, Fault, build_drift, build_fault, build_network
from .kriging import OrdinaryKriging, UniversalKriging
