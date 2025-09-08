"""
This file contains tests for the MCP server.

It skips testing the various tool functions as they're essentially light wrappers around the Oura
Ring API route functions and only really add useful code comments used by the LLM.
"""

import pytest
from unittest.mock import patch
from src.mcp.mcp import start_server, mcp

def test_start_server_with_stdio_transport():
    with patch.object(mcp, 'run') as mock_run:
        with patch('builtins.print') as mock_print:
            start_server()
            mock_run.assert_called_once_with(transport='stdio')
            mock_print.assert_called_once_with(f"Starting {mcp.name}")
