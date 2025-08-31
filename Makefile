build:
	uv sync
	uv run build

run:
	uvicorn main:app --reload

test:
	uv run pytest

clean:
	uv sync --clean
	uv run build --clean
	uv run test --clean