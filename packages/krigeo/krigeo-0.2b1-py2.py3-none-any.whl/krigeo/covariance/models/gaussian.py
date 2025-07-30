from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike

from . import Covariance


class GaussianCovariance(Covariance):
	_params: ClassVar[dict[str, float]] = {
		"range": 1.0,
		"sill": 1.0,
		"nugget": 0.0,
		"scale": 1.0,
	}

	def __call__(self, lag: ArrayLike) -> ArrayLike:
		# Formula: nugget + sill * (1 - np.exp(-((scale * lag / range) ** 2))
		result = np.divide(self.scale, self.range) * lag
		result *= result
		np.negative(result, out=result)
		np.exp(result, out=result)
		result -= 1.0
		result *= -self.sill
		if self.nugget != 0.0:
			result += self.nugget
		return result

	@staticmethod
	def guess_p0(lag, var):
		"""
		Autoguess of parameters.
		    range = half of the domain
		    sill = mean of var
		    nugget = 0
		    scale = 1.0


		Parameters
		----------
		lag : _type_
		    _description_
		var : _type_
		    _description_
		"""
		return np.max(lag) / 2, np.mean(var), 0, 1.0
