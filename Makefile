.PHONY: install dev up down test ingest

install:
	mise install
	mise exec -- pip install -U pip -r requirements.txt

dev:
	mise exec -- uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

up:
	docker compose up -d

down:
	docker compose down

test:
	mise exec -- pytest -v

ingest:
	mise exec -- python scripts/ingest.py --limit 10
