import contextlib
from typing import Any

import numpy as np
from numpy.typing import ArrayLike

from .drift import Drift
from .fault import Fault


class FaultsNetwork(list):
	"""
	List of Fault objects. Allows to generate a matrix of relations between these faults.
	Is used by DriftsNetwork.
	"""

	def __init__(
		self, faults: list[Fault], *, buffer: float = 0.0, relations: ArrayLike = None
	) -> None:
		super().__init__(faults)

		n = len(self)
		if n < 2:
			msg = "Needs at least 2 fault to build a network"
			raise ValueError(msg)
		if not all(isinstance(e, Fault) for e in self):
			raise TypeError(faults)

		if relations is not None:
			relations = np.asarray(relations)
			if relations.size == n**2:
				self.relations = relations.reshape((n, n))
			elif relations.size == (n**2, n * (n - 1) // 2):
				self.relations = relations
			else:
				msg = "Incompatible 'relations' vector size."
				raise ValueError(msg)
		else:
			self.infer_relations(buffer)

	def __setattr__(self, __name: str, __value: Any) -> None:
		with contextlib.suppress(AttributeError):
			del self.relations
		return super().__setattr__(__name, __value)

	def pairs(self, return_indices: bool = False):
		"""
		Returns iterator on pairs of faults (and optionally indices) in the network.

		Parameters
		----------
		return_indices : bool, optional
		    Return pairs indices, by default False

		Yields
		------
		    Iterator on pairs of faults
		"""
		for i, fault in enumerate(self):
			for j, other in enumerate(self[i + 1 :]):
				if return_indices:
					j += i + 1  # noqa: PLW2901
					yield (i, j), (fault, other)
				else:
					yield (fault, other)

	def indices(self):
		for ij, _ in self.pairs(return_indices=True):
			yield ij

	def infer_relations(self, buffer: float = 0.0) -> ArrayLike:
		"""
		Infers relations matrix.

		Parameters
		----------
		buffer : float, optional
		    Tolerance distance (to deal with cases where faults do not stop exactly on other), by default 0.0

		Returns
		-------
		ArrayLike
		    Possible values of coef i,j :
		        * -1 : fault i stops on negative side of fault j
		        * 1 : fault i stops on positive side of fault j
		        * 0 : faults i and j cross each other
		"""

		matrix = np.zeros((len(self), len(self)), dtype=np.int8)
		for i, fault in enumerate(self):
			dist = np.asarray([other(fault.points) for other in self]).squeeze()
			matrix_line = np.select(
				[
					np.all(dist + buffer >= 0.0, axis=-1),
					np.all(dist - buffer <= 0.0, axis=-1),
				],
				[1, -1],
				0,
			)
			matrix[i] = matrix_line
		np.fill_diagonal(matrix, 0)
		self.relations = self.clean_matrix(matrix)
		return self.relations

	def clean_matrix(self, matrix):
		"""
		Post-process of matrix of relations.
		If faults i and j stop on opposite sides of fault k, then k acts as a screen and faults i and j do not influence each other.

		Parameters
		----------
		matrix : ArrayLike
		    Matrix of relations between faults. Manually defined or returned by infer_relations

		Returns
		-------
		cleaned_matrix : ArrayLike
		    Post-processed matrix.
		"""
		cleaned_matrix = np.copy(matrix)

		to_check_pos = np.column_stack(np.where(matrix == 1))
		to_check_neg = np.column_stack(np.where(matrix == -1))

		for row, column in to_check_pos:
			opposite = matrix[..., column] == -1
			cleaned_matrix[row, opposite] = 0

		for row, column in to_check_neg:
			opposite = matrix[..., column] == 1
			cleaned_matrix[row, opposite] = 0

		return cleaned_matrix

	@property
	def matrix(self):
		"""
		Square-form relations matrix.

		Returns
		-------
		    ArrayLike: Possible values of coef i,j :
		        * -1 : fault i stops on negative side of fault j
		        * 1 : fault i stops on positive side of fault j
		        * 0 : faults i and j cross each other
		"""
		return self.relations.reshape((len(self), len(self)))


class DriftsNetwork(list):
	"""
	List of Drift objects.
	Allows to call all drifts at once on a set of points, taking into account the relations between the faults of the network.
	"""

	faults: FaultsNetwork = []  # noqa: RUF012

	def __init__(self, drifts: list[Drift], **kwargs) -> None:
		super().__init__(drifts)
		n = len(self)
		if n < 2:
			msg = "Needs at least 2 drifts to build a network"
			raise ValueError(msg)
		if not all(isinstance(e, Drift) for e in self):
			raise TypeError(drifts)

		self.faults = FaultsNetwork([d.fault for d in drifts], **kwargs)

	def __call__(self, points: ArrayLike, force_side: int = 0) -> ArrayLike:
		"""
		Calls all drift functions on evaluation points, taking into account the relations between faults.

		Parameters
		----------
		points : ArrayLike
		    Points where to evaluate drifts.
		force_side : int, optional
		    Force side of points exactly on faults, by default 0

		Returns
		-------
		ArrayLike, shape(len(self), len(points))
		    Array of drifts computed on points.
		"""
		drifts = [drift(points, force_side) for drift in self]
		corrected_drifts = np.copy(drifts)
		# nullify masked drift terms
		for (i, j), side in zip(
			np.ndindex((len(self), len(self))), self.faults.relations.flat
		):
			# WARNING: we do not recompute distance to fault, it assumes
			#   np.sign(drift(pt)) == np.sign(fault(pt))
			if side == 0:
				# both drifts play
				continue
			if side < 0:
				# drift[j] is below drift[i]
				#   > nullify terms of drifts[j] that are above drift[i]
				corrected_drifts[i][drifts[j] > 0] = 0
			elif side > 0:
				# drift[j] is above drift[i]
				#   > nullify terms of drifts[j] that are below drift[i]
				corrected_drifts[i][drifts[j] < 0] = 0
		return np.asarray(corrected_drifts)

	@property
	def relations(self):
		return self.faults.relations

	@property
	def matrix(self):
		return self.faults.matrix
