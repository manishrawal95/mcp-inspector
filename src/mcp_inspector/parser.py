"""Decodes and validates MCP message structure from raw byte streams into Python dictionaries."""

from __future__ import annotations

import json
from typing import Any


def parse_mcp(payload: bytes) -> dict[str, Any]:
    """Parse an MCP message from raw bytes into a structured dictionary.

    Handles both MCP requests and responses. Returns a dictionary with a
    ``type`` key of ``"request"``, ``"response"``, or ``"error"`` depending
    on the content.

    Args:
        payload: Raw bytes of the MCP JSON message.

    Returns:
        A dict with ``type`` and the relevant parsed fields.  On failure,
        returns ``{"type": "error", "message": "<reason>"}``.
    """
    try:
        data = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return {"type": "error", "message": f"Failed to decode JSON: {exc}"}

    if not isinstance(data, dict):
        return {"type": "error", "message": "Payload is not a JSON object"}

    mcp_version = data.get("mcp_version", "unknown")

    # --- request ---
    if "call" in data:
        call = data["call"]
        if not isinstance(call, dict):
            return {"type": "error", "message": "'call' field is not an object"}
        return {
            "type": "request",
            "mcp_version": mcp_version,
            "tool_name": call.get("tool_name", "unknown"),
            "function": call.get("function", "unknown"),
            "args": call.get("args", {}),
        }

    # --- response ---
    if "response" in data:
        resp = data["response"]
        if not isinstance(resp, dict):
            return {"type": "error", "message": "'response' field is not an object"}
        status = resp.get("status", "unknown")
        result: dict[str, Any] = {
            "type": "response",
            "mcp_version": mcp_version,
            "status": status,
        }
        if status == "success":
            result["data"] = resp.get("data", {})
        else:
            result["message"] = resp.get("message", "No error message provided")
        return result

    return {"type": "error", "message": "Unrecognised MCP message: missing 'call' or 'response' key"}
