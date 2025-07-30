from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike

from . import Covariance


class CubicCovariance(Covariance):
	_params: ClassVar[dict[str, float]] = {
		"range": 1.0,
		"sill": 1.0,
		"nugget": 0.0,
	}

	def __call__(self, lag: ArrayLike) -> ArrayLike:
		# Formula: nugget + sill * (7*lag**2 - 35/4*lag**3 + 7/2*lag**5 - 3/4*lag**7)
		# 	if lag < range else  nugget + sill
		result = np.ones_like(lag)
		within_range = lag < self.range
		lag = lag[within_range]
		lag *= np.divide(1.0, self.range)
		lag2 = lag * lag
		result_in_range = 7.0 * lag2
		pow_lag = lag2 * lag  # lag ** 3
		result_in_range += (-8.75) * pow_lag  # -35 / 4
		pow_lag *= lag2  # lag ** 5
		result_in_range += 3.5 * pow_lag  # 7 / 2
		pow_lag *= lag2  # lag ** 7
		result_in_range += (-0.75) * pow_lag  # 3 / 4
		result[within_range] = result_in_range
		result *= self.sill
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

		Parameters
		----------
		lag : _type_
		    _description_
		var : _type_
		    _description_
		"""
		return np.max(lag) / 2, np.mean(var), 0
