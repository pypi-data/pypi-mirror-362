from ..drift import Drift
from .gaussian import GaussianDrift
from .heaviside import HeavisideDrift
from .linear import LinearDrift

models = {
	"linear": LinearDrift,
	"heaviside": HeavisideDrift,
	"gaussian": GaussianDrift,
}
