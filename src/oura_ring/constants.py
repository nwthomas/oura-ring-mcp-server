import os
from dotenv import load_dotenv

load_dotenv()

# General constants and secrets
SERVER_USER_AGENT = "oura-ring-mcp-server/0.1.0"
SERVER_TIMEOUT_SECONDS = 5.0

# Oura Ring constants and secrets
OURA_RING_API_BASE = "https://api.ouraring.com"

# !IMPORTANT: Follow the directions in the README.md file to get this token process setup
OURA_RING_USER_CODE = os.getenv("OURA_RING_USER_CODE", "")
OURA_RING_CLIENT_ID = os.getenv("OURA_RING_CLIENT_ID", "")
OURA_RING_CLIENT_SECRET = os.getenv("OURA_RING_CLIENT_SECRET", "")

# For storing tokens locally against future MCP server runs
OURA_RING_TOKEN_FILE_NAME = "tokens.json"
OURA_RING_ACCESS_TOKEN_NAME = "access_token"
OURA_RING_REFRESH_TOKEN_NAME = "refresh_token"
