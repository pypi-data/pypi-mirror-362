"""
main.py - Local/STDIO Entrypoint for Tessell MCP Server

This file serves as the entry point for running the Tessell MCP (Model Context Protocol) server in local or stdio mode.

Key Points:
- This entrypoint is intended for local development, testing, and integration with MCP clients (such as Cursor or Visual Studio Code).
- It runs the MCP server in stdio mode, allowing direct communication with local tools and editors.
- All business logic, tool registration, and server configuration are handled via imports from the main MCP server and tools modules.
- For cloud/serverless deployment (e.g., AWS Lambda), use `app.py` instead.

See the README for more details on running in different modes.
"""

import logging
from mcp_core.mcp_server import mcp
from mcp_core.tools.availability_machine import *
from mcp_core.tools.services import *

# Configure root logger for the package (can be customized further)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Tessell MCP server (local/stdio mode)...")
    mcp.run()

if __name__ == "__main__":
    main()
