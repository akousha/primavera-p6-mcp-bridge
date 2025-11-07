"""
Primavera P6 MCP Server
FastAPI-based Model Context Protocol server for Oracle Primavera P6 integration
"""
from datetime import datetime
from typing import Dict, Optional, List, Any
import os
import json
import time

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import requests

# Version
VERSION = "1.0.0"

# Environment configuration
P6_BASE_URL = os.getenv("P6_BASE_URL", "https://ca1.p6.oraclecloud.com/metrolinx/p6ws/restapi")

# MCP Manifest Headers (DRY principle)
MANIFEST_HEADERS = {
    "Content-Type": "application/json",
    "Cache-Control": "public, max-age=3600",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
    "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'",
    "X-Content-Type-Options": "nosniff"
}

def _manifest_response(content: dict) -> JSONResponse:
    """Helper to create manifest responses with consistent headers"""
    return JSONResponse(content=content, headers=MANIFEST_HEADERS)

# FastAPI app setup
app = FastAPI(
    title="Primavera P6 MCP Server",
    description="Model Context Protocol server for Oracle Primavera P6 integration",
    version=VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"],
    allow_headers=["*"],
    max_age=600
)

# Session management
sessions = {}

class LoginRequest(BaseModel):
    username: str
    password: str
    databaseName: str
    remember: bool = False

class HealthResponse(BaseModel):
    ok: bool
    status: str
    time: int
    timestamp: str
    base: str
    auto_session_enabled: bool
    auto_session_strict_mode: bool
    mcp_ready: bool
    version: str
    sessions: List[str]
    endpoints: Dict[str, str]

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    response_data = {
        "ok": True,
        "status": "healthy",
        "time": int(time.time()),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "base": P6_BASE_URL,
        "auto_session_enabled": True,
        "auto_session_strict_mode": True,
        "mcp_ready": True,
        "version": VERSION,
        "sessions": list(sessions.keys()),
        "endpoints": {
            "mcp_manifest": "/.well-known/mcp.json",
            "tool_schema": "/tool_schema.json",
            "login": "/login",
            "call": "/call",
            "obs_find": "/obs/find",
            "projects_by_obs": "/projects/by_obs"
        }
    }
    
    return JSONResponse(
        content=response_data,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/.well-known/mcp.json")
async def mcp_manifest(request: Request):
    """MCP manifest endpoint"""
    base_url = str(request.base_url).rstrip('/')
    
    manifest = {
        "schema_version": "1.0",
        "name": "primavera-p6-mcp-server",
        "description": "Oracle Primavera P6 MCP Server for project management",
        "version": VERSION,
        "tools": [
            {
                "name": "p6_login",
                "description": "Login to Oracle P6 and start a session",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "P6 username"},
                        "password": {"type": "string", "description": "P6 password"},
                        "databaseName": {"type": "string", "description": "P6 database name"}
                    },
                    "required": ["username", "password", "databaseName"]
                }
            },
            {
                "name": "p6_obs_find",
                "description": "Search for OBS (Organizational Breakdown Structure) by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {"type": "string", "description": "Search query for OBS name"}
                    },
                    "required": ["q"]
                }
            },
            {
                "name": "p6_projects_by_obs",
                "description": "List projects that belong to a given OBS",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "obs_name": {"type": "string", "description": "OBS name to search for"}
                    },
                    "required": ["obs_name"]
                }
            }
        ],
        "api": {
            "type": "rest",
            "base_url": base_url
        }
    }
    
    return _manifest_response(manifest)

@app.options("/.well-known/mcp.json")
async def mcp_manifest_options():
    """Handle CORS preflight for manifest"""
    return _manifest_response({"status": "ok"})

@app.head("/.well-known/mcp.json")
async def mcp_manifest_head():
    """Handle HEAD requests for manifest"""
    return Response(headers=MANIFEST_HEADERS)

@app.get("/tool_schema.json")
async def tool_schema():
    """Tool schema endpoint for MCP clients"""
    schema = {
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "p6_login",
                    "description": "Login to Oracle P6 and start a session. Set remember=true to enable auto-relogin.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                            "databaseName": {"type": "string"},
                            "remember": {"type": "boolean", "default": False}
                        },
                        "required": ["username", "password", "databaseName"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "p6_obs_find",
                    "description": "Fuzzy search OBS by name (LIKE %q%). session_id is optional if auto-session is enabled.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "session_id": {"type": "string"},
                            "q": {"type": "string"},
                            "fields": {"type": "string", "default": "CreateDate,CreateUser,Description,GUID,LastUpdateDate,LastUpdateUser,Name,ObjectId,ParentObjectId,SequenceNumber"},
                            "order_by": {"type": "string", "default": "Name"},
                            "limit": {"type": "integer", "default": 50}
                        },
                        "required": ["q"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "p6_projects_by_obs",
                    "description": "List projects that belong to a given OBS (by name or id). session_id is optional if auto-session is enabled.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "session_id": {"type": "string"},
                            "obs_name": {"type": "string"},
                            "obs_id": {"type": "string"},
                            "fields": {"type": "string", "default": "Id,Code,Name,StartDate,FinishDate,GUID,Status,OBSObjectId"},
                            "order_by": {"type": "string", "default": "Name"},
                            "limit": {"type": "integer", "default": 100}
                        }
                    }
                }
            }
        ],
        "tool_server": {
            "base_url": str(os.getenv("BASE_URL", "http://localhost:8000")),
            "endpoints": {
                "p6_login": {"method": "POST", "path": "/login"},
                "p6_obs_find": {"method": "GET", "path": "/obs/find"},
                "p6_projects_by_obs": {"method": "GET", "path": "/projects/by_obs"}
            }
        }
    }
    
    return JSONResponse(content=schema, headers={"Content-Type": "application/json"})

@app.post("/login")
async def login(login_request: LoginRequest):
    """Login to P6 and create session"""
    # This is a placeholder implementation
    # In the real implementation, this would authenticate with P6
    session_id = f"session_{int(time.time())}"
    sessions[session_id] = {
        "username": login_request.username,
        "database": login_request.databaseName,
        "remember": login_request.remember,
        "created": datetime.utcnow().isoformat()
    }
    
    return {
        "success": True,
        "session_id": session_id,
        "message": "Login successful (mock implementation)"
    }

@app.get("/obs/find")
async def obs_find(q: str, session_id: Optional[str] = None):
    """Search for OBS by name"""
    # Mock implementation
    return {
        "results": [
            {
                "Name": f"Mock OBS matching '{q}'",
                "ObjectId": 12345,
                "Description": "Mock OBS for testing"
            }
        ],
        "total": 1
    }

@app.get("/projects/by_obs")
async def projects_by_obs(obs_name: Optional[str] = None, obs_id: Optional[str] = None):
    """List projects by OBS"""
    # Mock implementation
    return {
        "results": [
            {
                "Id": 1,
                "Code": "PROJ001",
                "Name": f"Mock Project for OBS {obs_name or obs_id}",
                "Status": "Active"
            }
        ],
        "total": 1
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)