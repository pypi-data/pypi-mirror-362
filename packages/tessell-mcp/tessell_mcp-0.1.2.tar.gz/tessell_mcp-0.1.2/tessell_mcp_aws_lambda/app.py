"""
app.py - AWS Lambda Entrypoint for Tessell MCP Server

This file serves as the entry point for deploying the Tessell MCP (Model Context Protocol) server on AWS Lambda.

Key Points:
- This entrypoint is designed specifically for AWS Lambda environments and expects Lambda-style event and context arguments.
- It exposes the `handler` function, which is the Lambda-compatible handler expected by AWS.
- The handler supports both legacy tool invocation (with a 'tool' key in the payload) and JSON-RPC 2.0 requests for modern, flexible API usage.
- Health checks are supported via the `/health` path for integration with AWS health monitoring and deployment templates.
- All business logic, tool registration, and server configuration are handled via imports from the main MCP server and tools modules.
- Logging is configured for operational visibility in cloud environments.

For local development, testing, or running as a standalone server, use a different entrypoint (such as main.py).
"""

import json
import logging
import asyncio
from typing import Any, Dict

from mcp.types import TextContent

from mcp_core.auth_config import TessellAuthConfig
from mcp_core.context import auth_config_var
from mcp_core.mcp_server import mcp
from mcp_core.tools.availability_machine import *
from mcp_core.tools.services import *

# Configure logging
log = logging.getLogger("mcp")
log.setLevel(logging.INFO)

async def _rpc_dispatch(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle JSON-RPC requests.
    """
    req_id = body.get("id")
    method = body.get("method", "")
    params = body.get("params") or {}

    if method == "tools/list":
        tools = [t.dict() for t in await mcp.list_tools()]
        return {"jsonrpc": "2.0", "result": tools, "id": req_id}

    try:
        result = await mcp.call_tool(method, params)
        payload = [c.dict() if isinstance(c, TextContent) else c for c in result]
        return {"jsonrpc": "2.0", "result": payload, "id": req_id}
    except Exception as exc:
        log.exception("RPC dispatch error")
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32000, "message": str(exc)},
            "id": req_id,
        }
    
def lambda_handler(event: Dict[str, Any], _ctx) -> Dict[str, Any]:
    """
    AWS Lambda handler for MCP server.
    """
    headers = event.get("headers") or {}
    #TODO: Caller should also pass base URL or should be derived from headers
    #base_url = headers.get("x-base-url", "")
    
    jwt_token = headers.get("authorization", "")
    tenant_id = headers.get("x-tenant", "")

    log.info(f"Authorization (token only)= {jwt_token} | X-Tenant={tenant_id}")

    # Create TessellApiConfig instance for this request
    api_config = TessellAuthConfig(jwt_token=jwt_token, tenant_id=tenant_id)

    #TODO: Uncomment once base_url is passed or derived
    # api_confg = TessellAuthConfig(base_url=base_url, jwt_token=jwt_token, tenant_id=tenant_id)

    # Set per-request config in contextvar
    auth_config_var.set(api_config)

    # Health check
    if event.get("rawPath") == "/health":
        return {"statusCode": 200, "body": json.dumps({"status": "ok"})}

    body: Any = event.get("body") if "body" in event else event
    if isinstance(body, str):
        body = json.loads(body or "{}")

    # Legacy style
    if isinstance(body, dict) and "tool" in body:
        try:
            result = asyncio.run(mcp.call_tool(body["tool"], body.get("args", {})))
            payload = [c.dict() if isinstance(c, TextContent) else c for c in result]
            return {"statusCode": 200, "body": json.dumps({"status": "success", "result": payload})}
        except Exception as exc:
            log.exception("legacy tool error")
            return {"statusCode": 200, "body": json.dumps({"status": "error", "error": str(exc)})}

    # JSON-RPC style
    if isinstance(body, dict) and body.get("jsonrpc") == "2.0":
        response = asyncio.run(_rpc_dispatch(body))
        return {"statusCode": 200, "body": json.dumps(response)}

    # Bad payload
    return {"statusCode": 400, "body": json.dumps({"error": "Unrecognized payload"})}


# AWS Lambda expects this name
handler = lambda_handler
