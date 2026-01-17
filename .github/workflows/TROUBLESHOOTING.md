# Troubleshooting GitHub Actions Workflows

This guide helps diagnose and fix common issues with the GitHub Actions workflows.

## Quick Diagnostics

### Local Validation

Run the validation script before pushing:

```bash
bash .github/workflows/validate.sh
```

This will check:
- YAML syntax
- Unit tests
- Python syntax
- Coverage generation
- Linting tools

### Common Issues and Solutions

#### 1. GitHub Actions Context Injection Errors

**Symptoms:**
- Shell errors like `command not found`, `Permission denied`
- Seeing file paths being executed as commands
- Errors mentioning `$:`, `docker-compose:`, file paths
- Error code 126 or 127

**Example Error:**
```
/home/runner/work/_temp/script.sh: line 174: docker-compose:: command not found
/home/runner/work/_temp/script.sh: line 174: .github/workflows/ci-tests.yml: Permission denied
Error: Process completed with exit code 126.
```

**Cause:**
- Using `${{ github.event.* }}` directly in shell scripts
- PR body/title with special characters gets interpreted as shell commands
- Unsafe variable interpolation in YAML

**Solution:**

❌ **WRONG** - Direct interpolation:
```yaml
- name: Check PR
  run: |
    PR_BODY="${{ github.event.pull_request.body }}"
    echo "$PR_BODY"
```

✅ **CORRECT** - Use environment variables:
```yaml
- name: Check PR
  env:
    PR_BODY: ${{ github.event.pull_request.body }}
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    echo "Title: $PR_TITLE"
    echo "Has description: $([ -z "$PR_BODY" ] && echo "No" || echo "Yes")"
```

**Why this works:**
- `env:` section handles escaping automatically
- Shell variables are properly quoted
- No direct execution of user input

#### 2. Tests Pass Locally But Fail in CI

**Symptoms:**
- All tests pass with `pytest` locally
- CI fails with test errors

**Causes:**
- Different Python versions
- Missing dependencies
- Environment variables not set
- pytest-asyncio version mismatch

**Solutions:**

```bash
# Test with multiple Python versions locally
python3.10 -m pytest tests/ -v -m "not e2e"
python3.11 -m pytest tests/ -v -m "not e2e"
python3.12 -m pytest tests/ -v -m "not e2e"

# Check pytest-asyncio configuration
# Make sure pytest.ini has:
asyncio_mode = auto

# Verify dependencies
pip install -e ".[dev]"
pip list | grep pytest
```

#### 2. Git Diff Commands Fail in PR Checks

**Symptoms:**
- `git diff origin/${{ github.base_ref }}...HEAD` fails
- "ambiguous argument" errors

**Cause:**
- Missing `fetch-depth: 0` in checkout action

**Solution:**

```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Required for git diff
```

#### 3. Labeler Action Fails

**Symptoms:**
- PR validation job fails on "Label PR based on files changed"

**Causes:**
- Missing `.github/labeler.yml`
- Incorrect labeler configuration
- Wrong action version

**Solution:**

```yaml
# Verify labeler.yml exists
ls -la .github/labeler.yml

# Use correct action version
- name: Label PR based on files changed
  uses: actions/labeler@v5
  with:
    repo-token: ${{ secrets.GITHUB_TOKEN }}
```

#### 4. Coverage Upload Fails

**Symptoms:**
- Tests pass but coverage upload to Codecov fails

**Cause:**
- Missing `coverage.xml` file
- Wrong file path

**Solution:**

```yaml
# Generate coverage XML
pytest tests/ --cov=. --cov-report=xml

# Verify file exists before upload
- name: Check coverage file
  run: ls -la coverage.xml

# Upload with correct path
- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml  # Relative to repo root
    fail_ci_if_error: false  # Don't fail CI on upload errors
```

#### 5. Release Workflow Version Bump Fails

**Symptoms:**
- Release workflow fails at version bump step

**Causes:**
- pyproject.toml format issues
- Insufficient permissions
- Git config not set

**Solution:**

```yaml
# Ensure proper git config
- name: Configure git
  run: |
    git config --local user.email "github-actions[bot]@users.noreply.github.com"
    git config --local user.name "github-actions[bot]"

# Verify pyproject.toml format
- name: Get version
  run: |
    CURRENT_VERSION=$(grep -oP 'version = "\K[^"]+' pyproject.toml)
    echo "Found version: $CURRENT_VERSION"
```

#### 6. Docker Build Fails in E2E Tests

