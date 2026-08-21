"""
This file contains tests for the MCP server.

It skips testing the various tool functions as they're essentially light wrappers around the Oura
Ring API route functions and only really add useful code comments used by the LLM.
"""

import sys
from unittest.mock import patch

from src.mcp.constants import SERVER_PORT
from src.mcp.mcp import mcp, start_server


def test_start_server_with_stdio_transport():
    with patch.object(mcp, "run") as mock_run:
        with patch("builtins.print") as mock_print:
            start_server()
            mock_run.assert_called_once_with(transport="stdio")
            mock_print.assert_called_once_with(
                f"Starting {mcp.name} on port {SERVER_PORT}", file=sys.stderr
            )
