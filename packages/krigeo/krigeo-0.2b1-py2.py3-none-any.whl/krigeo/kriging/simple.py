import logging
from functools import cached_property
from typing import Any, Union

import numpy as np
from numpy.typing import ArrayLike
from scipy.spatial.distance import cdist, pdist, squareform

from krigeo.covariance import Covariance, fit_covariance_model


class SimpleKriging:
	"""Simple kriging estimator ... KISS inspired.

	Designed as a "20 minutes top" implementation of simple kriging estimator,
	leveraging pythonic cached properties and numpy vectorization.

	Basically, the kriging estimator can be written as :
		`Ze(y) = sum(W(y).z)` for `W(y) = iK@Ke`
	With:
		- `x`   : location of known values
		- `y`   : location of (unknown) sampling values
		- `z`   : studied variable (known values)
		- `Z()` : random function associated with `z`
		- `Ze()`: estimator of `Z`
		- `W()` : kriging weights
		- `iK`  : inverted variable covariance matrix (covariance of known values locations pairwise distances)
		- `Ke`  : covariance of sampling locations with known values locations

	see: https://en.wikipedia.org/wiki/Kriging

	"""

	def __init__(
		self,
		points: ArrayLike,
		values: Union[ArrayLike, None] = None,
		covariance: Union[str, Covariance] = "auto",
		cache: bool = True,
		**kwargs,
	):
		"""
		Generates a simple kriging estimator.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
			n-by-d array of the d-dimensional locations of the n known values.
		lag_max : float
			Maximum distance between points to consider them in the computation of the variogram
		nbins : int
			Number of points of the experimental variogram to compute the variogram
		values : Union[ArrayLike, None], optional
			n-by-1 known values. Defaults to the last dimension of `points` if None
		covariance : Union[str, Covariance], optional
			The covariance function/model as `f(lag) = Cov(lag)`, by default "auto"
		cache : bool, optional
			Flag to cache known data covariance inverse matrix, by default True
		"""
		if values is None:
			self.points, self.values = points[:, :-1], points[:, -1]
			logging.warning(
				"No value provided, kriged variable is inferred as the points last coordinate !"
			)
		else:
			assert len(values) == len(points), "points/values length mismatch"
			self.points = np.asarray(points)
			self.values = np.asarray(values)

		if isinstance(covariance, str):
			covariance = fit_covariance_model(
				self.points,
				values=self.values,
				model=covariance,
				**kwargs,
			)
		self.covariance = covariance

		if cache:  # pre-cache computing needs for later evaluation
			self.iK  # noqa: B018

	# DO NOT DELETE: it flushes the cached properties when kriging parameters change !
	def __setattr__(self, __name: str, __value: Any) -> None:
		"""Invalidates cached properties when data changes"""

		if __name == "points" and __name in self.__dict__:
			del self.__dict__["lags"]

		if __name in ("points", "covariance", "drifts"):
			if "Ki" in self.__dict__:
				del self.__dict__["Ki"]
			if "iK" in self.__dict__:
				del self.__dict__["iK"]

		return super().__setattr__(__name, __value)

	def Ke(self, locations: ArrayLike) -> ArrayLike:
		"""
		Covariance vector between known points and points to estimate

		Parameters
		----------
		locations : ArrayLike, shape (n, d)
			Points to estimate

		Returns
		-------
		ArrayLike
		"""
		return self.covariance(cdist(self.points, locations))

	def weights(self, locations: ArrayLike) -> ArrayLike:
		"""
		Kriging weights for estimation sampling sites, by solving kriging system.

		Parameters
		----------
		locations : ArrayLike, shape (n, d)
			Points to estimate

		Returns
		-------
		ArrayLike, shape (m,)
			m-by-1 array of kriging weights, with m the number of known points.
		"""
		# Note: unused in practice (see __call__), but kept as it could be useful
		return self.iK @ self.Ke(locations)

	@cached_property
	def lags(self):
		"""
		Wrapper around scipy pairwise distance.
		See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
		"""
		return pdist(self.points)

	@cached_property
	def Ki(self):
		"""Known data covariance matrix"""
		Ki = squareform(self.covariance(self.lags))
		np.fill_diagonal(Ki, 0.0)
		return Ki

	@cached_property
	def iK(self):
		"""Known data inverted covariance matrix"""
		return np.linalg.inv(self.Ki)

	def __call__(
		self, locations: ArrayLike, return_variance: bool = False
	) -> Union[tuple[ArrayLike, ArrayLike], ArrayLike]:
		"""
		Solves kriging system at estimation points.

		Parameters
		----------
		locations : ArrayLike, shape (n, d)
			Points to estimate
		return_variance : bool, optional
			Return variance of estimation, by default False

		Returns
		-------
		ArrayLike
			estimation or (estimation, variance) if return_variance
		"""
		locations = np.asarray(locations)
		assert self.points.shape[1] == locations.shape[1]

		Ke = self.Ke(locations)
		weights = self.iK @ Ke
		estimations = np.sum(weights.T * self.values, axis=-1)

		if return_variance:
			variance = self.Ki[0, 0] - np.sum(weights.T * Ke.T, axis=-1)
			return estimations, np.abs(variance)
		return estimations