**Symptoms:**
- Docker build step fails
- "Cannot connect to Docker daemon" error

**Causes:**
- Docker not started
- Wrong Docker socket permissions
- Missing Dockerfile

**Solution:**

```yaml
# Set up Docker properly
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

# Verify Docker is running
- name: Check Docker
  run: docker info

# Build with proper context
- name: Build image
  run: docker build -t my-image:test -f docker/service/Dockerfile docker/service/
```

## Debugging Workflow Runs

### View Workflow Logs

1. Go to Actions tab in GitHub
2. Click on failed workflow
3. Click on failed job
4. Expand failed step
5. Review error messages

### Enable Debug Logging

Add to workflow file:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### Test Workflow Locally

Use [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# List workflows
act -l

# Run specific job
act -j unit-tests

# Run with event
act pull_request -j quick-tests
```

## Workflow-Specific Issues

### CI Tests Workflow

**Issue: Linting fails**

```bash
# Run locally to see errors
black --check localai_mcp/ comfyui_mcp/ uvr5_mcp/ rvc_mcp/
isort --check-only localai_mcp/ comfyui_mcp/ uvr5_mcp/ rvc_mcp/
flake8 localai_mcp/ comfyui_mcp/ uvr5_mcp/ rvc_mcp/

# Fix issues
black localai_mcp/ comfyui_mcp/ uvr5_mcp/ rvc_mcp/
isort localai_mcp/ comfyui_mcp/ uvr5_mcp/ rvc_mcp/
```

**Issue: E2E tests fail**

```bash
# Start services locally
docker-compose up -d uvr5-mock rvc-mock

# Wait for services
sleep 30

# Run E2E tests
pytest tests/test_e2e_integration.py -v

# Check service logs
docker-compose logs uvr5-mock
docker-compose logs rvc-mock

# Cleanup
docker-compose down -v
```

### Release Workflow

**Issue: Permission denied on push**

Add to workflow:

```yaml
permissions:
  contents: write  # Required for pushing commits and tags
```

**Issue: Release already exists**

```bash
# Check existing releases
gh release list

# Delete if needed (careful!)
gh release delete v1.0.0

# Delete tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### PR Checks Workflow

**Issue: Size check fails**

The size check doesn't fail the workflow, it just warns. If it's failing:

```yaml
# Make sure warnings don't exit with error
- name: Check PR size
  run: |
    # ... commands ...
    exit 0  # Always succeed
```

## Performance Issues

### Slow Test Execution

```yaml
# Run tests in parallel (if supported)
pytest tests/ -n auto

# Use test markers to run subsets
pytest tests/ -m "not slow"

# Cache dependencies
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # Caches pip dependencies
```

### Slow Docker Builds

```yaml
# Use Docker layer caching
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    driver-opts: |
      image=moby/buildkit:latest

# Use cache from registry
- name: Build with cache
  uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Getting Help

### Check Status

1. **GitHub Status**: https://www.githubstatus.com/
2. **Actions Status**: Check if GitHub Actions are operational

### Review Logs

```bash
# Get workflow run logs via CLI
gh run list
gh run view <run-id>
gh run view <run-id> --log
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Process completed with exit code 1` | Command failed | Check command output |
| `Unable to resolve action` | Wrong action version | Update action version |
| `Resource not accessible by integration` | Missing permissions | Add required permissions |
| `ambiguous argument` | Git ref not found | Add `fetch-depth: 0` |
| `No module named 'pytest'` | Dependencies not installed | Run `pip install -e ".[dev]"` |

## Prevention

### Before Pushing

1. Run validation script: `bash .github/workflows/validate.sh`
2. Run all tests: `pytest tests/ -v`
3. Check YAML syntax: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci-tests.yml'))"`
4. Test with act (if installed): `act -j unit-tests`

### Best Practices

1. **Always use pinned action versions**: `uses: actions/checkout@v4` not `@main`
2. **Add timeouts**: `timeout-minutes: 30` to prevent hanging jobs
3. **Use conditionals**: Skip unnecessary jobs with `if:` conditions
4. **Cache dependencies**: Use `cache:` in setup actions
5. **Fail fast**: Use `-x` flag in pytest for quick feedback

## Support

If issues persist:

1. Check this troubleshooting guide
2. Review workflow logs in GitHub Actions
3. Test locally with validation script
4. Check GitHub Actions status
5. Open an issue with:
   - Workflow name
   - Error message
   - Workflow run URL
   - Local test results
