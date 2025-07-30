# Pre-Commit Testing Guide

This guide provides comprehensive testing strategies to catch issues locally before committing to GitHub, avoiding CI failures and saving development time.

## Quick Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `make pre-commit` | Standard pre-commit checks | Before every commit |
| `make test-all-python` | Multi-Python version testing | Before major commits |
| `make test-github-actions` | Local GitHub Actions testing | Before workflow changes |
| `make quick-check` | Fast development checks | During development |

## Testing Strategies

### 1. **Daily Development Testing**

For regular development work:

```bash
# Quick checks during development
make quick-check

# Standard pre-commit checks
make pre-commit
```

**What it tests:**
- Code formatting (black)
- Linting (flake8)
- Type checking (mypy)  
- Unit tests (pytest)
- Invisible character detection

**Time:** ~30 seconds

### 2. **Comprehensive Multi-Python Testing**

For major commits or before releases:

```bash
# Test with all Python versions (3.8-3.12)
make test-all-python
```

**What it tests:**
- All standard checks across Python 3.8, 3.9, 3.10, 3.11, 3.12
- Dependency compatibility
- Version-specific linting differences
- Cross-platform compatibility

**Time:** ~5-10 minutes

**Interactive Options:**
1. **Test all versions** - Full CI simulation
2. **Test Python 3.12 only** - Quick check for recent linting issues
3. **Test specific version** - Debug version-specific issues

### 3. **GitHub Actions Local Testing**

For workflow changes or debugging CI issues:

```bash
# Test GitHub Actions workflows locally
make test-github-actions
```

**Requirements:**
- Docker installed and running
- [act](https://github.com/nektos/act) tool installed

**Installation:**
```bash
# Ubuntu/Debian
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# macOS
brew install act

# Arch Linux
yay -S act
```

## Common Testing Scenarios

### Scenario 1: Regular Code Changes

```bash
# During development
make quick-check

# Before committing
make pre-commit

# If all good, commit
git add .
git commit -m "Your commit message"
git push
```

### Scenario 2: Major Feature Addition

```bash
# Check code quality first
make lint

# Test with all Python versions
make test-all-python

# If all pass, commit
git add .
git commit -m "feat: major feature addition"
git push
```

### Scenario 3: Fixing Linting Issues

```bash
# Test specific Python version that failed
make test-all-python
# Choose option 3, enter specific version

# Fix issues, then test again
make test-all-python

# Commit the fix
git add .
git commit -m "fix: resolve linting issues"
git push
```

### Scenario 4: Workflow Changes

```bash
# Test workflows locally first
make test-github-actions

# If workflows pass, commit
git add .
git commit -m "ci: update GitHub Actions workflow"
git push
```

## Understanding Test Output

### Multi-Python Testing Output

```
🔍 Multi-Python Testing Script
==============================

Available Python versions for testing:
  ✓ Python 3.8.20
  ✓ Python 3.9.23
  ✓ Python 3.10.15
  ✓ Python 3.11.10
  ✓ Python 3.12.11

Select testing mode:
1. Test all versions (recommended before major commits)
2. Test Python 3.12 only (quick check for recent linting issues)
3. Test specific version
4. Exit
```

### Success Indicators

```
✓ Python 3.12.11: ALL TESTS PASSED
🎉 ALL PYTHON VERSIONS PASSED!
Safe to commit and push.
```

### Failure Indicators

```
❌ FAILED VERSIONS: 3.12.11
Fix issues before committing.
```

## Troubleshooting

### Common Issues

#### 1. **Linting Failures**
```
src/lunar_times/cli.py:168:35: E231 missing whitespace after ','
```

**Solution:** Fix formatting issues:
```bash
make lint    # Check code quality
make lint    # Check if fixed
```

#### 2. **Import Errors**
```
ModuleNotFoundError: No module named 'requests'
```

**Solution:** Reinstall dependencies:
```bash
make reset   # Clean and reinstall
make test    # Verify fix
```

#### 3. **Version-Specific Issues**
```
❌ Python 3.12 tests failed!
```

**Solution:** Test specific version:
```bash
make test-all-python  # Choose option 3
# Enter: 3.12.11
# Debug the specific issue
```

#### 4. **GitHub Actions Local Testing Issues**
```
❌ 'act' tool is not installed.
```

**Solution:** Install act tool:
```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Performance Tips

#### 1. **Parallel Testing**
- The multi-Python script runs tests in isolated environments
- Each Python version is tested independently
- Failed versions are reported at the end

#### 2. **Caching**
- Python versions are cached after first install
- Dependencies are cached per environment
- Subsequent runs are faster

#### 3. **Selective Testing**
- Use Python 3.12 only for quick linting checks
- Use full multi-Python testing for comprehensive validation
- Use GitHub Actions local testing only for workflow changes

## Best Practices

### Pre-Commit Workflow

1. **Always check code quality first:**
   ```bash
   make lint
   ```

2. **Run standard pre-commit checks:**
   ```bash
   make pre-commit
   ```

3. **For major changes, test all Python versions:**
   ```bash
   make test-all-python
   ```

4. **Only commit if all tests pass:**
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```

### Development Workflow

1. **Quick checks during development:**
   ```bash
   make quick-check
   ```

2. **Before each commit:**
   ```bash
   make pre-commit
   ```

3. **Before major releases:**
   ```bash
   make test-all-python
   make test-github-actions  # If workflows changed
   ```

### CI/CD Integration

The local testing mirrors the GitHub Actions CI pipeline:

1. **Quick Check** → **GitHub Actions Quick Check**
2. **Multi-Python Testing** → **GitHub Actions Matrix Testing**
3. **Local GitHub Actions** → **Actual GitHub Actions**

## Integration with Git Hooks

### Optional: Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running pre-commit checks..."
make pre-commit
```

```bash
chmod +x .git/hooks/pre-commit
```

### Optional: Pre-Push Hook

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash
echo "Running comprehensive tests before push..."
make test-all-python
```

```bash
chmod +x .git/hooks/pre-push
```

## Summary

Use this testing hierarchy:

1. **Development:** `make quick-check`
2. **Regular commits:** `make pre-commit` 
3. **Major changes:** `make test-all-python`
4. **Workflow changes:** `make test-github-actions`

This approach catches issues early, saves CI resources, and ensures reliable deployments.

---

*Last Updated: 2024-12-26*
*Version: 1.0* 