"""
Command-line interface for VEPmcp.
"""

import argparse
import asyncio
import logging
import sys
from typing import Optional

from .bridge import Bridge, Config

# Configure logging
logger = logging.getLogger("vep-mcp")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="VEPmcp",
        description="VEP MCP Server - Model Context Protocol server for Ensembl VEP API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  VEPmcp --test-connection     # Test connection to Ensembl API
  VEPmcp --test-mode          # Run server in test mode with sample requests
  VEPmcp --version             # Show version information
  VEPmcp --help                # Show this help message

The server communicates via stdin/stdout using the Model Context Protocol.
It's designed to be used with MCP-compatible clients like Claude Desktop.

For more information, visit: https://github.com/not-a-feature/VEPmcp
        """,
    )

    # Global options
    parser.add_argument("--version", action="version", version="VEPmcp 0.1.0")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds (default: 30.0)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test connection to Ensembl API and exit",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run server in test mode with sample requests",
    )

    return parser


def load_config(config_path: Optional[str]) -> Config:
    """Load configuration from file or use defaults."""
    # TODO: Implement configuration file loading if needed
    return Config()


async def test_connection() -> None:
    """Test connection to Ensembl VEP API"""
    print("Testing connection to Ensembl VEP API...")

    config = Config()
    bridge = Bridge(config)
    try:
        async with bridge:
            # Test a simple API call
            result = await bridge.get_vep_species()
            if result:
                print("✓ Connection successful!")
                print(f"✓ Found {len(result)} available species")
                print("✓ VEP API is accessible")
            else:
                print("✗ Connection failed - no data received")
                sys.exit(1)
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        sys.exit(1)


async def test_mode() -> None:
    """Run the server in test mode with sample requests."""
    print("Running VEP MCP server in test mode...")
    print("This will test the server with sample requests without requiring an MCP client.")

    from .mcp_server import MCPServer

    server = MCPServer()

    # Test tools/list
    print("\n1. Testing tools/list...")
    list_request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    await server.handle_request(list_request)

    # Test get_vep_species
    print("\n2. Testing get_vep_species...")
    species_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "get_vep_species", "arguments": {}},
    }
    await server.handle_request(species_request)

    print("\nTest mode completed successfully!")


def main(args: Optional[list] = None) -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # Configure logging level
    if parsed_args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if parsed_args.test_connection:
        asyncio.run(test_connection())
        return 0

    if parsed_args.test_mode:
        asyncio.run(test_mode())
        return 0

    # Default behavior: start the MCP server
    try:
        from .mcp_server import MCPServer

        server = MCPServer()
        print("Starting VEP MCP server...")
        print("Press Ctrl+C to stop the server.")
        print("This server communicates via stdin/stdout using the Model Context Protocol.")
        asyncio.run(server.run())
        return 0

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        if parsed_args.verbose:
            raise
        else:
            print(f"Error: {e}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())
