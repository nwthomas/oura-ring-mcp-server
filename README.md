# Oura Ring MCP Server

This repository contains a Model Context Protocol (MCP) implementation wrapping calls to the Oura Ring API. It can be used by any LLM that implements the MCP client protocol in order to interface with it. It's currently setup to run locally.

## Setup

First, you'll need to ensure that you have `uv` and the right Python versions.

Run these commands (assuming you don't already have them installed):

```sh
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# First, install pyenv
brew update
brew install pyenv
curl https://pyenv.run | bash

# Then, add these to your shell
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Restart your shell using one of these commands
source ~/.zshrc
source ~/.bashrc

# Install Python 3.12.4 in Pyenv and set it as global
pyenv install 3.12.14
pyenv global 3.12.14

# Finally, verify via these commands
python --version
pyenv version
```

Next, you'll need to setup the environment for this repository and install dependencies. You can do that with these commands (assuming you already completed the above Python version and `uv` install process):

```sh
# Setup virtual environment
make venv

# Start the virtual environment
source .venv/bin/activate

# Synchronize dependencies
make sync
```

Finally, you can run the project with the following command:

```sh
make run
```

However, this MCP server will likely be accessed locally. I will eventually wire up a Docker build process, but you can follow the [Anthropic local MCP server](https://modelcontextprotocol.io/quickstart/user) setup options until then to run it locally. It will integrate with any LLM that has MCP client wrappers setup.

If you want to exit the virtual environment, just run:

```sh
deactivate
```

## Built With

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [uv](https://github.com/astral-sh/uv)

## Oura Ring API Overview

Different data has different sync policies for different types of data they collect:
- Sleep data only syncs when users open the app
- Daily activity and stress sync in the background without using the app

This can explain any descrepencies you see when your LLM tries to fetch most recent data. You might not have the most recent sleep data available until you (as a human) open up your Oura Ring app next.

In order to use this MCP server, you will need to register with the Oura Ring developer portal and get your own keys to plug into a `.env` file (copied over from the `.env.example`). It's currently using the Personal Access Token (PAT), but Oura Ring has plans to deprecate this at the end of 2025.

This repository will get updated soon to accomodate OAuth2 authentication before then.

The Oura Ring API is a REST API that has two paradigms:
1. A webhook-based implementation where Oura Ring calls your API with event-driven updates; the object ID from these events is then used to fetch a single resource of its given type
2. You (this MCP server) call Oura Ring's API directly with date ranges in order to fetch resources within that date range

Because of this, Oura Ring offers up a `"Single <resource type> Document"` endpoint and a `"Multiple <resource type> Documents"` endpoint for every type of call you can make.

Given that this MCP server will be used by an LLM, I've opted to just use the multiple object resource fetch via date ranges and allow the LLM to decide what date range it wants to pull.

More information can be found in the [Oura Ring API Documentation](https://cloud.ouraring.com/v2/docs).

## Oura Ring Data Model

The following is a direct copy of the documentation at time of this writing (you can also find the [dcoumentation right here](https://cloud.ouraring.com/v2/docs#section/Core-Concepts)):

### Data Types Overview

- Daily Summaries: Aggregated metrics for each day (sleep score, readiness score, activity score)
- Time Series Data: Detailed measurements taken throughout the day (heart rate, HRV, temperature)
- Events: Discrete occurrences such as workouts, tags, and sessions

#### Data Processing Timeline

1. Data Collection: The Oura Ring continuously collects biometric data
2. Syncing: Data transfers to the Oura cloud when users sync their ring via the mobile app
3. Processing: Algorithms analyze raw data to generate insights and scores
4. API Availability: Processed data becomes available through API endpoints

#### Data Syncing Behavior

Different data types follow different syncing patterns:
- User-Initiated Sync Data:
    - Sleep Data: Only syncs when the user opens the Oura app and actively syncs their ring
    - Sleep Time Recommendations: Updated after sleep data syncs
    - Readiness: Calculated after sleep data is processed
- Background Sync Data:
    - Daily Activity: Updates periodically in the background
    - Daily Stress: Updates periodically in the background
    - Heart Rate: Updates periodically in the background This difference in syncing behavior affects when data becomes available through the API. For the most reliable access to all data types, we strongly recommend implementing webhooks to receive notifications when new data is available.

#### Common Data Structures

- Timestamps: All time-based data uses ISO 8601 format
- Scores: Range from 0-100, with higher values indicating better performance
- Durations: Provided in seconds unless otherwise specified
- IDs: Unique identifiers for specific data objects follow a consistent format

### Data Freshness

The Oura API provides the most recently synced data, which depends on when users last synced their ring. For real-time updates, consider using webhooks to receive notifications when new data becomes available.

### Best Practices for Data Access

- Initial Load: When a user first connects to your application, make a single request for historical data
- Ongoing Updates: Use webhooks for all subsequent data updates
- Webhook Integration: This approach minimizes API calls and ensures you always have the latest data
- Error Handling: Be prepared for occasional gaps in data if users don't regularly sync their rings

## API Version Information

The current Oura API (V2) is the only available integration point. The previous V1 API has been sunset and is no longer available.


## Resources

- [Model Context Protocol overview](https://modelcontextprotocol.io/docs/getting-started/intro), [architecture concepts](https://modelcontextprotocol.io/docs/learn/architecture), and [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts)
- [Model Context Protocol Github repository](https://github.com/modelcontextprotocol) and [Python SDK](https://github.com/modelcontextprotocol/python-sdk/tree/main)
- [Oura Ring API Documentation](https://cloud.ouraring.com/v2/docs)
