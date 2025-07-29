"""
Jay MCP - A demo MCP (Model Context Protocol) server

This package provides a simple MCP server with tools and resources
for demonstration purposes.
"""

__version__ = "0.2.1"
__author__ = "Jay MCP Team"
__email__ = "contact@example.com"

from .server import create_server

__all__ = ["create_server", "__version__"]
