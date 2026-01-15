# Docker Compose & E2E Testing Guide

This guide explains how to use Docker Compose to run all AI audio services locally and execute comprehensive end-to-end tests.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Services](#services)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [CI/CD Integration](#cicd-integration)

## Overview

The Docker Compose setup provides:

1. **LocalAI** - Open-source AI server for TTS, STT, and audio generation
2. **ComfyUI** - Node-based workflow system for audio processing
3. **UVR5 Mock** - Simulated vocal separation service
4. **RVC Mock** - Simulated voice conversion service
5. **Test Runner** - Container for running tests against all services

## Quick Start

### Using Make Commands (Recommended)

The Makefile automatically detects whether to use `docker compose` or `docker-compose`:

```bash
# See all available commands
make help

# Setup: Build and start all services
make setup

# Run e2e tests
make test-e2e

# Run unit tests (no Docker needed)
make test-unit

# Stop everything
make docker-down
```

### Manual Docker Compose Commands

**Note**: Modern Docker uses `docker compose` (with space). Older versions use `docker-compose` (with hyphen).

```bash
# Build images
docker compose build

# Start services
docker compose up -d

# Check status
docker compose ps

# Run tests
docker compose run --rm test-runner pytest tests/ -v -m e2e

# View logs
docker compose logs -f localai

# Stop services
docker compose down
```

## Services

### LocalAI (Port 8080)

**Purpose**: Open-source AI API compatible with OpenAI

**Features**:
- Text-to-Speech (TTS)
- Speech-to-Text (STT) with Whisper
- Audio generation with MusicGen

**Access**:
- API: http://localhost:8080
- Health: http://localhost:8080/readyz

**Configuration**:
```yaml
environment:
  - THREADS=4
  - CONTEXT_SIZE=512
volumes:
  - ./docker/localai/models:/models
```

### ComfyUI (Port 8188)

**Purpose**: Node-based workflow system for AI image/audio generation

**Features**:
- Custom workflow execution
- Web UI for designing workflows
- Audio generation nodes

**Access**:
- Web UI: http://localhost:8188
- API: http://localhost:8188/api
- Health: http://localhost:8188/system_stats

**Configuration**:
```yaml
volumes:
  - ./docker/comfyui/models:/opt/ComfyUI/models
  - ./docker/comfyui/custom_nodes:/opt/ComfyUI/custom_nodes
  - ./docker/comfyui/output:/opt/ComfyUI/output
  - ./examples:/opt/ComfyUI/workflows
```

### UVR5 Mock (Port 5000)

**Purpose**: Simulated UVR5 API for testing stem separation

**Features**:
- Mock audio separation into vocals/instrumentals
- Model listing
- Job status tracking

**Access**:
- API: http://localhost:5000
- Health: http://localhost:5000/health

**Endpoints**:
- `GET /health` - Health check
- `GET /api/models` - List models
- `POST /api/separate` - Separate audio
- `GET /api/result/{job_id}` - Get job result
- `GET /api/download/{job_id}/{stem_type}` - Download stem

### RVC Mock (Port 6000)

**Purpose**: Simulated RVC API for testing voice conversion

**Features**:
- Mock voice conversion
- Model management
- Voice model information

**Access**:
- API: http://localhost:6000
- Health: http://localhost:6000/health

**Endpoints**:
- `GET /health` - Health check
- `GET /api/models` - List models
- `GET /api/models/{model_name}` - Get model info
- `POST /api/convert` - Convert voice
- `POST /api/train` - Train model (simulated)

## Testing

### Test Types

#### Unit Tests
- No external services required
- Fast execution
- Mock all external dependencies

```bash
# Run locally
make test-unit

# Or with pytest
pytest tests/ -v -m "not e2e"
```

#### E2E Tests
- Require all services running
- Test full integration
- Validate real API calls

```bash
# Run with Docker (recommended)
make test-e2e

# Or manually
docker-compose up -d
docker-compose run --rm test-runner pytest tests/ -v -m e2e
docker-compose down
```

### Test Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── test_localai_client.py      # LocalAI unit tests
├── test_comfyui_client.py      # ComfyUI unit tests
├── test_uvr5_client.py         # UVR5 unit tests
├── test_rvc_client.py          # RVC unit tests
└── test_e2e_integration.py     # E2E integration tests
```

### E2E Test Coverage

The E2E tests verify:

1. **Service Health**
   - All services start correctly
   - Health checks pass
   - Services are reachable

2. **API Functionality**
   - Model listing
   - Audio processing
   - File handling

3. **Integration Workflows**
   - Multi-service orchestration
   - Data flow between services
   - Error handling

### Running Specific Tests

```bash
# Run only LocalAI e2e tests
docker-compose run --rm test-runner pytest tests/test_e2e_integration.py::TestLocalAIE2E -v

# Run only UVR5 e2e tests
docker-compose run --rm test-runner pytest tests/test_e2e_integration.py::TestUVR5E2E -v

# Run workflow tests
docker-compose run --rm test-runner pytest tests/test_e2e_integration.py::TestIntegrationWorkflow -v
```

## Development

### Local Development Workflow

1. **Start services you need:**
```bash
make dev-localai    # Start only LocalAI
make dev-comfyui    # Start only ComfyUI
make dev-uvr5       # Start UVR5 mock
make dev-rvc        # Start RVC mock
```

2. **Run tests locally:**
```bash
# Install dev dependencies
make install-dev

# Run unit tests
make test-unit

# Run e2e tests (services must be running)
make test-e2e-local
```

3. **Debug with shell access:**
```bash
# Shell into test container
make shell-test

# Shell into specific service
docker-compose exec localai sh
docker-compose exec comfyui bash
```

### Adding New Tests

1. **Create test file** in `tests/` directory
2. **Mark e2e tests** with `@pytest.mark.e2e`
3. **Use fixtures** from `conftest.py`
4. **Run tests** with `make test-e2e`

Example:
```python
import pytest

pytestmark = pytest.mark.e2e

class TestMyFeature:
    def test_something(self):
        # Your test here
        pass
```

### Mock Server Development

Mock servers are in `docker/*/app.py`:

**To modify a mock server:**
1. Edit `docker/uvr5-mock/app.py` or `docker/rvc-mock/app.py`
2. Rebuild: `docker-compose build uvr5-mock`
3. Restart: `docker-compose up -d uvr5-mock`
4. Test: `curl http://localhost:5000/health`

**To add endpoints:**
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    # Implementation
    return jsonify({"result": "success"}), 200
```

## Troubleshooting

### Services Won't Start

**Check Docker status:**
```bash
docker info
docker-compose ps
```

**Check logs:**
```bash
docker-compose logs localai
docker-compose logs comfyui
```

**Restart services:**
```bash
docker-compose restart localai
docker-compose restart comfyui
```

### Health Checks Failing

**Wait longer:**
- LocalAI: 60-90 seconds
- ComfyUI: 60-90 seconds
- Mock services: 10-20 seconds

**Check manually:**
```bash
curl http://localhost:8080/readyz
curl http://localhost:8188/system_stats
curl http://localhost:5000/health
curl http://localhost:6000/health
```

### Tests Failing

**Verify services are healthy:**
```bash
docker-compose ps
# Look for "healthy" status
```

**Run with verbose output:**
```bash
docker-compose run --rm test-runner pytest tests/test_e2e_integration.py -vvs
```

**Check service logs:**
```bash
docker-compose logs localai | tail -50
docker-compose logs comfyui | tail -50
```

### Port Conflicts

**Check what's using ports:**
```bash
lsof -i :8080
lsof -i :8188
lsof -i :5000
lsof -i :6000
```

**Change ports in docker-compose.yml:**
```yaml
services:
  localai:
    ports:
      - "8081:8080"  # Changed from 8080:8080
```

### Out of Memory

**Increase Docker memory:**
- Docker Desktop: Settings → Resources → Memory (set to 8GB+)

**Check memory usage:**
```bash
docker stats
```

**Reduce concurrent services:**
```bash
# Start only what you need
docker-compose up -d uvr5-mock rvc-mock
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Start services
        run: |
          docker-compose up -d
          sleep 120  # Wait for services
      
      - name: Check service health
        run: |
          docker-compose ps
          curl -f http://localhost:8080/readyz || exit 1
          curl -f http://localhost:5000/health || exit 1
          curl -f http://localhost:6000/health || exit 1
      
      - name: Run E2E tests
        run: docker-compose run --rm test-runner pytest tests/ -v -m e2e
      
      - name: Show logs on failure
        if: failure()
        run: docker-compose logs
      
      - name: Cleanup
        if: always()
        run: docker-compose down -v
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
e2e_tests:
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache docker-compose
  script:
    - docker-compose up -d
    - sleep 120
    - docker-compose run --rm test-runner pytest tests/ -v -m e2e
  after_script:
    - docker-compose down -v
  only:
    - merge_requests
    - main
```

## Best Practices

1. **Always clean up**: Use `make clean` or `docker-compose down -v`
2. **Wait for health**: Services need time to start (60-120s)
3. **Use make commands**: Easier than remembering Docker commands
4. **Check logs first**: When debugging, always check service logs
5. **Test locally first**: Run unit tests before e2e tests
6. **Isolate issues**: Start services one at a time to identify problems

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [LocalAI Documentation](https://localai.io/)
- [ComfyUI Documentation](https://github.com/comfyanonymous/ComfyUI)

## Support

For help:
1. Check [docker/README.md](docker/README.md)
2. Review service logs: `docker-compose logs <service>`
3. Run with verbose output: `pytest -vvs`
4. Open an issue on GitHub
