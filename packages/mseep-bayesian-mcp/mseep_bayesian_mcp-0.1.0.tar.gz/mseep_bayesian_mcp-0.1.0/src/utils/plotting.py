"""
Visualization utilities for Bayesian models.

This module contains helper functions for generating visualizations of
Bayesian models and their results.
"""

import base64
import io
from typing import Dict, List, Optional, Any, Tuple
import tempfile

import numpy as np
import matplotlib.pyplot as plt
import arviz as az
import pymc as pm


def plot_to_base64(fig=None) -> str:
    """
    Convert a matplotlib figure to base64 encoded string.
    
    Args:
        fig: The matplotlib figure to convert. If None, the current figure is used.
        
    Returns:
        Base64 encoded string of the figure.
    """
    if fig is None:
        fig = plt.gcf()
        
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    
    # Convert to base64
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return img_str


def save_plot_to_temp(fig=None) -> str:
    """
    Save a matplotlib figure to a temporary file.
    
    Args:
        fig: The matplotlib figure to save. If None, the current figure is used.
        
    Returns:
        Path to the saved file.
    """
    if fig is None:
        fig = plt.gcf()
        
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        fig.savefig(tmp.name, dpi=300)
        return tmp.name


def create_trace_plot(trace, var_names=None, title=None) -> Tuple[plt.Figure, str]:
    """
    Create a trace plot for the specified variables.
    
    Args:
        trace: The PyMC trace object
        var_names: Names of variables to plot
        title: Title for the plot
        
    Returns:
        Tuple of (figure, base64_string)
    """
    fig = plt.figure(figsize=(12, 8))
    az.plot_trace(trace, var_names=var_names)
    
    if title:
        plt.suptitle(title)
    plt.tight_layout()
    
    img_str = plot_to_base64(fig)
    return fig, img_str


def create_posterior_plot(trace, var_names=None, title=None) -> Tuple[plt.Figure, str]:
    """
    Create a posterior distribution plot for the specified variables.
    
    Args:
        trace: The PyMC trace object
        var_names: Names of variables to plot
        title: Title for the plot
        
    Returns:
        Tuple of (figure, base64_string)
    """
    fig = plt.figure(figsize=(12, 8))
    az.plot_posterior(trace, var_names=var_names)
    
    if title:
        plt.suptitle(title)
    plt.tight_layout()
    
    img_str = plot_to_base64(fig)
    return fig, img_str


def create_pair_plot(trace, var_names=None, title=None) -> Tuple[plt.Figure, str]:
    """
    Create a pair plot for the specified variables.
    
    Args:
        trace: The PyMC trace object
        var_names: Names of variables to plot
        title: Title for the plot
        
    Returns:
        Tuple of (figure, base64_string)
    """
    fig = plt.figure(figsize=(12, 10))
    az.plot_pair(trace, var_names=var_names, kind="scatter")
    
    if title:
        plt.suptitle(title)
    plt.tight_layout()
    
    img_str = plot_to_base64(fig)
    return fig, img_str


def create_forest_plot(trace, var_names=None, title=None) -> Tuple[plt.Figure, str]:
    """
    Create a forest plot for the specified variables.
    
    Args:
        trace: The PyMC trace object
        var_names: Names of variables to plot
        title: Title for the plot
        
    Returns:
        Tuple of (figure, base64_string)
    """
    fig = plt.figure(figsize=(12, 8))
    az.plot_forest(trace, var_names=var_names)
    
    if title:
        plt.suptitle(title)
    plt.tight_layout()
    
    img_str = plot_to_base64(fig)
    return fig, img_str