from .universal import UniversalKriging


class DualKriging(UniversalKriging):
	"""Dual kriging is similar to Ordinary Kriging.

	Note that it is faster by design but prevent the variance computation !
	"""

	# TODO: implement dual kriging (faster but without variance estimation)
	msg = "Work in progress"
	raise NotImplementedError(msg)
