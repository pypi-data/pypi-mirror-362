# Bayesian MCP

A Model Calling Protocol (MCP) server for Bayesian reasoning, inference, and belief updating. This tool enables LLMs to perform rigorous Bayesian analysis and probabilistic reasoning.

## Features

- 🧠 **Bayesian Inference**: Update beliefs with new evidence using MCMC sampling
- 📊 **Model Comparison**: Compare competing models using information criteria
- 🔮 **Predictive Inference**: Generate predictions with uncertainty quantification
- 📈 **Visualization**: Create visualizations of posterior distributions
- 🔌 **MCP Integration**: Seamlessly integrate with any LLM that supports MCP

## Installation

### Development Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/wrenchchatrepo/bayesian-mcp.git
cd bayesian-mcp
pip install -e .
```

### Requirements

- Python 3.9+
- PyMC 5.0+
- ArviZ
- NumPy
- Matplotlib
- FastAPI
- Uvicorn

## Quick Start

### Starting the Server

```bash
# Run with default settings
python bayesian_mcp.py

# Specify host and port
python bayesian_mcp.py --host 0.0.0.0 --port 8080

# Set log level
python bayesian_mcp.py --log-level debug
```

The server will start and listen for MCP requests on the specified host and port.

## API Usage

The Bayesian MCP server exposes several functions through its API:

### 1. Create Model

Create a new Bayesian model with specified variables.

```python
# MCP Request
{
    "function_name": "create_model",
    "parameters": {
        "model_name": "my_model",
        "variables": {
            "theta": {
                "distribution": "normal",
                "params": {"mu": 0, "sigma": 1}
            },
            "likelihood": {
                "distribution": "normal",
                "params": {"mu": "theta", "sigma": 0.5},
                "observed": [0.1, 0.2, 0.3, 0.4]
            }
        }
    }
}
```

### 2. Update Beliefs

Update model beliefs with new evidence.

```python
# MCP Request
{
    "function_name": "update_beliefs",
    "parameters": {
        "model_name": "my_model",
        "evidence": {
            "data": [0.1, 0.2, 0.3, 0.4]
        },
        "sample_kwargs": {
            "draws": 1000,
            "tune": 1000,
            "chains": 2
        }
    }
}
```

### 3. Make Predictions

Generate predictions using the posterior distribution.

```python
# MCP Request
{
    "function_name": "predict",
    "parameters": {
        "model_name": "my_model",
        "variables": ["theta"],
        "conditions": {
            "x": [1.0, 2.0, 3.0]
        }
    }
}
```

### 4. Compare Models

Compare multiple models using information criteria.

```python
# MCP Request
{
    "function_name": "compare_models",
    "parameters": {
        "model_names": ["model_1", "model_2"],
        "metric": "waic"
    }
}
```

### 5. Create Visualization

Generate visualizations of model posterior distributions.

```python
# MCP Request
{
    "function_name": "create_visualization",
    "parameters": {
        "model_name": "my_model",
        "plot_type": "trace",
        "variables": ["theta"]
    }
}
```

## Examples

The `examples/` directory contains several examples demonstrating how to use the Bayesian MCP server:

### Linear Regression

A simple linear regression example to demonstrate parameter estimation:

```bash
python examples/linear_regression.py
```

### A/B Testing

An example of Bayesian A/B testing for conversion rates:

```bash
python examples/ab_test.py
```

## Supported Distributions

The Bayesian engine supports the following distributions:

- `normal`: Normal (Gaussian) distribution
- `lognormal`: Log-normal distribution
- `beta`: Beta distribution
- `gamma`: Gamma distribution
- `exponential`: Exponential distribution
- `uniform`: Uniform distribution
- `bernoulli`: Bernoulli distribution
- `binomial`: Binomial distribution
- `poisson`: Poisson distribution
- `deterministic`: Deterministic transformation

## MCP Integration

This server implements the Model Calling Protocol, making it compatible with a wide range of LLMs and frameworks. To use it with your LLM:

```python
import requests

response = requests.post("http://localhost:8000/mcp", json={
    "function_name": "create_model",
    "parameters": {
        "model_name": "example_model",
        "variables": {...}
    }
})

result = response.json()
```

## License

MIT

## Credits

Based on concepts and code from the Wrench AI framework.