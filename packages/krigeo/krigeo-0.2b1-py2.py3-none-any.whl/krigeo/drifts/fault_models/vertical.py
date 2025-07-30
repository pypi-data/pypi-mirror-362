import numpy as np
from numpy.typing import ArrayLike
from scipy.spatial.distance import cdist

from . import Fault


class VerticalFault(Fault):
	"""
	Defines a vertical fault from 2D points (trace on topography).

	Object is callable on any point and returns the signed distance to itself.
	"""

	def __init__(
		self,
		vertices: ArrayLike,
		reverse: bool = False,
	) -> None:
		"""
		Parameters
		----------
		vertices : ArrayLike. Shape (n,d)
		    Ordered vertices of the polyline representing the fault. Takes only the first two dimensions into account.
		"""
		vertices = np.asarray(vertices, dtype=float)
		assert vertices.ndim == 2, (
			f"Invalid vertices, must be a n-by-m 2D array, not: {vertices.ndim}D"
		)
		n, d = vertices.shape
		assert n >= 2, f"Invalid vertices, must have at least 2 points: {n} found"
		assert d >= 2, f"Invalid vertices, must have at least 2 dimensions: {d} found"
		if reverse:
			vertices = vertices[::-1]
		self.points = vertices[:, :2]
		self.vectors = np.diff(self.points, axis=0)
		self.norms = np.linalg.norm(self.vectors, axis=-1)

	### Required stuff

	@property
	def length(self):
		return np.sum(self.norms)

	def __call__(self, points: ArrayLike, clip: bool = True):
		"""
		Computes euclidean signed distance from points to closest segment.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    n-by-2 array of points coordinates to evaluate on.
		clip : bool, optional
		    TODO, by default True

		Returns
		-------
		ArrayLike, shape(n,)
		    Signed distance between points and fault
		"""
		return self.distance_to_closest_segment(points, clip=clip)

	def longitude(self, points: ArrayLike, clip: bool = False) -> ArrayLike:
		"""
		Computes curvilinear positions of projections of points on fault.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    n-by-2 array of points coordinates to evaluate on.
		clip : bool, optional
		    clip distance on [0, length], by default False

		Returns
		-------
		ArrayLike, shape(n,)
		    Positions of projections of points
		"""
		index, alpha, *_ = self.get_closest_segment(points, return_distance=False)
		longitude = np.asarray(
			[np.sum(self.norms[:i]) + a * self.norms[i] for i, a in zip(index, alpha)]
		)
		return np.clip(longitude, 0, self.length) if clip else longitude

	### Non-required stuff

	def __len__(self):
		return len(self.vectors)

	@staticmethod
	def parse_points(points: ArrayLike) -> ArrayLike:
		"""
		Formats points into a n-by-2 shape (dismiss extra dimensions)

		Parameters
		----------
		points : ArrayLike, shape(n, d)
		    n-by-d array of points coordinates to evaluate on.

		Returns
		-------
		ArrayLike, shape (n, 2)
		"""
		return np.asanyarray(points, dtype=float)[..., :2].reshape(-1, 2)

	# piecewise operations (one to many)

	def distance_to_points(self, points: ArrayLike) -> ArrayLike:
		"""
		Computes distance from points to each vertex.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points coordinates to evaluate on.

		Returns
		-------
		ArrayLike, shape (n, m)
		    n-by-m array of distances, with m the number of vertices in fault.
		"""
		points = self.parse_points(points)
		return cdist(points, self.points)

	def distance_to_midpoints(self, points: ArrayLike) -> ArrayLike:
		"""
		Computes distance from points to each segment center.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points coordinates to evaluate on.

		Returns
		-------
		ArrayLike, shape (n, m)
		    n-by-m array of distances with m the number of segments in fault.
		"""
		points = self.parse_points(points)
		return cdist(points, self.points[:-1] + self.vectors / 2.0)

	def distance_to_segments(self, points: ArrayLike) -> ArrayLike:
		"""
		Computes euclidean signed distance from points to each segment.

		Parameters
		----------
		points : ArrayLike, shape(n, d)
		    Points coordinates to evaluate on.

		Returns
		-------
		ArrayLike, shape (n, m)
		    n-by-m array of distances with m the number of segments in fault.
		"""
		points = self.parse_points(points)
		_, dist = self.project_on_segments(points, return_distance=True)
		return dist

	def project_on_segments(
		self, points: ArrayLike, return_distance: bool = True
	) -> ArrayLike:
		"""
		Orthogonally projects points on each segment of the fault trace.

		Parameters
		----------
		points : ArrayLike, shape (n, 2)
		    n-by-2 array of points coordinates to evaluate on.
		return_distance : bool, optional
		    Return distance between points and their projections, by default True

		Returns
		-------
		ArrayLike
		    Returns two or three arrays, depending on return_distance :
		        - projected points, shape (n, n_segments, 2)
		        - position of projections on the segment (between 0 and 1), shape (n, n_segments)
		        - (optional) distance between points and their projections, shape (n, n_segments)
		"""
		proj = np.empty((len(points), len(self), 2), dtype=float)
		alpha = np.empty((len(points), len(self)), dtype=float)

		v = points - self.points[:-1, np.newaxis]
		dot = (
			v[..., 0] * self.vectors[..., 0, np.newaxis]
			+ v[..., 1] * self.vectors[..., 1, np.newaxis]
		) / (self.norms[..., np.newaxis] ** 2)
		alpha = np.swapaxes(np.clip(dot, 0.0, 1.0), 0, 1)
		p_x = self.points[:-1, 0] + alpha * self.vectors[..., 0]
		p_y = self.points[:-1, 1] + alpha * self.vectors[..., 1]
		proj = np.stack((p_x, p_y), axis=-1)

		if return_distance:
			w = np.swapaxes(points[:, np.newaxis, :] - proj, 0, 1)
			distance = np.linalg.norm(w, axis=-1)
			polarity = (
				self.vectors[..., 0, np.newaxis] * w[..., 1]
				- self.vectors[..., 1, np.newaxis] * w[..., 0]
			)
			distance[polarity < 0] *= -1

			return proj, alpha, np.swapaxes(distance, 0, 1)
		return proj, alpha

	# selective operations (one to one)

	def get_closest_point(self, points: ArrayLike, return_distance: bool = False):
		"""
		Selects closest vertex for each point.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points to evaluate on.
		return_distance : bool, optional
		    Return distance between points and closest vertices, by default False

		Returns
		-------
		ArrayLike, shape (2, n) or (3, n) if return_distance
		    Indices of closest vertices, closest vertices and distance between points and closest vertices if return_distance
		"""
		dist = self.distance_to_points(points)
		index = np.argmin(dist, axis=-1)
		if return_distance:
			return (
				index,
				self.points[index],
				np.take_along_axis(dist, index.reshape((-1, 1)), axis=-1),
			)
		return index, self.points[index]

	def get_closest_midpoint(self, points: ArrayLike, return_distance: bool = False):
		"""
		Selects closest segment centers for each point.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points to evaluate on.
		return_distance : bool, optional
		    Return distance between points and closest segment centers, by default False

		Returns
		-------
		ArrayLike, shape (2, n) or (3, n) if return_distance
		    Indices of closest segment centers, closest segment centers and distance between points and closest segment centers if return_distance
		"""
		dist = self.distance_to_midpoints(points)
		index = np.argmin(dist, axis=-1)
		midpoints = self.points[:-1] + self.vectors / 2.0
		if return_distance:
			return (
				index,
				midpoints[index],
				np.take_along_axis(dist, index.reshape((-1, 1)), axis=-1),
			)
		return index, midpoints[index]

	def get_closest_segment(self, points: ArrayLike, return_distance: bool = False):
		"""
		Selects closest segment for each point.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points to evaluate on.
		return_distance : bool, optional
		    Return distance between points and closest segment, by default False

		Returns
		-------
		ArrayLike, shape (2, n) or (3, n) if return_distance
		    Returns two or three arrays :
		    - index of closest segment, shape (n,)
		    - position of projection on this segment, shape (n,)
		    - (optional) signed distance between points and projection, shape (n,)
		"""
		points = self.parse_points(points)
		# Project points onto each segment
		proj, alpha, dist = self.project_on_segments(points, return_distance=True)
		index = np.argmin(np.abs(dist), axis=-1)
		proj = self.parse_points(
			np.take_along_axis(proj, index.reshape((-1, 1, 1)), axis=1).squeeze()
		)
		temp_alpha = np.take_along_axis(
			alpha, index.reshape((-1, 1)), axis=-1
		).squeeze()

		# Case where alpha(closest projected point) = 1. (except if last segment)
		to_change = np.logical_and(
			temp_alpha == 1.0, np.logical_not(index == len(self.vectors) - 1)
		)

		# Compute dot product with previous (A->B) and next (B->C) vertex (normalized) (point projects on B)
		ab = self.vectors[index[to_change]] / self.norms[index[to_change], np.newaxis]
		bc = (
			self.vectors[index[to_change] + 1]
			/ self.norms[index[to_change] + 1, np.newaxis]
		)

		# print(points, to_change.shape, proj.shape)
		bx = points[to_change] - proj[to_change]

		dot_a = ab[..., 0] * bx[..., 0] + ab[..., 1] * bx[..., 1]
		dot_c = bc[..., 0] * bx[..., 0] + bc[..., 1] * bx[..., 1]

		# Change indexes
		to_change[to_change] = -dot_a < dot_c
		index[to_change] += 1

		dist = np.take_along_axis(dist, index.reshape((-1, 1)), axis=-1)
		alpha = np.take_along_axis(alpha, index.reshape((-1, 1)), axis=-1)
		if return_distance:
			return index, alpha, dist
		return index, alpha

	# distance helpers (one to one)

	def distance_to_closest_point(self, points: ArrayLike) -> ArrayLike:
		"""
		Computes distance from points to the fault closest vertex.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points to evaluate on.

		Returns
		-------
		ArrayLike, shape (n,)
		    Distance from points to the fault closest vertice.
		"""
		return self.get_closest_point(points, return_distance=True)[-1]

	def distance_to_closest_midpoint(self, points: ArrayLike) -> ArrayLike:
		"""
		Computes distance from points to the fault closest midpoint.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points to evaluate on.

		Returns
		-------
		ArrayLike, shape (n,)
		    Distance from points to the fault closest midpoint.
		"""
		return self.get_closest_midpoint(points, return_distance=True)[-1]

	def distance_to_closest_segment(
		self,
		points: ArrayLike,
		clip: bool = True,  # noqa: ARG002
	) -> ArrayLike:
		"""
		Computes distance from points to the fault closest segment.

		Parameters
		----------
		points : ArrayLike, shape (n, d)
		    Points to evaluate on.
		clip : bool, optional
		    TODO, by default True

		Returns
		-------
		ArrayLike, shape (n,)
		    Signed distance from points to the fault closest segment.
		"""
		# TODO: allow no_clip to get distance on infinite faults
		return self.get_closest_segment(points, return_distance=True)[-1]
