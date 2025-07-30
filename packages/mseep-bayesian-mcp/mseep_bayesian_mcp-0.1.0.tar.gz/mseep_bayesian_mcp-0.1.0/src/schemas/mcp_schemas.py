"""
MCP API Schemas for the Bayesian MCP Server.

This module defines the Pydantic models used for API request/response validation
in the MCP server interface.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class Variable(BaseModel):
    """A variable in a Bayesian model."""
    
    name: str = Field(..., description="The name of the variable")
    distribution: str = Field(..., description="The type of distribution (e.g., 'normal', 'beta', etc.)")
    params: Dict[str, Any] = Field(..., description="Parameters for the distribution")
    observed: Optional[Any] = Field(None, description="Observed value, if any")
    
    
class CreateModelRequest(BaseModel):
    """Request to create a new Bayesian model."""
    
    model_name: str = Field(..., description="Name for the model")
    variables: Dict[str, Dict[str, Any]] = Field(
        ..., 
        description="Dictionary of variables and their specifications"
    )


class UpdateBeliefRequest(BaseModel):
    """Request to update beliefs in a model with new evidence."""
    
    model_name: str = Field(..., description="Name of the model to update")
    evidence: Dict[str, Any] = Field(..., description="Evidence to update the model with")
    sample_kwargs: Optional[Dict[str, Any]] = Field(
        None, 
        description="Optional parameters for the sampling process"
    )


class PredictRequest(BaseModel):
    """Request to make predictions using a model."""
    
    model_name: str = Field(..., description="Name of the model to use for prediction")
    variables: List[str] = Field(..., description="Variables to predict")
    conditions: Optional[Dict[str, Any]] = Field(
        None, 
        description="Conditions for the prediction"
    )


class CompareModelsRequest(BaseModel):
    """Request to compare multiple models."""
    
    model_names: List[str] = Field(..., description="Names of models to compare")
    metric: str = Field(..., description="Metric to use for comparison (e.g., 'waic', 'loo')")


class ModelResponse(BaseModel):
    """Response for model operations."""
    
    model_name: str = Field(..., description="Name of the model")
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Message about the operation")
    data: Optional[Dict[str, Any]] = Field(None, description="Data associated with the response")


class BeliefUpdateResponse(BaseModel):
    """Response for belief update operations."""
    
    model_name: str = Field(..., description="Name of the model")
    success: bool = Field(..., description="Whether the update was successful")
    message: str = Field(..., description="Message about the update")
    posterior: Dict[str, Any] = Field(..., description="Posterior distribution details")
    
    
class PredictionResponse(BaseModel):
    """Response for prediction operations."""
    
    model_name: str = Field(..., description="Name of the model used for prediction")
    success: bool = Field(..., description="Whether the prediction was successful")
    message: str = Field(..., description="Message about the prediction")
    predictions: Dict[str, Any] = Field(..., description="Prediction results")


class ModelComparisonResponse(BaseModel):
    """Response for model comparison operations."""
    
    success: bool = Field(..., description="Whether the comparison was successful")
    message: str = Field(..., description="Message about the comparison")
    comparison: Dict[str, Any] = Field(..., description="Comparison results")


class MCPRequest(BaseModel):
    """General MCP request format."""
    
    function_name: str = Field(..., description="Name of the function to call")
    parameters: Dict[str, Any] = Field(..., description="Parameters for the function call")
    

class MCPResponse(BaseModel):
    """General MCP response format."""
    
    result: Union[
        ModelResponse, 
        BeliefUpdateResponse, 
        PredictionResponse, 
        ModelComparisonResponse
    ] = Field(..., description="Result of the function call")
    
    
class CreateVisualizationRequest(BaseModel):
    """Request to create a visualization of a model."""
    
    model_name: str = Field(..., description="Name of the model to visualize")
    plot_type: str = Field(..., description="Type of plot to generate")
    variables: Optional[List[str]] = Field(None, description="Variables to include in the plot")
    options: Optional[Dict[str, Any]] = Field(None, description="Additional plot options")


class VisualizationResponse(BaseModel):
    """Response for visualization requests."""
    
    model_name: str = Field(..., description="Name of the model visualized")
    success: bool = Field(..., description="Whether the visualization was successful")
    message: str = Field(..., description="Message about the visualization")
    image_data: Optional[str] = Field(None, description="Base64 encoded image data")
    plot_path: Optional[str] = Field(None, description="Path to the saved plot, if applicable")