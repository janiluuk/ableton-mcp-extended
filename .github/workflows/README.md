# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the Ableton MCP Extended project.

## Workflows

### 1. CI - Tests (`ci-tests.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Jobs:**

#### Unit Tests
- Runs on Python 3.10, 3.11, and 3.12
- Executes all unit tests (excluding e2e)
- Generates coverage reports
- Uploads coverage to Codecov

#### Lint
- Checks code formatting with Black
- Checks import sorting with isort
- Lints with flake8
- Validates Python syntax

#### E2E Tests
- Starts mock UVR5 and RVC servers using `docker compose`
- Runs end-to-end integration tests
- Tests service health and connectivity
- Cleans up containers after tests
- **Note**: Uses `docker compose` (space) as it's now standard in GitHub Actions runners

#### Docker Build
- Builds all Docker images
- Tests mock server containers
- Validates container health

#### Security Scan
- Runs Safety for dependency vulnerabilities
- Runs Bandit for security issues
- Reports findings (non-blocking)

**Usage:**
```bash
# Automatically runs on push/PR
# Manual trigger:
# Go to Actions → CI - Tests → Run workflow
```

### 2. Release - Version & Publish (`release.yml`)

**Triggers:**
- Push to `main` branch (excluding docs/examples)
- Manual workflow dispatch with version bump selection

**Jobs:**

#### Check Version
- Detects if version bump is needed
- Calculates new version number
- Supports major, minor, patch bumps

#### Test Before Release
- Runs full test suite
- Verifies all imports work
- Ensures quality before release

#### Create Release
- Updates version in pyproject.toml
- Creates git commit and tag
- Generates release notes
- Creates GitHub release
- Builds distribution packages
- Uploads wheel and source dist

#### Notify Release
- Creates summary with release info
- Provides next steps

**Usage:**
```bash
# Manual release with version bump:
# 1. Go to Actions → Release
# 2. Click "Run workflow"
# 3. Select version bump type (major/minor/patch)
# 4. Click "Run workflow"

# Automatic release:
# - Merge to main triggers automatic patch version bump
```

**Version Bump Types:**
- **major**: 1.0.0 → 2.0.0 (breaking changes)
- **minor**: 1.0.0 → 1.1.0 (new features)
- **patch**: 1.0.0 → 1.0.1 (bug fixes)

### 3. PR - Merge Checks (`pr-checks.yml`)

**Triggers:**
- Pull request opened, synchronized, reopened, or ready for review

**Jobs:**

#### PR Validation
- Checks PR title format (conventional commits)
- Validates PR description exists
- Auto-labels based on changed files

#### Quick Tests
- Fast unit test execution
- Python syntax validation
- Fails fast on first error

#### Size Check
- Counts files and lines changed
- Warns on large PRs
- Suggests splitting if needed

#### Dependency Check
- Detects dependency changes
- Tests installation
- Checks for conflicts

#### Documentation Check
- Validates docs are updated with code
- Checks for broken links
- Warns on missing docs

#### Merge Ready
- Final summary when all checks pass
- Lists completed checks

**Usage:**
```bash
# Automatically runs on all PRs
# No manual intervention needed
```

## Workflow Best Practices

### For Contributors

1. **Before creating PR:**
   - Run tests locally: `make test-unit`
   - Check formatting: `black --check .`
   - Ensure docs are updated

2. **PR Title Format:**
   - Use conventional commits: `type(scope): description`
   - Examples:
     - `feat: add LocalAI integration`
     - `fix(comfyui): resolve workflow loading`
     - `docs: update usage examples`

3. **PR Description:**
   - Always include description
   - List changes made
   - Mention related issues

### For Maintainers

1. **Merging PRs:**
   - Ensure all checks pass
   - Review code and tests
   - Update version if needed
   - Merge to `develop` first for testing

2. **Creating Releases:**
   - Merge `develop` to `main`
   - Run release workflow manually
   - Select appropriate version bump
   - Verify release notes

3. **Monitoring:**
   - Check Actions tab regularly
   - Review failed workflows
   - Update workflows as needed

## Local Testing

Test workflows locally with [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run CI workflow
act -j unit-tests

# Run PR checks
act pull_request -j quick-tests

# List available workflows
act -l
```

## Secrets Required

### Optional Secrets

- `CODECOV_TOKEN` - For coverage uploads (optional)

### Automatic Secrets

- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

## Status Badges

Add to README.md:

```markdown
![CI Tests](https://github.com/janiluuk/ableton-mcp-extended/workflows/CI%20-%20Tests/badge.svg)
![Release](https://github.com/janiluuk/ableton-mcp-extended/workflows/Release%20-%20Version%20%26%20Publish/badge.svg)
```

## Troubleshooting

### Workflow Fails

1. **Check logs:**
   - Go to Actions tab
   - Click on failed workflow
   - Expand failed step
   - Review error messages

2. **Common issues:**
   - **Import errors**: Check dependencies in pyproject.toml
   - **Test failures**: Run tests locally first
   - **Docker issues**: Check docker-compose.yml
   - **Permission errors**: Check GITHUB_TOKEN permissions

### Manual Workflow Trigger

1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Select branch
5. Fill in inputs if required
6. Click "Run workflow"

### Cancel Running Workflow

1. Go to Actions tab
2. Click on running workflow
3. Click "Cancel workflow"

## Workflow Maintenance

### Updating Python Version

Update in all workflow files:
```yaml
python-version: ['3.10', '3.11', '3.12']  # Update here
```

### Updating Dependencies

1. Update `pyproject.toml`
2. Test locally
3. Push changes
4. Workflows will use new dependencies

### Adding New Tests

1. Add test files to `tests/`
2. Mark e2e tests: `@pytest.mark.e2e`
3. Workflows automatically include them

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

## Support

For workflow issues:
1. Check this documentation
2. Review workflow logs
3. Check GitHub Actions status
4. Open issue if problem persists
