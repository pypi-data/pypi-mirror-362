from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike

from . import Drift


class LinearDrift(Drift):
	_params: ClassVar[dict[str, float]] = {
		"order": 1  # order of the lateral attenuation
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def __call__(self, points: ArrayLike, force_side: int = 0) -> ArrayLike:
		lags = self.fault(points, clip=False)
		# drift lateral magnitude (linear)
		drifts = np.divide(1, lags**self.order)
		# attenuate longitudinally
		if self.extent < np.inf:
			drifts *= self.attenuation(points)
		# invert drift on sides
		return drifts * self.side(lags, force_side)
