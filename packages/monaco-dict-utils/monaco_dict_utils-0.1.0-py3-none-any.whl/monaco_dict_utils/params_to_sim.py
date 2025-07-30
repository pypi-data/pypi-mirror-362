"""Utilities for converting parameter dictionaries to Monaco simulations.

This module provides functions for converting parameter dictionaries into Monaco
simulation objects and outputs. It handles mapping distribution parameters,
constant values, and simulation outputs between dictionary and Monaco formats.

Functions:
    params_to_sim: Add input variables and constants to a simulation
    params_to_model: Create a model from factory function and parameters
    case_vals_to_dict: Convert case values to a parameter dictionary
    output_to_case: Convert model output to a Case object
    outvals_to_dict: Convert simulation output values to a dictionary
"""

import re
from collections.abc import Callable
from typing import Any

from monaco import Case, Sim

_CONST = "_constant"


def _key(k: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s_]", "", k).strip().lower().replace(" ", "_")


def params_to_sim(sim: Sim, invars: dict) -> Sim:
    """Add input variables and constants to a simulation.

    Args:
        sim: A Monaco Sim object to add inputs to
        invars: Dictionary mapping input names to distribution parameters

    Returns:
        The modified Sim object with inputs added

    The invars dictionary should contain entries mapping parameter names to either:
    1. Distribution specifications with 'dist' and 'params' keys
    2. Constant values with 'dist' set to '_constant'

    For distributions, the 'params' key should contain parameter values for the
    distribution. For constants, 'params' can be a single value or a dictionary
    of parameter values.

    Example:
        invars = {
            'x': {'dist': 'uniform', 'params': {'loc': 0, 'scale': 1}},
            'y': {'dist': '_constant', 'params': 5}
        }

    """
    for name, details in invars.items():
        if details["dist"] != _CONST:
            sim.addInVar(
                name=name,
                dist=details["dist"],
                distkwargs={k: v.value for k, v in details["params"].items()},
            )
        elif hasattr(details["params"], "items") and callable(
            details["params"].items,
        ):
            for k, v in details["params"].items():
                sim.addConstVal(name=k, val=v.value)
        elif hasattr(details["params"], "value"):
            sim.addConstVal(name=name, val=details["params"].value)
        else:
            sim.addConstVal(name=name, val=details["params"])
    return sim


def case_vals_to_dict(case: Case) -> tuple[dict[str, Any]]:
    """Convert case input values to a dictionary.

    Args:
        case: A Monaco Case object containing input values

    Returns:
        Tuple containing a dictionary mapping normalized parameter names to values

    The input values are normalized by converting to lowercase, removing special chars,
    and replacing spaces with underscores. Both input values and constant values from
    the case are included in the output dictionary.

    """
    return (
        {_key(k): v.val for k, v in case.invals.items()}
        | {_key(k): v for k, v in case.constvals.items()},
    )


def output_to_case(case: Case, output: dict) -> None:
    """Add output values to a simulation case.

    Args:
        case: A Monaco Case object to add outputs to
        output: Dictionary of output values to add

    The output values are added to the case with normalized names.
    Keys are converted to title case with underscores removed.
    For example, "time_savings" becomes "Time_Savings".

    """
    for k, v in output.items():
        case.addOutVal(name="_".join([w.capitalize() for w in k.split("_")]), val=v)


def params_to_model(model_factory: Callable, factory_vars: dict) -> Callable:
    """Convert model factory and parameters into a callable model.

    Args:
        model_factory: Factory function that creates the model
        factory_vars: Dictionary of variables to pass to model factory

    Returns:
        Configured model function ready to accept simulation parameters

    The factory_vars dict contains parameters needed to construct the model.
    Keys are normalized by converting to lowercase, removing special characters,
    and replacing spaces with underscores.

    """
    return model_factory(
        **{
            _key(k): v["params"].value if isinstance(v, dict) else v
            for k, v in factory_vars.items()
        },
    )


def outvals_to_dict(sim: Sim) -> dict:
    """Convert simulation output values to a dictionary.

    Args:
        sim: A Monaco Sim object that has been run

    Returns:
        Dictionary mapping outvar to the np array of the output values.

    """
    return {k: outvar.nums for k, outvar in sim.outvars.items()}
