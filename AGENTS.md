# AGENTS.md

This file provides guidance to coding agents when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server that wraps the Oura Ring API, enabling LLM clients (like Claude Desktop) to query health data from Oura Ring devices. The server uses OAuth2 authentication with automatic token refresh and runs on stdio transport.

## Development Commands

### Environment Setup

```bash
# Install dependencies and sync environment (run after cloning)
make sync

# Create virtual environment (manual activation required after)
make venv
# Then run: source .venv/bin/activate
```

### Running and Testing

```bash
# Run the MCP server
make run

# Run all tests (requires activated venv)
make test

# Clean UV cache
make nuke
```

### Prerequisites

- Python 3.14+ (managed via pyenv)
- `uv` package manager
- Valid Oura Ring OAuth2 credentials in `.env` file

## Architecture

### Core Structure

**Entry Point**: `main.py` calls `start_server()` which launches the MCP server on stdio transport.

**MCP Layer** (`src/mcp/`):

- `mcp.py`: Defines the FastMCP server and registers tool handlers using `@mcp.tool()` decorators
- Each tool is a thin async wrapper that calls corresponding Oura Ring API route functions
- Tools accept date ranges in `YYYY-MM-DD` format and return data as dictionaries

**Oura Ring Integration** (`src/oura_ring/`):

- `routes.py`: API endpoint functions for each Oura Ring data type (sleep, activity, heart rate, etc.)
- `utils.py`: OAuth2 token management (fetch, refresh, store), request building, and pagination handling
- `constants.py`: Environment variables, API base URL, and token configuration

**Token Management Flow**:

1. On server start, `load_or_fetch_tokens()` loads tokens from `tokens.json`
2. If tokens don't exist, fetches them using `OURA_RING_USER_CODE` from `.env`
3. On every request, refreshes access token using the refresh token
4. Tokens are cached in-memory and persisted to `tokens.json`

**Request Flow**:

1. MCP tool receives request with date range
2. Route function constructs Oura Ring API URL and params
3. `make_oura_ring_request()` handles authentication, pagination via `next_token`, and aggregates results
4. All data across pages is collected and returned as `{"data": [...]}`

### OAuth2 Setup

Initial setup requires manual OAuth2 flow (documented in README):

1. Create Oura Ring application at developer portal
2. Get `client_id`, `client_secret`, and user authorization `code`
3. Store in `.env` as `OURA_RING_CLIENT_ID`, `OURA_RING_CLIENT_SECRET`, `OURA_RING_USER_CODE`
4. Server automatically exchanges user code for access/refresh tokens on first run
5. Subsequent runs use refresh token to get new access tokens

**Critical**: If `tokens.json` is deleted, the OAuth2 flow must be repeated as user codes are single-use.

### Data Synchronization Notes

Different Oura Ring data types sync differently:

- Sleep data: Only syncs when user opens Oura app
- Activity and stress: Background sync without app interaction
- This affects data freshness for LLM queries

## Testing

- Test framework: pytest with pytest-asyncio and pytest-mock
- Tests use `mocker.patch()` to mock `httpx.AsyncClient` and API responses
- All async functions must be decorated with `@pytest.mark.asyncio`
- Test structure: `tests/` mirrors `src/` directory structure

## Configuration

- **Server**: Name and port defined in `src/mcp/constants.py`
- **API**: Base URL and timeouts in `src/oura_ring/constants.py`
- **Secrets**: All credentials loaded via `python-dotenv` from `.env` file
- **Token Storage**: Local `tokens.json` file (gitignored)

## MCP Client Configuration

Claude Desktop setup example:

```json
{
  "mcpServers": {
    "oura-ring": {
      "command": "/Users/<username>/.local/bin/uv",
      "args": ["--directory", "/path/to/oura-ring-mcp-server", "run", "main.py"]
    }
  }
}
```
