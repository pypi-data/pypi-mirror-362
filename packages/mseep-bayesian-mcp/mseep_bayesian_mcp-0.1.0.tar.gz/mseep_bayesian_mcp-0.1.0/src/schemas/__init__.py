"""Schema definitions for the Bayesian MCP server."""

from .inputs import (
    PriorSpec,
    LikelihoodSpec,
    InferenceSettings,
    ModelSpec,
    VariableSpec,
    ModelComparisonRequest,
    BeliefUpdateRequest,
    PredictionRequest,
    VisualizationRequest,
)

from .outputs import (
    BayesianResult,
    BeliefUpdateResponse,
    ModelComparisonResponse,
    PredictionResponse,
    VisualizationResponse,
    ModelCreationResponse,
)

__all__ = [
    "PriorSpec",
    "LikelihoodSpec",
    "InferenceSettings",
    "ModelSpec",
    "VariableSpec",
    "ModelComparisonRequest",
    "BeliefUpdateRequest",
    "PredictionRequest",
    "VisualizationRequest",
    "BayesianResult",
    "BeliefUpdateResponse",
    "ModelComparisonResponse",
    "PredictionResponse",
    "VisualizationResponse",
    "ModelCreationResponse",
]