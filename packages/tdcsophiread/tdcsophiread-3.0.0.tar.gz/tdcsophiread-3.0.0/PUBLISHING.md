# Publishing TDCSophiread to PyPI

This document describes how to publish the TDCSophiread Python package to PyPI with support for linux-64 and osx-arm64 platforms.

## Version Management

The package uses a single source of truth for versioning:

1. **Primary Version**: Defined in `include/version.h` (C++)
2. **Python Package**: Must be manually synced in `pyproject.toml`
3. **Sync Script**: Use `pixi run sync-version` to synchronize versions

### Updating the Version

1. Edit `include/version.h` to update version numbers:
   ```cpp
   #define VERSION_MAJOR 3
   #define VERSION_MINOR 0  
   #define VERSION_PATCH 1  // Increment this for patch releases
   ```

2. Run the sync script:
   ```bash
   pixi run sync-version
   ```

3. Commit the changes:
   ```bash
   git add include/version.h pyproject.toml src/tdcsophiread/_version.py
   git commit -m "Bump version to 3.0.1"
   git tag v3.0.1
   ```

## Local Testing

Before publishing, test the wheel locally:

```bash
# Build bundled wheel
pixi run build-wheel    # Creates wheel with all dependencies bundled

# Test the wheel
pixi run test-wheel     # Installs and tests import

# Build source distribution
pixi run build-sdist    # Creates source tarball
```

## Publishing Methods

### Method 1: GitHub Actions (Recommended)

The repository includes a GitHub Actions workflow (`.github/workflows/build-wheels.yml`) that automatically:
- Builds wheels for linux-64 and osx-arm64
- Builds source distribution  
- Publishes to PyPI on tag pushes

To use:

1. Set up PyPI API tokens in GitHub secrets:
   - `PYPI_API_TOKEN`: For publishing to PyPI
   - `TEST_PYPI_API_TOKEN`: For testing on Test PyPI

2. Push a version tag:
   ```bash
   git tag v3.0.1
   git push origin v3.0.1
   ```

3. The workflow will automatically build and publish

### Method 2: Manual Publishing

For manual publishing (requires PyPI account and API tokens):

```bash
# Set up PyPI credentials in ~/.pypirc or use environment variables
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your_pypi_api_token

# Build both wheel and source distribution
pixi run build-wheel
pixi run build-sdist

# Publish to Test PyPI first (recommended)  
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your_test_pypi_token
python -m twine upload --repository testpypi dist/*

# If testing succeeds, publish to PyPI
export TWINE_PASSWORD=your_pypi_token
pixi run publish-pypi
```


## Platform Support

The package currently supports:
- **Linux**: x86_64 (manylinux2014)
- **macOS**: ARM64 (Apple Silicon)

Python versions supported: 3.9, 3.10, 3.11, 3.12

## Dependencies

The wheels include these compiled dependencies:
- Eigen3 (header-only, compiled in)
- Intel TBB (dynamically linked)
- HDF5 (dynamically linked)
- nlohmann/json (header-only, compiled in)

Python dependencies are listed in `pyproject.toml` and installed automatically:
- numpy >= 2.3.0
- h5py >= 3.12.0  
- pydantic >= 2.11.7

## Troubleshooting

### Version Mismatch
If the Python package shows wrong version:
```bash
pixi run sync-version
pixi run clean
pixi run build
pixi run install
```

### Build Failures
For platform-specific build issues:
1. Check cibuildwheel logs in GitHub Actions
2. Verify all dependencies are available in pixi environment
3. Check that delocate is properly bundling dependencies

### Missing Dependencies
If wheels fail to work on target systems:
1. Check that TBB and HDF5 are properly bundled
2. Use `auditwheel` (Linux) or `delocate` (macOS) to verify dependencies
3. Update cibuildwheel configuration if needed

## Release Checklist

Before each release:

- [ ] Update version in `include/version.h`
- [ ] Run `pixi run sync-version`  
- [ ] Run `pixi run test` (C++ tests)
- [ ] Run `pixi run python-test` (Python tests)
- [ ] Test notebooks with new version
- [ ] Update CHANGELOG.md
- [ ] Commit and tag version
- [ ] Push tag to trigger CI/CD
- [ ] Verify packages on PyPI
- [ ] Test installation: `pip install tdcsophiread==X.Y.Z`

## Security Notes

- API tokens should never be committed to version control
- Use GitHub secrets for automated publishing
- Test PyPI should be used for initial testing
- All wheels are built in isolated environments