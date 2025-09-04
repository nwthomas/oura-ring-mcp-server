# NOTE: All current API documentation for Oura Ring is using the v2 version of their API
import os
from dotenv import load_dotenv

load_dotenv()

# General constants and secrets
SERVER_USER_AGENT = "oura-ring-mcp-server/0.1.0"
SERVER_TIMEOUT_SECONDS = 5.0

# Oura Ring constants and secrets
OURA_RING_API_BASE = "https://api.ouraring.com"
# NOTE: Oura Ring says the Personal Access Tokens (PATs) are only valid until the end of 2025. See:
# https://cloud.ouraring.com/v2/docs#section/Deprecation-Warning-Personal-Access-Tokens
OURA_RING_PERSONAL_ACCESS_TOKEN=os.getenv("OURA_RING_PERSONAL_ACCESS_TOKEN")