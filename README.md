# Oura Ring MCP Server

A Model Context Protocol (MCP) implementation wrapping calls to the Oura Ring API.

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
make sync
```

Finally, you can run the project with the following command:

```sh
make run
```

## Built With

- [FastAPI](https://fastapi.tiangolo.com/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [uv](https://github.com/astral-sh/uv)

## Oura Ring API

Oura Ring limits users to 5,000 requests per 5 minute period, but they say they have not had any users hit rate limits with webhook properly implemented.

Different data has different sync policies for them:
- Sleep data only syncs when users open the app
- Daily activity and stress, for instance, sync in the background

In order to use this MCP server, you will need to register with the Oura Ring developer portal and get your own keys to plug into a `.env` file (copied over from the `.env.example`).

## Resources

- [Model Context Protocol overview](https://modelcontextprotocol.io/docs/getting-started/intro), [architecture concepts](https://modelcontextprotocol.io/docs/learn/architecture), and [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts)
- [Model Context Protocol Github repository](https://github.com/modelcontextprotocol)
- [Oura Ring API Documentation](https://cloud.ouraring.com/v2/docs)
