# Primavera P6 MCP Server - Copilot Instructions

This is a FastAPI-based Model Context Protocol (MCP) server for Oracle Primavera P6 integration.

## Project Context
- **Purpose**: MCP server that bridges ChatGPT/Claude to Oracle Primavera P6 REST API
- **Stack**: Python 3.12, FastAPI, Uvicorn, pytest
- **Deployment**: Docker, Railway platform
- **Architecture**: Clean separation with src/, tests/, docs/, docker/ structure

## Development Guidelines
- Use modern Python patterns and type hints
- Follow FastAPI best practices for API design
- Maintain comprehensive test coverage with pytest
- Use proper error handling and logging
- Follow MCP protocol specifications

## Key Components
- **src/main.py**: Main FastAPI application with MCP endpoints
- **src/models/**: Pydantic models for P6 data structures
- **src/utils/**: Helper functions and utilities
- **tests/**: Comprehensive endpoint and integration tests
- **docker/**: Containerization configs

## MCP Protocol Requirements
- Provide manifest at `/.well-known/mcp.json`
- Support tool schema endpoint
- Handle CORS properly for web clients
- Implement proper HTTP methods (GET, POST, OPTIONS, HEAD)
- Use consistent headers and caching strategies