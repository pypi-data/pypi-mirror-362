from itertools import cycle
from typing import Optional, Union

from numpy.typing import ArrayLike

from .drift import Drift
from .drift_models import models as DRIFTS
from .fault import Fault
from .fault_models import models as FAULTS
from .network import DriftsNetwork


def build_fault(points: ArrayLike, **kwargs) -> Fault:
	"""
	Builds a Fault object

	Parameters
	----------
	points : ArrayLike
	    Points of the fault trace.
	**kwargs : dict, optional

	Returns
	-------
	Fault
	"""
	geometry = kwargs.pop("geometry", "vertical")
	if geometry.lower() not in FAULTS:
		msg = f"invalid fault geometry '{geometry}', must be one of {list(FAULTS)}"
		raise ValueError(msg)
	return FAULTS[geometry](points, **kwargs)


def build_drift(fault: Fault, model: str = "heaviside", **params) -> Drift:
	"""
	Builds a Drift object

	Parameters
	----------
	fault : Fault
	    Fault associated to the drift
	model : str, optional
	    Type of drift, by default "heaviside"
	**params : dict, optional
	    Parameters corresponding to the chosen type of drift.

	Returns
	-------
	Drift
	    _description_
	"""
	if model.lower() not in DRIFTS:
		msg = f"invalid drift model '{model}', must be one of {list(DRIFTS)}"
		raise ValueError(msg)
	return DRIFTS[model](fault, **params)


def build_network(
	faults: list[ArrayLike],
	models: Union[str, list[str]] = "heaviside",
	*,
	params: Optional[Union[dict, list[dict]]] = None,
	relations: ArrayLike = None,
	buffer: float = 0.0,
) -> DriftsNetwork:
	"""
	Builds a DriftsNetwork object from a list of fault traces.

	Parameters
	----------
	faults : List[ArrayLike]
	    List of fault traces
	models : Union[str, List[str]], optional
	    Type of drifts (same type for all drift or list od types), by default "heaviside"
	params : Union[dict, List[dict]], optional
	    Drifts parameters (unique dictionary or list of dictionaries), by default {}
	relations : ArrayLike, optional
	    Matrix of relations between faults, by default None
	buffer : float, optional
	    If no relations is given, used to infer relations, by default 0.0

	Returns
	-------
	DriftsNetwork
	"""
	if params is None:
		params = {}
	faults = [build_fault(f) if not isinstance(f, Fault) else f for f in faults]
	if isinstance(models, str):
		models = cycle([models])
	if isinstance(params, dict):
		params = cycle([params])
	drifts = [build_drift(f, m, **p) for f, m, p in zip(faults, models, params)]
	return DriftsNetwork(drifts, buffer=buffer, relations=relations)
