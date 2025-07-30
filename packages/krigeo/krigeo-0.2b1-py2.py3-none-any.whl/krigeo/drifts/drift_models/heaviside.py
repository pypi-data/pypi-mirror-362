import numpy as np
from numpy.typing import ArrayLike

from . import Drift


class HeavisideDrift(Drift):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def __call__(self, points: ArrayLike, force_side: int = 0) -> ArrayLike:
		lags = self.fault(points, clip=True)
		# drift lateral magnitude (constant)
		drifts = np.ones_like(lags, dtype=float)
		# attenuate longitudinally
		if self.extent < np.inf:
			drifts *= self.attenuation(points)
		# invert drift on sides
		return drifts * self.side(lags, force_side)
