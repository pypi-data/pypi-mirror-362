from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike

from . import Drift


class GaussianDrift(Drift):
	_params: ClassVar[dict[str, float]] = {
		"range": None  # Distance above which attenuation > 95%. Defaults to 50% of fault's length.
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.range is None:
			self.range = 0.5 * self.fault.length

	def __call__(self, points: ArrayLike, force_side: int = 0) -> ArrayLike:
		lags = self.fault(points, clip=True)
		sigma = self.range / np.sqrt(2 * np.log(20))
		# lateral attenuation
		drifts = np.exp(-(lags**2) / (2 * sigma**2))
		# longitudinal attenuation
		if self.extent < np.inf:
			drifts *= self.attenuation(points)
		# invert sides
		return drifts * self.side(lags, force_side)
