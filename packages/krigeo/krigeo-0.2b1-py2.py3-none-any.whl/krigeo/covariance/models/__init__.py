from ..covariance import Covariance
from .cubic import CubicCovariance
from .exponential import ExponentialCovariance
from .gaussian import GaussianCovariance
from .spherical import SphericalCovariance

models = {
	"exponential": ExponentialCovariance,
	"gaussian": GaussianCovariance,
	"spherical": SphericalCovariance,
	"cubic": CubicCovariance,
}
