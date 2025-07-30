"""Core Bayesian engine implementation."""

import logging
from typing import Dict, List, Any, Tuple, Optional, Callable, Union

import pymc as pm
import numpy as np
import arviz as az

from .distributions import create_distribution, extract_posterior_stats

logger = logging.getLogger(__name__)

class BayesianEngine:
    """Core engine for probabilistic reasoning using PyMC.
    
    This engine manages Bayesian models, performs belief updating with
    new evidence, and provides interfaces for model comparison and
    predictive inference.
    """
    
    def __init__(self):
        """Initialize the Bayesian engine."""
        self.belief_models = {}
        logger.info("Bayesian Engine initialized")
    
    def create_model(self, model_name: str, variables: Dict[str, Dict]) -> None:
        """Create a Bayesian model with specified variables.
        
        Args:
            model_name: Unique identifier for the model
            variables: Dictionary defining model variables and their priors
                Format: {
                    'var_name': {
                        'type': 'continuous'|'binary'|'categorical',
                        'prior_mean': float, # for continuous
                        'prior_std': float,  # for continuous
                        'prior_prob': float, # for binary
                        'categories': List,  # for categorical
                        'prior_probs': List  # for categorical
                    }
                }
        """
        with pm.Model() as model:
            # Create model variables based on config
            model_vars = {}
            for var_name, var_config in variables.items():
                if var_config['type'] == 'continuous':
                    model_vars[var_name] = pm.Normal(
                        var_name,
                        mu=var_config.get('prior_mean', 0),
                        sigma=var_config.get('prior_std', 1)
                    )
                elif var_config['type'] == 'binary':
                    model_vars[var_name] = pm.Bernoulli(
                        var_name,
                        p=var_config.get('prior_prob', 0.5)
                    )
                elif var_config['type'] == 'categorical':
                    model_vars[var_name] = pm.Categorical(
                        var_name,
                        p=var_config.get('prior_probs', None),
                        categories=var_config.get('categories')
                    )
                # Add more distribution types as needed
            
            # Store the model for future use
            self.belief_models[model_name] = {
                'model': model,
                'vars': model_vars
            }
            
            logger.info(f"Created Bayesian model: {model_name} with variables: {list(variables.keys())}")
    
    def update_beliefs(self, model_name: str, 
                       evidence: Dict[str, Any],
                       sample_kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update beliefs given new evidence.
        
        Args:
            model_name: Name of the model to update
            evidence: Observed data {variable_name: value}
            sample_kwargs: Optional kwargs for pm.sample()
            
        Returns:
            Dictionary with posterior summaries for all variables
        """
        if model_name not in self.belief_models:
            raise ValueError(f"Model {model_name} not found")
            
        model_data = self.belief_models[model_name]
        
        # Default sampling parameters
        sampling_params = {
            'draws': 1000,
            'tune': 500,
            'chains': 2,
            'return_inferencedata': True
        }
        
        # Update with user-provided parameters
        if sample_kwargs:
            sampling_params.update(sample_kwargs)
        
        with model_data['model']:
            # Add observed data based on evidence
            for var_name, value in evidence.items():
                if var_name in model_data['vars']:
                    # Create a potential to incorporate the evidence
                    pm.Potential(f"obs_{var_name}", pm.math.switch(
                        pm.math.eq(model_data['vars'][var_name], value),
                        0,
                        -np.inf
                    ))
            
            # Sample from the posterior
            trace = pm.sample(**sampling_params)
        
        # Extract posterior summaries
        results = {}
        for var_name in model_data['vars']:
            results[var_name] = extract_posterior_stats(trace, var_name)
        
        return results
    
    def compare_models(self, model_names: List[str], 
                       evidence: Dict[str, Any],
                       method: str = "waic") -> Dict[str, Any]:
        """Compare multiple models given the same evidence.
        
        Args:
            model_names: List of model names to compare
            evidence: Observed data {variable_name: value}
            method: Method to use for comparison ('waic' or 'loo')
            
        Returns:
            Dictionary with comparison metrics for all models
        """
        # Validate models
        for name in model_names:
            if name not in self.belief_models:
                raise ValueError(f"Model {name} not found")
        
        # Update beliefs for all models
        traces = {}
        for name in model_names:
            traces[name] = self.update_beliefs(name, evidence)
        
        # Compare models using specified method
        if method == "waic":
            waic_results = {}
            for name, trace in traces.items():
                with self.belief_models[name]['model']:
                    waic_results[name] = az.waic(trace)
            return {"method": "waic", "results": waic_results}
        
        elif method == "loo":
            loo_results = {}
            for name, trace in traces.items():
                with self.belief_models[name]['model']:
                    loo_results[name] = az.loo(trace)
            return {"method": "loo", "results": loo_results}
        
        else:
            raise ValueError(f"Unsupported comparison method: {method}")
    
    def predict(self, model_name: str, 
                posterior: Dict[str, Any],
                new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate predictions using a model and posterior.
        
        Args:
            model_name: Name of the model to use
            posterior: Posterior samples for model variables
            new_data: New data points to predict for
            
        Returns:
            Dictionary with predictions and uncertainty estimates
        """
        if model_name not in self.belief_models:
            raise ValueError(f"Model {model_name} not found")
            
        model_data = self.belief_models[model_name]
        
        with model_data['model']:
            # Setup posterior predictive sampling
            pp_trace = pm.sample_posterior_predictive(
                posterior,
                var_names=list(new_data.keys())
            )
        
        # Extract predictions
        predictions = {}
        for var_name in new_data:
            predictions[var_name] = {
                "mean": pp_trace.posterior_predictive[var_name].mean(dim=["chain", "draw"]).values,
                "std": pp_trace.posterior_predictive[var_name].std(dim=["chain", "draw"]).values,
                "hdi": az.hdi(pp_trace.posterior_predictive[var_name])
            }
        
        return predictions
    
    def get_model_names(self) -> List[str]:
        """Get names of all available models.
        
        Returns:
            List of model names
        """
        return list(self.belief_models.keys())