"""Utilities for creating Monaco simulations from model factories.

This module provides functions for creating Monaco simulations from model factory
functions and parameter dictionaries. It handles setting up the simulation with
appropriate input variables, constants, and processing functions.

Functions:
    sim_factory: Create a Monte Carlo simulation from a model factory and parameters
"""

from collections.abc import Callable

from monaco import Sim, SimFunctions

from .params_to_sim import (
    case_vals_to_dict,
    output_to_case,
    params_to_model,
    params_to_sim,
)


def sim_factory(  # noqa: PLR0913
    name: str,
    model_factory: Callable,
    factory_vars: dict,
    invars: dict,
    ndraws: int,
    *,
    verbose: bool = True,
    debug: bool = False,
) -> Sim:
    """Create a Monte Carlo simulation from a model factory and parameters.

    Args:
        name: Name of the simulation
        model_factory: Factory function that creates the model
        factory_vars: Dictionary of variables to pass to model factory
        invars: Dictionary mapping input names to distribution parameters
        ndraws: Number of Monte Carlo draws to simulate
        verbose: Whether to print simulation progress
        debug: Whether to run in debug mode

    Returns:
        Configured Monaco Sim object ready to run simulations

    The factory_vars dict contains parameters needed to construct the model.
    The invars dict specifies the input distributions and parameters for the simulation.

    """
    model = params_to_model(model_factory, factory_vars)
    sim = Sim(
        name=name,
        ndraws=ndraws,
        fcns={
            SimFunctions.PREPROCESS: case_vals_to_dict,
            SimFunctions.RUN: lambda params: (model(**params),),
            SimFunctions.POSTPROCESS: output_to_case,
        },
        debug=debug,
        verbose=verbose,
    )
    params_to_sim(sim, invars)
    return sim
