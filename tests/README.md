# Tests

This directory contains comprehensive tests for the Primavera P6 MCP Server.

## Running Tests

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_endpoints.py

# Run with coverage
python -m pytest --cov=src --cov-report=html
```

## Test Coverage

- **test_endpoints.py**: Tests all HTTP endpoints including:
  - Health endpoint response and headers
  - MCP manifest endpoint with proper headers
  - Tool schema endpoint
  - CORS OPTIONS requests
  - HEAD requests for manifest

## Dependencies

- pytest (included in requirements.txt)
