from dotenv import load_dotenv
import os

load_dotenv()

# Server constants and secrets
SERVER_NAME = "oura-ring-mcp-server"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# Oura Ring constants and secrets
OURA_RING_CLIENT_ID=os.getenv("OURA_RING_CLIENT_ID")
OURA_RING_CLIENT_SECRET=os.getenv("OURA_RING_CLIENT_SECRET")
OURA_RING_BEARER_TOKEN=os.getenv("OURA_RING_BEARER_TOKEN")
OURA_RING_REFRESH_TOKEN=os.getenv("OURA_RING_REFRESH_TOKEN")
# NOTE: Oura Ring says the Personal Access Tokens (PATs) are only valid until the end of 2025. See:
# https://cloud.ouraring.com/v2/docs#section/Deprecation-Warning-Personal-Access-Tokens
OURA_RING_PERSONAL_ACCESS_TOKEN=os.getenv("OURA_RING_PERSONAL_ACCESS_TOKEN")