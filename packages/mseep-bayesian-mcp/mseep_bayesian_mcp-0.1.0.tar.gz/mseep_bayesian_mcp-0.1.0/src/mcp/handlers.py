"""
MCP request handlers for the Bayesian MCP Server.

This module contains the handler functions that process MCP requests
and interact with the Bayesian engine.
"""

import json
import base64
from typing import Dict, Any, Optional, List, Tuple
import logging
from pathlib import Path
import tempfile

import numpy as np
import matplotlib.pyplot as plt
import arviz as az

from ..bayesian_engine.engine import BayesianEngine
from ..schemas.mcp_schemas import (
    CreateModelRequest, 
    UpdateBeliefRequest,
    PredictRequest,
    CompareModelsRequest,
    ModelResponse,
    BeliefUpdateResponse,
    PredictionResponse,
    ModelComparisonResponse,
    CreateVisualizationRequest,
    VisualizationResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global engine instance
engine = BayesianEngine()


def handle_create_model(params: Dict[str, Any]) -> ModelResponse:
    """Handle a request to create a new Bayesian model."""
    try:
        # Parse request
        request = CreateModelRequest(**params)
        
        # Create the model
        engine.create_model(request.model_name, request.variables)
        
        # Return response
        return ModelResponse(
            model_name=request.model_name,
            success=True,
            message=f"Model '{request.model_name}' created successfully",
            data={"variables": list(request.variables.keys())}
        )
    except Exception as e:
        logger.error(f"Error creating model: {str(e)}")
        return ModelResponse(
            model_name=params.get("model_name", "unknown"),
            success=False,
            message=f"Error creating model: {str(e)}",
            data=None
        )


def handle_update_beliefs(params: Dict[str, Any]) -> BeliefUpdateResponse:
    """Handle a request to update beliefs with new evidence."""
    try:
        # Parse request
        request = UpdateBeliefRequest(**params)
        
        # Update beliefs
        posterior = engine.update_beliefs(
            request.model_name, 
            request.evidence,
            request.sample_kwargs
        )
        
        # Return response
        return BeliefUpdateResponse(
            model_name=request.model_name,
            success=True,
            message=f"Beliefs for model '{request.model_name}' updated successfully",
            posterior=posterior
        )
    except Exception as e:
        logger.error(f"Error updating beliefs: {str(e)}")
        return BeliefUpdateResponse(
            model_name=params.get("model_name", "unknown"),
            success=False,
            message=f"Error updating beliefs: {str(e)}",
            posterior={}
        )


def handle_predict(params: Dict[str, Any]) -> PredictionResponse:
    """Handle a request to make predictions using a model."""
    try:
        # Parse request
        request = PredictRequest(**params)
        
        # Make predictions
        predictions = engine.predict(
            request.model_name,
            request.variables,
            request.conditions
        )
        
        # Return response
        return PredictionResponse(
            model_name=request.model_name,
            success=True,
            message=f"Predictions for model '{request.model_name}' completed successfully",
            predictions=predictions
        )
    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        return PredictionResponse(
            model_name=params.get("model_name", "unknown"),
            success=False,
            message=f"Error making predictions: {str(e)}",
            predictions={}
        )


def handle_compare_models(params: Dict[str, Any]) -> ModelComparisonResponse:
    """Handle a request to compare models."""
    try:
        # Parse request
        request = CompareModelsRequest(**params)
        
        # Compare models
        comparison = engine.compare_models(
            request.model_names,
            request.metric
        )
        
        # Return response
        return ModelComparisonResponse(
            success=True,
            message=f"Model comparison using '{request.metric}' completed successfully",
            comparison=comparison
        )
    except Exception as e:
        logger.error(f"Error comparing models: {str(e)}")
        return ModelComparisonResponse(
            success=False,
            message=f"Error comparing models: {str(e)}",
            comparison={}
        )


def handle_create_visualization(params: Dict[str, Any]) -> VisualizationResponse:
    """Handle a request to create a visualization of a model."""
    try:
        # Parse request
        request = CreateVisualizationRequest(**params)
        
        # Get the model trace data
        if request.model_name not in engine.belief_models:
            raise ValueError(f"Model '{request.model_name}' not found")
            
        model_data = engine.belief_models[request.model_name]
        if "trace" not in model_data:
            raise ValueError(f"No posterior trace found for model '{request.model_name}'")
            
        trace = model_data["trace"]
        
        # Create visualization based on plot type
        plt.figure(figsize=(10, 6))
        
        if request.plot_type == "trace":
            variables = request.variables or list(trace.posterior.data_vars)
            az.plot_trace(trace, var_names=variables)
            title = f"Trace Plot for {request.model_name}"
            
        elif request.plot_type == "posterior":
            variables = request.variables or list(trace.posterior.data_vars)
            az.plot_posterior(trace, var_names=variables)
            title = f"Posterior Distribution for {request.model_name}"
            
        elif request.plot_type == "forest":
            variables = request.variables or list(trace.posterior.data_vars)
            az.plot_forest(trace, var_names=variables)
            title = f"Forest Plot for {request.model_name}"
            
        elif request.plot_type == "density":
            variables = request.variables or list(trace.posterior.data_vars)
            az.plot_density(trace, var_names=variables)
            title = f"Density Plot for {request.model_name}"
            
        elif request.plot_type == "pair":
            variables = request.variables or list(trace.posterior.data_vars)[:2]  # Default to first 2 vars
            az.plot_pair(trace, var_names=variables, kind="scatter")
            title = f"Pair Plot for {request.model_name}"
            
        else:
            raise ValueError(f"Unsupported plot type: {request.plot_type}")
            
        plt.suptitle(title)
        plt.tight_layout()
        
        # Save to temporary file and encode as base64
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            plot_path = tmp.name
            plt.savefig(plot_path, dpi=300)
            
        # Convert to base64 for API response
        with open(plot_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode("utf-8")
            
        return VisualizationResponse(
            model_name=request.model_name,
            success=True,
            message=f"Visualization created successfully",
            image_data=img_data,
            plot_path=plot_path
        )
        
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        return VisualizationResponse(
            model_name=params.get("model_name", "unknown"),
            success=False,
            message=f"Error creating visualization: {str(e)}",
            image_data=None,
            plot_path=None
        )


# Function mapping for MCP requests
FUNCTION_MAP = {
    "create_model": handle_create_model,
    "update_beliefs": handle_update_beliefs,
    "predict": handle_predict,
    "compare_models": handle_compare_models,
    "create_visualization": handle_create_visualization,
}


def handle_mcp_request(function_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main handler for MCP requests.
    
    Args:
        function_name: The name of the function to call
        parameters: The parameters for the function call
        
    Returns:
        The function result as a dictionary
    """
    if function_name not in FUNCTION_MAP:
        return {
            "success": False,
            "message": f"Unknown function: {function_name}",
            "data": None
        }
        
    handler = FUNCTION_MAP[function_name]
    result = handler(parameters)
    
    # Convert Pydantic model to dict
    if hasattr(result, "dict"):
        return result.dict()
    return result