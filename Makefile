# Makefile para facilitar comandos comuns do projeto

.PHONY: help install install-dev test test-cov lint format check pre-commit clean

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências de produção
	pip install -r requirements.txt

install-dev: ## Instala dependências de desenvolvimento
	pip install -r requirements-dev.txt
	pre-commit install

test: ## Executa os testes
	pytest -v

test-cov: ## Executa os testes com cobertura
	pytest -v --cov=src/geodata_br_mcp --cov-report=term-missing --cov-report=html

lint: ## Executa o linter (ruff)
	ruff check .

lint-fix: ## Executa o linter e corrige problemas automaticamente
	ruff check . --fix

format: ## Formata o código com ruff e black
	ruff format .
	black .

format-check: ## Verifica se o código está formatado corretamente
	ruff format --check .
	black --check .

type-check: ## Verifica tipos com mypy
	mypy src/

check: lint format-check type-check test ## Executa todas as verificações

pre-commit: ## Executa pre-commit em todos os arquivos
	pre-commit run --all-files

pre-commit-update: ## Atualiza versões dos hooks do pre-commit
	pre-commit autoupdate

clean: ## Remove arquivos temporários e cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true

server: ## Inicia o servidor MCP
	python main.py

.DEFAULT_GOAL := help
