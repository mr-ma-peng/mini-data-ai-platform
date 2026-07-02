.PHONY: install dev up down test ingest

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

dev:
	.venv/bin/uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

up:
	docker compose up -d

down:
	docker compose down

test:
	.venv/bin/pytest -v

ingest:
	.venv/bin/python scripts/ingest.py --limit 10
