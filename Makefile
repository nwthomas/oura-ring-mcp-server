clean:
	uv sync --clean

build:
	make sync
	uv run python -m build

run:
	uv run uvicorn main:app --reload

sync:
	uv sync

test:
	uv run pytest