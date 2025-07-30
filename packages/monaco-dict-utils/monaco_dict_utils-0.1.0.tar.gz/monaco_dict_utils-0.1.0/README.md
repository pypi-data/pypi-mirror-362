[![PyPI](https://img.shields.io/pypi/v/monaco-dict-utils.svg)](https://pypi.org/project/monaco-dict-utils/)
[![Lint and Typecheck](https://github.com/hbmartin/monaco-dict-utils/actions/workflows/lint.yml/badge.svg)](https://github.com/hbmartin/monaco-dict-utils/actions/workflows/lint.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/🐧️-black-000000.svg)](https://github.com/psf/black)

# Monaco Dictionary Utils

A Python library for easily bootstrapping Monaco Monte Carlo simulations with a dictionary-based workflow.

[See example notebook here](https://github.com/hbmartin/ai-roi-mcm-npv-marimo/blob/main/ai_roi_mcm_npv.py)

## Overview

Monaco Dictionary Utils provides a simplified interface for creating and running Monte Carlo simulations using the Monaco framework. It streamlines the process of setting up simulations by allowing you to define model factories, input parameters, and distributions using dictionary-based configuration.

## Features

- **Dictionary-based configuration**: Define simulations using simple dictionary structures
- **Model factory support**: Create models from factory functions with configurable parameters
- **Input variable management**: Handle both probabilistic distributions and constants
- **Output conversion**: Convert simulation results to easily accessible dictionary format
- **Parameter normalization**: Automatic parameter name normalization for consistency

## Installation

```bash
uv add monaco-dict-utils
```

## Requirements

- Python ≥ 3.11
- Monaco ≥ 0.16.0

## Quick Start

```python
from monaco_dict_utils import sim_factory, outvals_to_dict

# Define your model factory
def my_model_factory(param1, param2):
    def model(x, y):
        return {"result": x * param1 + y * param2}
    return model

# Configure simulation
factory_vars = {"param1": 2, "param2": 3}
invars = {
    "x": {"dist": "uniform", "params": {"loc": 0, "scale": 1}},
    "y": {"dist": "_constant", "params": 5}
}

# Create and run simulation
sim = sim_factory(
    name="my_simulation",
    model_factory=my_model_factory,
    factory_vars=factory_vars,
    invars=invars,
    ndraws=1000
)

sim.run()

# Convert outputs to dictionary
results = outvals_to_dict(sim)
```

## API Reference

#### `sim_factory(name, model_factory, factory_vars, invars, ndraws, *, verbose=True, debug=False)`

Create a Monte Carlo simulation from a model factory and parameters.

**Parameters:**
- `name` (str): Name of the simulation
- `model_factory` (Callable): Factory function that creates the model
- `factory_vars` (dict): Dictionary of variables to pass to model factory
- `invars` (dict): Dictionary mapping input names to distribution parameters
- `ndraws` (int): Number of Monte Carlo draws to simulate
- `verbose` (bool, optional): Whether to print simulation progress. Defaults to True.
- `debug` (bool, optional): Whether to run in debug mode. Defaults to False.

**Returns:**
- `Sim`: Configured Monaco Sim object ready to run simulations

**Example:**
```python
sim = sim_factory(
    name="example_sim",
    model_factory=my_factory,
    factory_vars={"param": 10},
    invars={"x": {"dist": "normal", "params": {"loc": 0, "scale": 1}}},
    ndraws=5000
)
```

#### `outvals_to_dict(sim)`

Convert simulation output values to a dictionary.

**Parameters:**
- `sim` (Sim): A Monaco Sim object that has been run

**Returns:**
- `dict`: Dictionary mapping output variable names to numpy arrays of output values

**Example:**
```python
results = outvals_to_dict(sim)
# results = {"Result": array([1.23, 4.56, ...]), "Other_Output": array([...])}
```

## Input Variables Configuration

The `invars` dictionary supports two types of inputs:

### 1. Probabilistic Distributions

For random variables, specify a distribution and its parameters:

```python
invars = {
    "temperature": {
        "dist": "normal",
        "params": {"loc": 20, "scale": 5}
    },
    "pressure": {
        "dist": "uniform", 
        "params": {"loc": 10, "scale": 2}
    }
}
```

### 2. Constants

For constant values, use the special `_constant` distribution:

```python
invars = {
    "gravity": {
        "dist": "_constant",
        "params": 9.81
    },
    "config": {
        "dist": "_constant",
        "params": {"setting1": 100, "setting2": 200}
    }
}
```

## Parameter Normalization

The library automatically normalizes parameter names by:
- Converting to lowercase
- Removing special characters
- Replacing spaces with underscores

For example: `"Air Temperature"` becomes `"air_temperature"`

## Output Formatting

Output values are automatically formatted with:
- Title case conversion
- Underscore preservation
- Example: `"time_savings"` becomes `"Time_Savings"`

