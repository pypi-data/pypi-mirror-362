# PyPI Publishing Guide

This document covers how to publish the Lunar Times package to the Python Package Index (PyPI).

## Package Configuration

The project is now configured for PyPI publishing with the following improvements:

### ✅ **What's Already Configured**

1. **Consolidated Author Information**
   - Author: Luis Cortés
   - Email: `cscortes@users.noreply.github.com` (GitHub noreply email for privacy)
   - Both `pyproject.toml` and `__init__.py` use consistent information

2. **PyPI-Ready Metadata**
   - Proper package name: `lunar-times`
   - Rich classifiers for discoverability
   - Keywords for searchability
   - MIT license with proper file reference
   - Markdown README with content-type specification

3. **Python Version Support**
   - Supports Python 3.8+ (broadened from 3.8-only)
   - Classifiers for Python 3.8, 3.9, 3.10, 3.11, 3.12

4. **Build System**
   - Uses modern `hatchling` build backend
   - Proper package structure with `src/` layout
   - Command-line script entry point: `lunar-times`

5. **Development Dependencies**
   - Added `twine==5.1.1` for PyPI uploads
   - All necessary dev tools included

## Pre-Publishing Checklist

### 🔧 **Required Updates Before Publishing**

1. **Update Contact Information**
   ```toml
   # In pyproject.toml, current configuration:
   {name = "Luis Cortés", email = "cscortes@users.noreply.github.com"}
   # Using GitHub noreply email for privacy protection
   ```

2. **Update URLs (Optional)**
   ```toml
   # Real URLs (already configured in pyproject.toml):
   [project.urls]
   Homepage = "https://github.com/cscortes/lunar-times"
   Repository = "https://github.com/cscortes/lunar-times"
   Documentation = "https://github.com/cscortes/lunar-times/tree/main/docs"
   Issues = "https://github.com/cscortes/lunar-times/issues"
   Changelog = "https://github.com/cscortes/lunar-times/blob/main/docs/CHANGELOG.md"
   ```

3. **Update Version** (if needed)
   - Current version: `0.5.0`
   - Update in both `pyproject.toml` and `src/lunar_times/__init__.py`

4. **Final Quality Checks**
   ```bash
   make check      # Run all quality checks (includes invisible character check)
   make test       # Ensure all tests pass
   make lint       # Check code style
   ```

## PyPI Account Setup

### 1. **Create PyPI Accounts**
- **Test PyPI**: https://test.pypi.org/account/register/
- **Real PyPI**: https://pypi.org/account/register/

### 2. **Generate API Tokens**
- Go to Account Settings → API tokens
- Create tokens for both TestPyPI and PyPI
- Set as environment variables:
  ```bash
  export TWINE_USERNAME=__token__
  export TWINE_PASSWORD=pypi-your-test-token-here    # For TestPyPI
  export TWINE_PASSWORD=pypi-your-real-token-here    # For PyPI
  ```

## Invisible Character Protection

The build process automatically removes invisible characters that can cause issues:

- **Automatic Cleanup**: `make build-package` runs `pre-publish-clean` automatically
- **Manual Check**: `make check-invisible` to scan for invisible characters
- **Manual Clean**: `make clean-invisible` to remove with backups
- **Documentation**: See `scripts/invisible_chars_commands.md` for manual detection methods

All PyPI packages are guaranteed clean of problematic invisible characters.

## Publishing Process

### 1. **Build and Test Package**
```bash
# Install development dependencies
make setup

# Build the package
make build-package

# Check package integrity
make check-package
```

### 2. **Test Upload to TestPyPI**
```bash
# Upload to Test PyPI first
make upload-test-pypi

# Test installation from TestPyPI
pip install -i https://test.pypi.org/simple/ lunar-times
```

### 3. **Upload to Real PyPI**
```bash
# Only when you're confident everything works
make upload-pypi
```

## Available Make Targets

| Target | Description |
|--------|-------------|
| `make build-package` | Build wheel and source distribution (includes invisible char cleanup) |
| `make check-package` | Validate package integrity with twine |
| `make upload-test-pypi` | Upload to Test PyPI |
| `make upload-pypi` | Upload to real PyPI (with confirmation) |
| `make check-invisible` | Check for invisible characters in source files |
| `make clean-invisible` | Remove invisible characters (with backups) |
| `make pre-publish-clean` | Proactive cleanup for publishing |

## Package Installation

Once published, users can install with:

```bash
# Install from PyPI
pip install lunar-times

# Run the application
lunar-times
```

## Troubleshooting

### Common Issues

1. **Email configured**: Now using `cscortes@users.noreply.github.com` for privacy
2. **Authentication errors**: Check API tokens and environment variables
3. **Package name conflicts**: Check if name is available on PyPI
4. **Build errors**: Run `make check` to verify all quality checks pass

### Version Updates

For subsequent releases:

1. **Update version** in `pyproject.toml` and `__init__.py`
2. **Update CHANGELOG.md** with new version entry
3. **Commit changes** and tag the release
4. **Rebuild and re-upload**:
   ```bash
   make clean
   make build-package
   make upload-pypi
   ```

## Package Management Best Practices

1. **Semantic Versioning**: Follow MAJOR.MINOR.PATCH format
2. **Changelog**: Keep detailed changelog with each release
3. **Testing**: Always test on TestPyPI first
4. **Documentation**: Keep README.md updated and comprehensive
5. **Quality**: Maintain 100% test coverage and clean linting

## Security Considerations

- **Never commit API tokens** to version control
- **Use environment variables** for sensitive information
- **Enable 2FA** on PyPI accounts
- **Use API tokens** instead of passwords
- **Rotate tokens** periodically

## Next Steps

1. Replace placeholder email with real contact information
2. Set up PyPI accounts and generate API tokens
3. Test the build process: `make build-package`
4. Upload to TestPyPI first: `make upload-test-pypi`
5. If everything works, upload to PyPI: `make upload-pypi`

## Automated CI/CD Publishing

The project includes GitHub Actions workflows for automated PyPI publishing:

### Automated Release Process
1. **Version Tag**: Create and push a version tag (e.g., `git tag v0.6.0`)
2. **CI Pipeline**: GitHub Actions automatically runs full test suite
3. **Test PyPI**: Package is first published to Test PyPI for validation
4. **Production PyPI**: After validation, package is published to production PyPI
5. **GitHub Release**: Automatic GitHub release creation with changelog

### Release Workflow Features
- **Version Validation**: Ensures tag matches package version in `pyproject.toml`
- **Full Testing**: Runs complete CI pipeline before publishing
- **Two-Stage Deployment**: Test PyPI → Production PyPI
- **Installation Testing**: Validates package installation from Test PyPI
- **Release Notes**: Automatic GitHub release with changelog integration

### Setting Up Automated Publishing
1. **Add secrets** to your GitHub repository:
   ```
   PYPI_API_TOKEN=your_production_pypi_token
   TEST_PYPI_API_TOKEN=your_test_pypi_token
   ```

2. **Create version tag**:
   ```bash
   git tag v0.6.0
   git push origin v0.6.0
   ```

3. **Monitor release**: Check GitHub Actions tab for progress

### Manual Override
You can still use manual publishing:
```bash
make upload-test-pypi    # Manual Test PyPI upload
make upload-pypi    # Manual production PyPI upload
```

The automated pipeline provides safer, more reliable releases with comprehensive validation.

## Summary

The package is now properly configured and ready for PyPI publishing once you complete the contact information updates! 