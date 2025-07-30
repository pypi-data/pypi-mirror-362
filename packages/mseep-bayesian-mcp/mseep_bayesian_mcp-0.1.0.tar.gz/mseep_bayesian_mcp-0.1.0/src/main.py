"""
Main entry point for the Bayesian MCP server.

This module provides the main function for starting the MCP server.
It also includes CLI argument parsing for configuration.
"""

import argparse
import logging
import os
import sys
from typing import Dict, Any

from .mcp.server import start_server


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Bayesian MCP Server")
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1", 
        help="Host to bind the server to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to (default: 8000)"
    )
    parser.add_argument(
        "--log-level", 
        type=str, 
        default="info", 
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level (default: info)"
    )
    
    return parser.parse_args()


def setup_logging(log_level: str):
    """Configure logging for the application."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
        
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )


def main():
    """Main function to start the server."""
    args = parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info(f"Starting Bayesian MCP Server on {args.host}:{args.port}")
    
    try:
        # Start the server
        start_server(
            host=args.host,
            port=args.port,
            log_level=args.log_level
        )
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()