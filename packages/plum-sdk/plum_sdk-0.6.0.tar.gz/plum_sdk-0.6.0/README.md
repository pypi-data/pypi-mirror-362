# Plum SDK

Python SDK for Plum AI platform.

## Installation

```bash
pip install plum_sdk
```

## Development

### Prerequisites

- Python 3.6+
- pip
- build (`pip install build`)
- twine (`pip install twine`)
- black (`pip install black`)

### Setup

1. Clone the repository
2. Navigate to the SDK directory: `cd sdk`
3. Install development dependencies: `pip install -e .[dev]`

## Version Management, Building, and Publishing

### 1. Version Bumping

The SDK version is managed in `setup.py`. To bump the version:

1. Open `setup.py`
2. Update the `version` field:
   ```python
   setup(
       name="plum_sdk",
       version="0.5.1",  # Update this version number
       # ... rest of setup
   )
   ```

### Version Numbering Convention

Follow semantic versioning (semver):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

Examples:
- `0.5.0` → `0.5.1` (patch: bug fixes)
- `0.5.1` → `0.6.0` (minor: new features)
- `0.6.0` → `1.0.0` (major: breaking changes)

### 2. Building the Package

Before publishing, you need to build the package:

```bash
make build
```

This command will:
- Format code with black
- Clean previous builds
- Create a source distribution in `dist/`
- Show you the package contents for verification

You can manually verify the package contents with:
```bash
tar -tvf dist/*.tar.gz
```

### 3. Testing

Always run tests before publishing:

```bash
# Run unit tests only
make test

# Run export verification tests
make test-exports

# Run all tests
make test-all
```

### 4. Publishing to PyPI

#### Prerequisites for Publishing

1. **PyPI Account**: You need a PyPI account and appropriate permissions
2. **API Token**: Configure your PyPI API token in `~/.pypirc`:
   ```ini
   [distutils]
   index-servers = pypi

   [pypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmcC... # Your API token
   ```

#### Publishing Process

1. **Bump the version** in `setup.py`
2. **Test thoroughly**:
   ```bash
   make test-all
   ```
3. **Build the package**:
   ```bash
   make build
   ```
4. **Publish to PyPI**:
   ```bash
   make publish
   ```

#### Complete Release Workflow

For a complete release, you can use:

```bash
make all
```

This will run all tests, build the package, and test the installation.

### 5. Development Installation

To install the package in development mode for testing:

```bash
make install-dev
```

This will:
- Install the package in editable mode
- Test imports
- Uninstall the development package

## Available Make Commands

```bash
make help          # Show available commands
make test          # Run unit tests
make test-exports  # Run export verification tests
make test-all      # Run all tests
make build         # Build the package
make publish       # Publish to PyPI
make install-dev   # Install in development mode and test
make all           # Run tests, build, and install dev package
```

## Project Structure

```
sdk/
├── plum_sdk/           # Main package directory
│   ├── __init__.py     # Package initialization and exports
│   ├── models.py       # Data models
│   ├── plum_sdk.py     # Main SDK client
│   └── tests/          # Test suite
├── setup.py            # Package configuration
├── Makefile           # Build and test automation
└── README.md          # This file
```

## Testing

The SDK includes comprehensive tests:

- **Unit tests**: Test individual components
- **Integration tests**: Test SDK integration with the platform
- **Export verification**: Ensure all public APIs are properly exported

Run tests before every release to ensure quality and compatibility.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run the full test suite: `make test-all`
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Import errors**: Run `make test-exports` to verify all exports are working
2. **Build failures**: Ensure all dependencies are installed
3. **Publishing errors**: Check your PyPI credentials and network connection

### Getting Help

- Check the test output for specific error messages
- Review the Makefile for available commands
- Verify your Python environment and dependencies