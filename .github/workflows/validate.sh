#!/bin/bash
# Workflow Validation Script
# Run this locally to validate all GitHub Actions workflows before pushing

set -e

echo "=== GitHub Actions Workflow Validation ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if required tools are installed
echo "Checking required tools..."
command -v python >/dev/null 2>&1 || { echo -e "${RED}✗ Python not found${NC}"; exit 1; }
command -v pip >/dev/null 2>&1 || { echo -e "${RED}✗ pip not found${NC}"; exit 1; }
echo -e "${GREEN}✓ Required tools found${NC}"
echo ""

# Validate YAML syntax
echo "Validating workflow YAML files..."
python -c "
import yaml
import sys
from pathlib import Path

workflows_dir = Path('.github/workflows')
if not workflows_dir.exists():
    print('${RED}✗ .github/workflows directory not found${NC}')
    sys.exit(1)

errors = []
for workflow_file in workflows_dir.glob('*.yml'):
    try:
        with open(workflow_file) as f:
            yaml.safe_load(f)
        print(f'${GREEN}✓ {workflow_file.name}${NC}')
    except Exception as e:
        errors.append(f'{workflow_file.name}: {e}')
        print(f'${RED}✗ {workflow_file.name}: {e}${NC}')

if errors:
    sys.exit(1)
"
echo ""

# Install dev dependencies
echo "Installing dev dependencies..."
pip install -e ".[dev]" > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Run unit tests
echo "Running unit tests..."
if pytest tests/ -v -m "not e2e" --tb=short -q; then
    echo -e "${GREEN}✓ All unit tests passed${NC}"
else
    echo -e "${RED}✗ Unit tests failed${NC}"
    exit 1
fi
echo ""

# Check Python syntax
echo "Checking Python syntax..."
if python -m py_compile localai_mcp/*.py comfyui_mcp/*.py uvr5_mcp/*.py rvc_mcp/*.py 2>/dev/null; then
    echo -e "${GREEN}✓ Python syntax valid${NC}"
else
    echo -e "${RED}✗ Python syntax errors found${NC}"
    exit 1
fi
echo ""

# Test coverage command
echo "Testing coverage generation..."
if pytest tests/ -m "not e2e" --cov=localai_mcp --cov=comfyui_mcp --cov=uvr5_mcp --cov=rvc_mcp --cov-report=xml --cov-report=term -q > /dev/null 2>&1; then
    if [ -f coverage.xml ]; then
        echo -e "${GREEN}✓ Coverage report generated${NC}"
        rm coverage.xml
    else
        echo -e "${YELLOW}⚠ Coverage report not generated${NC}"
    fi
else
    echo -e "${RED}✗ Coverage generation failed${NC}"
    exit 1
fi
echo ""

# Check linting tools (optional)
echo "Checking linting tools..."
if command -v black >/dev/null 2>&1; then
    echo -e "${GREEN}✓ black found${NC}"
else
    echo -e "${YELLOW}⚠ black not installed (optional)${NC}"
fi

if command -v isort >/dev/null 2>&1; then
    echo -e "${GREEN}✓ isort found${NC}"
else
    echo -e "${YELLOW}⚠ isort not installed (optional)${NC}"
fi

if command -v flake8 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ flake8 found${NC}"
else
    echo -e "${YELLOW}⚠ flake8 not installed (optional)${NC}"
fi
echo ""

# Summary
echo "=== Validation Summary ==="
echo -e "${GREEN}✓ All workflows are valid${NC}"
echo -e "${GREEN}✓ All tests pass${NC}"
echo -e "${GREEN}✓ Ready for CI/CD${NC}"
echo ""
echo "You can safely push your changes."
