"""Distribution definitions and utilities for the Bayesian engine."""

from typing import Dict, Any, Optional, Union
import numpy as np
import pymc as pm
import arviz as az


def create_distribution(
    distribution_type: str,
    name: str,
    **params
) -> Any:
    """Create a PyMC distribution based on type and parameters.
    
    Args:
        distribution_type: Type of distribution ('normal', 'beta', etc.)
        name: Name of the random variable
        **params: Distribution parameters
    
    Returns:
        PyMC distribution object
    
    Raises:
        ValueError: If distribution type is not supported
    """
    dist_map = {
        'normal': pm.Normal,
        'beta': pm.Beta,
        'gamma': pm.Gamma,
        'uniform': pm.Uniform,
        'exponential': pm.Exponential,
        'poisson': pm.Poisson,
        'bernoulli': pm.Bernoulli,
        'binomial': pm.Binomial,
        'categorical': pm.Categorical,
        'dirichlet': pm.Dirichlet,
        'multinomial': pm.Multinomial,
        'lognormal': pm.Lognormal,
        'studentt': pm.StudentT,
        'halfnormal': pm.HalfNormal,
        'weibull': pm.Weibull,
    }
    
    if distribution_type not in dist_map:
        raise ValueError(f"Unsupported distribution: {distribution_type}")
        
    return dist_map[distribution_type](name, **params)


def extract_posterior_stats(trace: az.InferenceData, var_name: str) -> Dict[str, Any]:
    """Extract summary statistics for a posterior variable.
    
    Args:
        trace: ArviZ InferenceData object containing posterior samples
        var_name: Name of the variable to extract
    
    Returns:
        Dictionary with posterior statistics
    """
    posterior = trace.posterior[var_name]
    
    # Get HDI (highest density interval)
    hdi = az.hdi(trace, var_names=[var_name])
    
    # Get ESS (effective sample size)
    ess = az.ess(trace, var_names=[var_name])
    
    # Get r_hat (convergence diagnostic)
    rhat = az.rhat(trace, var_names=[var_name])
    
    # Create result dictionary
    result = {
        "mean": float(posterior.mean().values),
        "std": float(posterior.std().values),
        "median": float(np.median(posterior.values)),
        "hdi_low": float(hdi[var_name].values[0]),
        "hdi_high": float(hdi[var_name].values[1]),
        "ess": float(ess[var_name].mean().values),
        "r_hat": float(rhat[var_name].mean().values)
    }
    
    return result