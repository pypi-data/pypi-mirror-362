import logging
from collections.abc import Iterable
from functools import cached_property
from typing import Callable, Union

import numpy as np
from numpy.typing import ArrayLike, NDArray

from krigeo.drifts import DriftsNetwork

from .ordinary import OrdinaryKriging
from .simple import SimpleKriging


class UniversalKriging(SimpleKriging):
	"""Generalization of the Ordinary Kriging with drifts, also known as Kriging with External Drift."""

	def __init__(
		self,
		points: ArrayLike,
		values: Union[ArrayLike, None] = None,
		covariance: Union[str, Callable[[ArrayLike], ArrayLike]] = "auto",
		drifts: Union[Iterable[Callable], DriftsNetwork] = None,
		cache: bool = True,
		**kwargs,
	):
		"""
		Generates a Universal kriging system, that is callable on any set of points.

		Parameters
		----------
		points : ArrayLike
		    Points of sample dataset
		lag_max : float
		    Maximum distance between points to consider them in the computation
		nbins : int
		    Number of points of the experimental variogram to compute
		values : Union[ArrayLike, None], optional
		    Values of sample dataset, by default None, takes points last coordinates as kriging values
		covariance : Union[str, Callable[[ArrayLike], ArrayLike]], optional
		    Covariance model, by default "auto"
		drifts : Union[Iterable[Callable], DriftsNetwork], optional
		    Drift functions, either DriftsNetwork or list of Callables (with the form 'f(points)'), by default None
		cache : bool, optional
		    Cache covariance matrix, by default True
		"""
		self.drifts = drifts
		if self.drifts is None:
			logging.warning(
				"No drifts provided : used ordinary kriging instead of universal kriging"
			)
			self.ord = OrdinaryKriging(
				points,
				values=values,
				covariance=covariance,
			)
		else:
			try:
				self.drift_terms = drifts(points).squeeze()
			except Exception:
				self.drift_terms = np.asarray([d(points) for d in drifts]).squeeze()

				if self.drift_terms.ndim == 1:
					self.drift_terms = self.drift_terms.reshape(1, -1)

			self.drifts = np.asarray(drifts, dtype=object)[
				self.mask_drifts_with_missing_data()
			]

			super().__init__(points, values, covariance, cache, **kwargs)

	def Ke(self, locations) -> NDArray[np.float64]:
		try:
			terms = self.drifts(locations)
		except Exception:
			terms = np.asarray([d(locations)[np.newaxis] for d in self.drifts])

		Ke = np.pad(
			super().Ke(locations), ((0, 1), (0, 0)), "constant", constant_values=1.0
		)
		for t in terms:
			Ke = np.concatenate((Ke, t.reshape(1, len(locations))), axis=0)
		return Ke

	@cached_property
	def Ki(self):
		K = np.pad(super().Ki, (0, 1), "constant", constant_values=1.0)
		K[-1, -1] = 0
		for i in range(len(self.drifts)):
			K = np.concatenate(
				(
					K,
					np.pad(
						self.drift_terms[i, np.newaxis],
						((0, 0), (0, i + 1)),
						"constant",
						constant_values=0.0,
					),
				),
				axis=0,
			)
			K = np.concatenate(
				(
					K,
					np.pad(
						self.drift_terms[i, np.newaxis],
						((0, 0), (0, i + 2)),
						"constant",
						constant_values=0.0,
					).T,
				),
				axis=1,
			)
		return K

	def __call__(
		self, locations: ArrayLike, return_variance: bool = False
	) -> Union[tuple[ArrayLike, ArrayLike], ArrayLike]:
		locations = np.asarray(locations)

		if self.drifts is None:  # No drifts : use ordinary kriging
			return self.ord(locations)

		Ke = self.Ke(locations)
		weights = self.iK @ Ke

		estimations = np.sum(
			weights[: -(len(self.drifts) + 1), :].T * self.values, axis=-1
		)

		if return_variance:
			variance = self.Ki[0, 0] - np.sum(weights.T * Ke.T, axis=-1)
			return estimations, np.abs(variance)

		return estimations

	def mask_drifts_with_missing_data(self) -> ArrayLike:
		"""
		Deletes drift functions where all drifts of data points is null. Avoids having a singular covariance matrix.

		Returns
		-------
		ArrayLike
		    Indexes of drifts that should be kept for kriging.
		"""
		missing_fault_data = np.all(
			np.abs(np.asarray(self.drift_terms)) < 0.05, axis=-1
		)

		if np.count_nonzero(missing_fault_data) > 0:
			msg = f"Missing data inside fault scope for faults {np.where(missing_fault_data)}. These faults are not taken into account for kriging."
			logging.warning(msg)
			assert np.count_nonzero(missing_fault_data) < len(self.drift_terms), (
				"No drift can be computed from data."
			)

			to_keep = np.invert(missing_fault_data)
			# Update drift_terms
			self.drift_terms = self.drift_terms[to_keep]
			return to_keep

		return np.full(len(self.drift_terms), True)
