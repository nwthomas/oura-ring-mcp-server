clean:
	uv sync --clean
	uv run build --clean
	uv run test --clean

build:
	uv sync
	uv run build

env:
	uv venv

run:
	uvicorn main:app --reload

sync:
	uv sync

test:
	uv run pytest