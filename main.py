from mcp.server.fastmcp import FastMCP
from src import SERVER_NAME

mcp = FastMCP(SERVER_NAME)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

if __name__ == "__main__":
    mcp.run(transport='stdio')