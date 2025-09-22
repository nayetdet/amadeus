.PHONY: run

run:
	uv run uvicorn src.amadeus.main:app
