.PHONY: help docker-up docker-down docker-logs test test-unit test-e2e test-all clean docker-build

# Detect if docker-compose or docker compose is available
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null)
ifndef DOCKER_COMPOSE
    DOCKER_COMPOSE := docker compose
endif

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

docker-build: ## Build all Docker images
	$(DOCKER_COMPOSE) build

docker-up: ## Start all services in detached mode
	$(DOCKER_COMPOSE) up -d

docker-down: ## Stop all services
	$(DOCKER_COMPOSE) down

docker-down-volumes: ## Stop all services and remove volumes
	$(DOCKER_COMPOSE) down -v

docker-logs: ## View logs from all services
	$(DOCKER_COMPOSE) logs -f

docker-ps: ## Show status of all services
	$(DOCKER_COMPOSE) ps

docker-health: ## Check health of all services
	@echo "Checking service health..."
	@$(DOCKER_COMPOSE) ps | grep "healthy" || echo "Waiting for services to become healthy..."

test-unit: ## Run unit tests only (no services needed)
	pytest tests/ -v -m "not e2e"

test-e2e: ## Run e2e tests (requires services to be running)
	$(DOCKER_COMPOSE) run --rm test-runner pytest tests/ -v -m e2e

test-e2e-local: ## Run e2e tests locally (services must be running)
	pytest tests/ -v -m e2e

test-all: ## Run all tests via Docker
	$(DOCKER_COMPOSE) run --rm test-runner pytest tests/ -v

test-all-local: ## Run all tests locally
	pytest tests/ -v

clean: ## Clean up Docker resources
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

setup: docker-build docker-up ## Setup: Build and start all services
	@echo "Waiting for services to be healthy (this may take 2-3 minutes)..."
	@sleep 120
	@$(MAKE) docker-health
	@echo "Setup complete! Services are ready."

quick-test: ## Quick test: Start services and run tests
	@$(MAKE) docker-up
	@echo "Waiting 120 seconds for services to start..."
	@sleep 120
	@$(MAKE) test-e2e
	@$(MAKE) docker-down

# Development helpers
dev-localai: ## Start only LocalAI service
	$(DOCKER_COMPOSE) up -d localai

dev-comfyui: ## Start only ComfyUI service
	$(DOCKER_COMPOSE) up -d comfyui

dev-uvr5: ## Start only UVR5 mock service
	$(DOCKER_COMPOSE) up -d uvr5-mock

dev-rvc: ## Start only RVC mock service
	$(DOCKER_COMPOSE) up -d rvc-mock

shell-test: ## Open shell in test runner container
	$(DOCKER_COMPOSE) run --rm test-runner bash

install-dev: ## Install development dependencies locally
	pip install -e ".[dev]"

lint: ## Run linting checks
	@echo "Running linting (if configured)..."
	@command -v flake8 >/dev/null 2>&1 && flake8 . || echo "flake8 not installed"
	@command -v black >/dev/null 2>&1 && black --check . || echo "black not installed"

format: ## Format code with black
	@command -v black >/dev/null 2>&1 && black . || echo "black not installed, run: pip install black"
