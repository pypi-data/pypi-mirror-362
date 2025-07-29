"""
Command line interface for Jay MCP
"""

import argparse
import sys
from .server import run_server
from . import __version__


def main() -> None:
    """
    Main entry point for the CLI
    """
    parser = argparse.ArgumentParser(
        description="Jay MCP - A demo MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jay-mcp                    # Run with stdio transport
  jay-mcp --transport stdio  # Run with stdio transport (explicit)
  jay-mcp --version          # Show version information
        """
    )
    
    parser.add_argument(
        "--transport",
        choices=["stdio"],
        default="stdio",
        help="Transport type (default: stdio)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Jay MCP {__version__}"
    )
    
    args = parser.parse_args()
    
    try:
        run_server(transport=args.transport)
    except KeyboardInterrupt:
        print("\nShutting down Jay MCP server...")
        sys.exit(0)
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
