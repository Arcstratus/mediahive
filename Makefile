.PHONY: help dev.frontend dev.backend code.format code.format.frontend code.format.backend

help: ## Show available commands
	@grep -E '^[a-zA-Z._-]+:.*##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev.frontend: ## Start frontend dev server
	cd frontend && npm run dev

dev.backend: code.format.backend ## Start backend dev server (runs code.format.backend first)
	cd backend && uv run fastapi dev app/main.py

code.format: code.format.frontend code.format.backend ## Format frontend and backend code

code.format.frontend: ## Lint and format frontend code with ESLint
	cd frontend && pnpm lint:fix

code.format.backend: ## Format and check backend code with ruff
	cd backend && uv run ruff format && uv run ruff check --fix
