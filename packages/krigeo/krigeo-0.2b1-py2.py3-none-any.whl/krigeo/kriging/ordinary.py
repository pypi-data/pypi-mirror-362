from functools import cached_property
from typing import Union

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .simple import SimpleKriging


class OrdinaryKriging(SimpleKriging):
	"""Generalization of the simple kriging for unknown expectation random field"""

	@cached_property
	def Ki(self):
		K = np.pad(super().Ki, (0, 1), "constant", constant_values=1)
		K[-1, -1] = 0
		return K

	def Ke(self, locations: ArrayLike) -> NDArray[np.float64]:
		return np.pad(
			super().Ke(locations), ((0, 1), (0, 0)), "constant", constant_values=1
		)

	def __call__(
		self, locations: ArrayLike, return_variance: bool = False
	) -> Union[tuple[ArrayLike, ArrayLike], ArrayLike]:
		locations = np.asarray(locations)
		# assert self.points.shape[-1] == locations.shape[-1]

		Ke = self.Ke(locations)
		weights = self.iK @ Ke
		weights, mu = weights[:-1, :], weights[-1, :]

		estimations = np.sum(weights.T * self.values, axis=-1)

		if return_variance:
			variance = self.Ki[0, 0] - np.sum(weights.T * Ke[:-1].T, axis=-1) - mu
			return estimations, np.abs(variance)
		return estimations
