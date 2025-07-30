import numpy as np
from numpy.typing import ArrayLike

from krigeo.covariance.covariance import Covariance
from krigeo.covariance.models import models as MODELS


def fit_covariance_model(
	points: ArrayLike,
	values: ArrayLike = None,
	model: str = "auto",
	return_metric: bool = False,
	lag_max: float = np.inf,
	nbins: int | str = "auto",
) -> Covariance | tuple[Covariance, float]:
	"""
	Generates a Covariance object, from sample dataset.

	Parameters
	----------
	points : ArrayLike
	    Points of the data
	lag_max : float
	    Maximum distance between points to consider them in the computation
	nbins : int
	    Number of points of the experimental variogram to compute
	values : ArrayLike, optional
	    Values of the variable to estimate at points, by default None, takes the points last coordinates.
	model : str, optional
	    Covariance type to fit ('gaussian', 'exponential', 'cubic' or 'spherical'), by default "auto"
	return_metric : bool, optional
	    Return distance metric between fitted model and experimental variogram, by default False

	Returns
	-------
	Covariance
	    Fitted covariance model.
	"""
	if model.lower() == "auto":
		# loop over all known models and return the best fitting
		covariances, metrics = [], []
		for mdl in MODELS.values():
			covariance, metric = mdl.fit(
				points,
				values,
				nbins=nbins,
				lag_max=lag_max,
			)
			covariances.append(covariance)
			metrics.append(metric)
		idx = np.argmin(metrics)
		return (covariances[idx], metrics[idx]) if return_metric else covariances[idx]
	if model.lower() not in MODELS:
		msg = f"invalid model '{model}', must be one of {['auto', *list(MODELS)]}"
		raise ValueError(msg)
	covariance, metric = MODELS[model].fit(
		points,
		values,
		nbins=nbins,
		lag_max=lag_max,
	)
	return (covariance, metric) if return_metric else covariance
