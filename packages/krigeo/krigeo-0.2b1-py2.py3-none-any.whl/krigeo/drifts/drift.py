from abc import ABC, abstractmethod
from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike

from .fault import Fault


class Drift(ABC):
	fault: Fault
	_params: ClassVar[dict[str, float]] = {}  # use it to extend Drift parameters

	def __init__(
		self, fault: Fault, extent: float = 0, name: str = "", **params
	) -> None:
		"""
		Generates a drift model.

		A drift model represents the shape of the drift reject:
		    - is it longitudinally attenuated/infinite ?
		    - is the reject attenuated ? how ?
		    - etc ...

		The model is composed of a set of parameters and a __call__() method
		that computes the drift value relative to the distance to the fault (lag).

		Parameters
		----------
		fault : Fault
		    Fault associated with the drift.
		extent : float
		    Extent of the influence, defaults to the fault length
		name : str, optional
		    Name of the drift, by default ""
		**params : dict, optional
		    Drift model tunning parameters (model, range, ...). Defaults to {}.
		"""
		if not isinstance(fault, Fault):
			msg = f"invalid fault type '{type(fault)}'"
			raise TypeError(msg)
		self.fault = fault
		self.name = name
		for _ in params:
			if _ not in self._params:
				msg = f"invalid parameter '{_}'"
				raise ValueError(msg)
		self._params.update(params)
		# Monkey-Patch: wrap _params as class attributes
		self.__dict__.update(self._params)
		# defaults extent to fault length
		self.extent = extent or self.fault.length

	@abstractmethod
	def __call__(self, points: ArrayLike, force_side: int = 0) -> ArrayLike:
		"""
		Computes the relative reject at sampling points.

		Parameters
		----------
		points : ArrayLike
		    Sampling points coordinates.
		force_side : int, optional
		    Force the polarity on faults to override NaNs, by default 0

		Returns
		-------
		ArrayLike
		    Relative reject value
		"""
		...

	@classmethod
	def side(cls, lags: ArrayLike, force_side: int = 0):
		"""
		Handle points exactly on faults.

		Parameters
		----------
		lags : ArrayLike
		    Distance of a set of points to the fault;
		force_side : int, optional
		    Force the polarity on faults to override NaNs, by default 0

		Returns
		-------
		ArrayLike
		    Possible values : -1, 1, np.nan, depending on the side of the faults points are on
		"""
		sign = np.sign(lags)
		if force_side > 0:
			sign[sign == 0] += 1
		elif force_side < 0:
			sign[sign == 0] -= 1
		else:
			sign[sign == 0] = np.nan
		return sign

	def attenuation(self, points: ArrayLike):
		"""
		Longitudinally attenuates fault drift.

		Parameters
		----------
		points : ArrayLike
		    Sampling points coordinates.
		approximate : bool
		    Consider attenuation along segment between fault extremities or along exact fault trace, by default True

		Returns
		-------
		ArrayLike
		    Attenuation coefficients at points
		"""
		if self.extent < np.inf:
			x = self.fault.longitude(points, clip=False)
			x -= self.extent / 2.0  # center on fault
			sigma = (self.extent / 2.2) / np.sqrt(2 * np.log(20))
			return np.exp(-(x**2) / (2 * sigma**2))
		return np.ones(len(points), dtype=float)
