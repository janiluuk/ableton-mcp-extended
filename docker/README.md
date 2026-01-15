# Docker Setup for Ableton MCP Extended

This directory contains Docker configurations for running all AI audio services locally and executing end-to-end tests.

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
  - **Note**: Modern Docker installations use `docker compose` (with space). Older versions use `docker-compose` (with hyphen). All examples below use `docker compose`, but both work.
- At least 8GB of RAM available for Docker
- 10GB of free disk space

### Start All Services

```bash
# Start all services in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Check service health
docker compose ps
```

### Run Tests

```bash
# Run unit tests only
docker compose run --rm test-runner pytest tests/ -v -m "not e2e"

# Run e2e tests (requires services to be running)
docker compose run --rm test-runner pytest tests/ -v -m e2e

# Run all tests
docker compose run --rm test-runner pytest tests/ -v
```

### Stop Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v
```

## Services

### LocalAI (Port 8080)
- Open-source AI API server
- Provides TTS, STT, and audio generation
- Health check: `http://localhost:8080/readyz`

### ComfyUI (Port 8188)
- Node-based workflow system for audio generation
- Web UI: `http://localhost:8188`
- Health check: `http://localhost:8188/system_stats`

### UVR5 Mock (Port 5000)
- Mock server simulating UVR5 API
- Provides audio stem separation
- Health check: `http://localhost:5000/health`

### RVC Mock (Port 6000)
- Mock server simulating RVC API
- Provides voice conversion
- Health check: `http://localhost:6000/health`

## Directory Structure

```
docker/
├── comfyui/
│   ├── models/          # ComfyUI models
│   ├── custom_nodes/    # Custom nodes
│   └── output/          # Generated files
├── localai/
│   └── models/          # LocalAI models
├── uvr5/
│   └── output/          # Separated stems
├── rvc/
│   ├── models/          # Voice models
│   └── output/          # Converted audio
├── uvr5-mock/           # Mock UVR5 server
│   ├── Dockerfile
│   └── app.py
├── rvc-mock/            # Mock RVC server
│   ├── Dockerfile
│   └── app.py
└── test-runner/         # Test environment
    └── Dockerfile
```

## Environment Variables

The services use the following environment variables (defined in docker-compose.yml):

```env
LOCALAI_BASE_URL=http://localai:8080
COMFYUI_BASE_URL=http://comfyui:8188
UVR5_BASE_URL=http://uvr5-mock:5000
RVC_BASE_URL=http://rvc-mock:6000
AI_AUDIO_OUTPUT_DIR=/tmp/ai_audio
```

## Development Workflow

### 1. Start Services
```bash
docker-compose up -d localai comfyui uvr5-mock rvc-mock
```

### 2. Wait for Health Checks
```bash
# Wait for all services to be healthy
docker-compose ps
```

### 3. Run Tests
```bash
# Unit tests (no services needed)
docker-compose run --rm test-runner pytest tests/ -v -m "not e2e"

# E2E tests (requires services)
docker-compose run --rm test-runner pytest tests/ -v -m e2e
```

### 4. Debug Services
```bash
# View logs for a specific service
docker-compose logs -f localai
docker-compose logs -f comfyui

# Shell into a service
docker-compose exec localai sh
docker-compose exec test-runner bash
```

## Customization

### Add LocalAI Models

Place model files in `docker/localai/models/`:
```bash
# Example: Download a TTS model
cd docker/localai/models
wget https://example.com/model.bin
```

### Add ComfyUI Custom Nodes

Place custom nodes in `docker/comfyui/custom_nodes/`:
```bash
cd docker/comfyui/custom_nodes
git clone https://github.com/example/custom-node
```

### Configure Workflows

Place ComfyUI workflows in the `examples/` directory - they're automatically mounted.

## Troubleshooting

### Services Won't Start

**Check Docker resources:**
```bash
docker system df
docker system prune  # Clean up if needed
```

**Check logs:**
```bash
docker-compose logs localai
```

### Health Checks Failing

**Wait longer for startup:**
- LocalAI needs 60s to initialize
- ComfyUI needs 60s to load
- Mock services start quickly (10s)

**Check connectivity:**
```bash
docker-compose exec test-runner curl http://localai:8080/readyz
docker-compose exec test-runner curl http://comfyui:8188/system_stats
```

### Tests Failing

**Verify services are healthy:**
```bash
docker-compose ps
# All services should show "healthy" status
```

**Run tests with more verbose output:**
```bash
docker-compose run --rm test-runner pytest tests/test_e2e_integration.py -vvs
```

### Port Conflicts

If ports are already in use, modify `docker-compose.yml`:
```yaml
services:
  localai:
    ports:
      - "8081:8080"  # Change first port only
```

## Performance Tips

1. **Use volumes for models** - Models are downloaded once and reused
2. **Allocate enough RAM** - Each service needs 1-2GB
3. **Use SSD storage** - Significantly faster model loading
4. **Limit parallel tests** - Use `pytest -n 2` to limit workers

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start services
        run: docker-compose up -d
      - name: Wait for health
        run: docker-compose run --rm test-runner /bin/sh -c "sleep 120"
      - name: Run tests
        run: docker-compose run --rm test-runner pytest tests/ -v -m e2e
      - name: Cleanup
        run: docker-compose down -v
```

## Cleaning Up

```bash
# Stop services
docker-compose down

# Remove volumes (deletes models and data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Support

For issues with:
- **Docker setup**: Check Docker and Docker Compose versions
- **Service integration**: Review logs with `docker-compose logs`
- **Tests**: Run with `-vvs` for detailed output
- **Mock servers**: Check `docker/*/app.py` for implementation details
