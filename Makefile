.PHONY: install dev test lint

install:
	python -m pip install -r requirements.txt -r requirements-dev.txt

dev:
	python -m uvicorn server.main:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check .