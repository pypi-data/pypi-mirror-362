from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import curve_fit

from krigeo.covariance.variogram import variogram


class Covariance(ABC):
	_params: ClassVar[dict[str, float]] = {}

	def __init__(self, **params) -> None:
		"""
		Generates a covariance model.

		The model is composed of a set of parameters and a __call__() method to evaluate on lags.
		It provides a fit() classmethod to estimate parameters from an experimental sample.

		See: https://scikit-gstat.readthedocs.io/en/latest/reference/models.html

		Parameters
		----------
		**params : dict, optional
		    Parameters of the covariance model (range, sill, nugget, ...)

		Raises
		------
		ValueError
		    _description_
		"""

		for name in params:
			if name not in self._params:
				msg = f"invalid parameter '{name}'"
				raise ValueError(msg)
		self._params.update(params)

		# Monkey-Patch: wrap _params as class attributes
		self.__dict__ = self._params

	def __str__(self) -> str:
		s = f"{self.__class__.__name__}:"
		for k, v in self._params:
			s += f"\n\t{k}: {v}"
		return s

	@abstractmethod
	def __call__(self, lag: ArrayLike, dir: ArrayLike | None = None) -> ArrayLike:
		"""
		Computes the covariance of samples.

		Parameters
		----------
		lag : ArrayLike
		    Distance between samples.
		dir : Optional[ArrayLike], optional
		    Direction of the lags (needed for anisotropic covariance models), by default None

		Returns
		-------
		ArrayLike
		    Covariance value
		"""
		...

	@abstractmethod
	def guess_p0(self, lag, var): ...

	@classmethod
	def fit(
		cls,
		points: ArrayLike,
		values: ArrayLike | None = None,
		lag_max: float = np.inf,
		nbins: int | str = "auto",
	) -> tuple[Covariance, float]:
		"""
		Estimates the covariance model parameters from sample dataset.

		Parameters
		----------
		points : ArrayLike
		    Sample dataset to fit the model on.
		lag_max : float
		    Maximum distance between points to consider them in the computation
		nbins : int
		    Number of bins for the experimental variogram
		values : Optional[ArrayLike], optional
		    Values of the variable to estimate at points, by default None

		Returns
		-------
		Tuple[Covariance, float]
		    The covariance model and the metric of fit.
		"""
		# experimental variogram components
		lag, var = variogram(points, values=values, lag_max=lag_max, nbins=nbins)
		mask = ~np.isnan(var)
		lag, var = lag[mask], var[mask]
		if np.isnan(var).any():
			msg = "Some bins of the experimental variogram contain no data. Reduce number of bins or change lag_max."
			raise ValueError(msg)

		# wrap the model
		def curve_to_optimise(lags, *args):
			params = dict(zip(cls._params.keys(), args))
			return cls(**params)(lags)

		_lag, _var = np.max(lag), np.max(var)
		args, _ = curve_fit(
			curve_to_optimise,
			lag,
			var,
			bounds=(0, max(_lag, _var)),
			p0=cls.guess_p0(lag, var),
		)

		params = dict(zip(cls._params.keys(), args))
		model = cls(**params)

		# fitting metric: mean square error (MSE)
		fit = model(lag)
		metric = np.mean((var - fit) ** 2)

		return model, metric
