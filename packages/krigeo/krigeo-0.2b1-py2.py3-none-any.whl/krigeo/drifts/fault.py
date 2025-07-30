from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import ArrayLike


class Fault(ABC):
	points: ArrayLike = np.array([])

	@abstractmethod
	def __call__(self, points: ArrayLike, **kwargs) -> ArrayLike:
		"""
		Computes the signed distance to the fault.

		Parameters
		----------
		points : ArrayLike
		    n-by-m points coordinates.

		Returns
		-------
		ArrayLike
		    n-by-1 float array of signed distance.
		"""
		...

	@property
	@abstractmethod
	def length(self):
		"""The length of the fault (used for longitudinal attenuation)"""
		return np.inf

	@property
	def simplified_length(self):
		"""The length of the segment between fault extremities (used for longitudinal attenuation)"""
		return np.linalg.norm(self.points[0] - self.points[-1])

	@abstractmethod
	def longitude(self, points: ArrayLike, **kwargs) -> ArrayLike:
		"""
		Computes points (projection) longitudinal coordinates.

		Parameters
		----------
		points : ArrayLike
		    n-by-m points coordinates.

		Returns
		-------
		ArrayLike
		    n-by-1 float array of signed distance.
		"""
		...
