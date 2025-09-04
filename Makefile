nuke:
	uv cache clean

run:
	uv run main.py

sync:
	uv sync --reinstall

test:
	uv run pytest

venv:
	# NOTE: source .venv/bin/activate must be run manually after this command
	uv venv