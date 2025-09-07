nuke:
	uv cache clean

run:
	uv run main.py

sync:
	uv sync --reinstall

test:
	# NOTE: make venv, make sync, and source .venv/bin/activate must be run before this command
	uv run pytest

venv:
	# NOTE: source .venv/bin/activate must be run manually after this command
	uv venv