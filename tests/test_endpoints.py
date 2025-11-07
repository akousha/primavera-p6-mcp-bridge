import json
import sys
import asyncio
from pathlib import Path
from typing import Dict

from starlette.requests import Request

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import main


def _assert_manifest_headers(headers: Dict[str, str]) -> None:
    """Helper to validate manifest headers"""
    normalized = {k.lower(): v for k, v in headers.items()}
    for key, value in main.MANIFEST_HEADERS.items():
        assert key.lower() in normalized
        assert normalized[key.lower()] == value


def test_health_endpoint_returns_status_payload_and_headers():
    """Test health endpoint functionality"""
    response = asyncio.run(main.health())
    assert response.status_code == 200

    payload = json.loads(response.body.decode())
    assert payload["ok"] is True
    assert payload["status"] == "healthy"
    assert payload["mcp_ready"] is True
    assert payload["endpoints"]["mcp_manifest"] == "/.well-known/mcp.json"

    assert response.headers["Cache-Control"] == "no-cache, no-store, must-revalidate"
    assert response.headers["Pragma"] == "no-cache"
    assert response.headers["Expires"] == "0"


def test_manifest_endpoint_serves_json_with_expected_headers():
    """Test MCP manifest endpoint"""
    request = Request({"type": "http", "headers": []})
    response = asyncio.run(main.mcp_manifest(request))
    assert response.status_code == 200

    manifest = json.loads(response.body.decode())
    assert manifest["schema_version"] == "1.0"
    assert manifest["name"] == "primavera-p6-mcp-server"
    assert manifest["api"]["type"] == "rest"

    _assert_manifest_headers(response.headers)


def test_tool_schema_endpoint_available():
    """Test tool schema endpoint"""
    response = asyncio.run(main.tool_schema())
    schema = json.loads(response.body.decode())
    assert "tools" in schema
    assert any(tool.get("function", {}).get("name") == "p6_login" for tool in schema["tools"])
    assert schema["tool_server"]["endpoints"]["p6_login"] == {"method": "POST", "path": "/login"}


def test_manifest_options_request_exposes_cors_headers():
    """Test CORS OPTIONS for manifest"""
    response = asyncio.run(main.mcp_manifest_options())
    assert response.status_code == 200

    headers = dict(response.headers)
    _assert_manifest_headers(headers)


def test_manifest_head_request_returns_manifest_headers():
    """Test HEAD request for manifest"""
    response = asyncio.run(main.mcp_manifest_head())
    assert response.status_code == 200
    _assert_manifest_headers(dict(response.headers))