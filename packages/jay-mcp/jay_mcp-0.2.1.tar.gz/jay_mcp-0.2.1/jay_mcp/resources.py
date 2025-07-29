"""
Resources for Jay MCP server
"""

from mcp.server.fastmcp import FastMCP


def register_resources(mcp: FastMCP) -> None:
    """
    Register all resources with the MCP server
    
    Args:
        mcp: FastMCP server instance
    """
    
    @mcp.resource("greeting://{name}")
    def get_greeting(name: str) -> str:
        """
        Get a personalized greeting
        
        Args:
            name: Name to greet
            
        Returns:
            Personalized greeting message
        """
        return f"Hello, {name}! Welcome to Jay MCP Demo server."
    
    @mcp.resource("info://server")
    def get_server_info() -> str:
        """
        Get server information as a resource
        
        Returns:
            Server information string
        """
        return """
Jay MCP Demo Server
==================

This is a demonstration MCP (Model Context Protocol) server that provides:

Tools:
- add: Add two numbers (with a bonus of 1000)
- multiply: Multiply two numbers
- get_info: Get server information

Resources:
- greeting://{name}: Get a personalized greeting
- info://server: Get this server information

Version: 0.1.0
"""
