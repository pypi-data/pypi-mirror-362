from __future__ import annotations

import logging

import numpy as np
from numpy.typing import ArrayLike
from scipy.spatial.distance import pdist


def full_variogram(
	points: ArrayLike,
	values: ArrayLike = None,
	lag_max: float = np.inf,
) -> ArrayLike:
	"""
	Computes the experimental variogram from a sample dataset.

	Parameters
	----------
	points : ArrayLike
	    Points of the dataset
	values : ArrayLike, optional
	    Values of the variable to estimate at points. Defaults to points last coordinate.
	lag_max : float
	    Maximum distance between points to consider them in the computation

	Returns
	-------
	ArrayLike
	    Array of (x, y) points of the variogram
	"""
	if values is None:
		points, values = points[:, :-1], points[:, -1]
		logging.warning(
			"No values provided, using the points last coordinate as target variable!"
		)

	# get pairwise distance between points
	lags = pdist(points)
	# get pairwise indices
	i, j = np.triu_indices(len(values), k=1)

	# invalid too far away pairs
	if lag_max and lag_max < np.inf:
		valids = lags < lag_max
		lags, i, j = lags[valids], i[valids], j[valids]

	# get pairwise variance
	gamma = (values[i] - values[j]) ** 2

	return np.asarray(lags), np.asarray(gamma)


def variogram(
	points: ArrayLike,
	values: ArrayLike = None,
	lag_max: float = np.inf,
	nbins: int | str = "auto",
) -> ArrayLike:
	"""
	Computes the experimental variogram from a sample dataset.

	Parameters
	----------
	points : ArrayLike
	    Points of the dataset
	values : ArrayLike, optional
	    Values of the variable to estimate at points. Defaults to points last coordinate.
	lag_max : float
	    Maximum distance between points to consider them in the computation
	nbins : int,
	    Number of points of the experimental variogram to compute

	Returns
	-------
	ArrayLike
	    Array of (x, y) points of the variogram
	"""

	_lags, _gamma = full_variogram(points, values, lag_max)
	# build the histogram of variances
	bin_edges = np.histogram_bin_edges(_lags, nbins or "auto")
	lags, gamma = [], []
	for low, up in zip(bin_edges[:-1], bin_edges[1:]):
		lags.append((up + low) / 2.0)
		gamma.append(
			np.nanmean(
				np.select(
					[
						np.logical_and(
							_lags >= low,
							_lags < up,
						)
					],
					[_gamma],
					np.nan,
				)
			)
		)
	return np.asarray(lags), np.asarray(gamma)
