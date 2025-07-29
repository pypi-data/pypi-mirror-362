"""
MCP Server implementation for Jay MCP
"""

from mcp.server.fastmcp import FastMCP
from .tools import register_tools
from .resources import register_resources


def create_server(name: str = "Jay MCP Demo") -> FastMCP:
    """
    Create and configure the MCP server
    
    Args:
        name: Server name
        
    Returns:
        Configured FastMCP server instance
    """
    # Create an MCP server
    mcp = FastMCP(name)
    
    # Register tools and resources
    register_tools(mcp)
    register_resources(mcp)
    
    return mcp


def run_server(transport: str = 'stdio') -> None:
    """
    Run the MCP server
    
    Args:
        transport: Transport type (default: 'stdio')
    """
    server = create_server()
    server.run(transport=transport)
