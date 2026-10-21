# Owner: Harsh (Full-stack · QA + DevOps) · Task: T-115
.PHONY: dev test lint gen

dev:   ## start the local stack
	docker compose up -d

test:  ## backend + frontend tests
	cd apps/api && uv run pytest
	cd apps/web && pnpm test

lint:  ## linters, type checks, file-length guard
	cd apps/api && uv run ruff check . && uv run mypy src
	cd apps/web && pnpm lint && pnpm typecheck
	python scripts/check_file_length.py

gen:   ## regenerate the TypeScript API client from OpenAPI
	./scripts/gen_api_client.sh
