# Primavera P6 MCP Server

A clean, professionally structured FastAPI-based Model Context Protocol (MCP) server for Oracle Primavera P6 integration.

## 🎯 Purpose

This server bridges ChatGPT, Claude, and other MCP clients to Oracle Primavera P6 REST API for project management data access.

## 🏗️ Architecture

```text
src/
├── main.py              # FastAPI application with MCP endpoints
├── models/              # Pydantic models for P6 data structures  
└── utils/               # Helper functions and utilities

tests/
├── test_endpoints.py    # Comprehensive endpoint tests
└── README.md           # Test documentation

docker/
├── Dockerfile          # Multi-stage containerization
└── docker-compose.yml  # Development environment

docs/                   # Project documentation
```

## 🚀 Quick Start

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python -m pytest tests/ -v
```

### Docker

```bash
# Build and run with Docker Compose
cd docker/
docker-compose up --build

# Or build directly
docker build -f docker/Dockerfile -t p6-mcp-server .
docker run -p 8000:8000 p6-mcp-server
```

### VS Code

Use the "Run P6 MCP Server" task from the Command Palette (`Ctrl+Shift+P` → `Tasks: Run Task`)

## 🔌 MCP Integration

### Endpoints

- **Health**: `GET /health` - Server status and configuration
- **MCP Manifest**: `GET /.well-known/mcp.json` - MCP protocol manifest  
- **Tool Schema**: `GET /tool_schema.json` - Available tools and endpoints
- **Login**: `POST /login` - Authenticate with P6
- **OBS Search**: `GET /obs/find` - Search organizational structures
- **Projects**: `GET /projects/by_obs` - List projects by OBS

### MCP Client Configuration

For ChatGPT or Claude, add this MCP connector:

```json
{
  "name": "Primavera P6",
  "url": "http://localhost:8000/.well-known/mcp.json"
}
```

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## 🛠️ Development

### Key Features

- ✅ **Clean Architecture**: Proper separation of concerns
- ✅ **Type Safety**: Full type hints with Pydantic models
- ✅ **CORS Support**: Cross-origin requests handled
- ✅ **Caching**: Efficient manifest caching strategy
- ✅ **Security**: Content Security Policy headers
- ✅ **Testing**: Comprehensive endpoint coverage
- ✅ **Docker**: Production-ready containerization

### MCP Protocol Compliance

- ✅ Manifest served at `/.well-known/mcp.json`
- ✅ Tool schema endpoint available
- ✅ Proper HTTP methods (GET, POST, OPTIONS, HEAD)
- ✅ CORS headers for web clients
- ✅ Consistent response headers and caching

## 📚 API Documentation

When running, visit `http://localhost:8000/docs` for interactive API documentation (FastAPI automatic docs).

## 🔧 Configuration

Environment variables:

- `P6_BASE_URL`: Oracle Primavera P6 REST API base URL
- `PORT`: Server port (default: 8000)

## 📝 License

This project is part of the Primavera P6 MCP integration suite.
