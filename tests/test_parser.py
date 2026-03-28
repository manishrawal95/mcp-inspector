"""Unit tests for the MCP parser."""

from __future__ import annotations

import json

from mcp_inspector.parser import parse_mcp


class TestParseRequest:
    """Tests for valid MCP request parsing."""

    def test_valid_request(self) -> None:
        payload = json.dumps({
            "mcp_version": "1.0",
            "call": {
                "tool_name": "weather",
                "function": "get_current_temp",
                "args": {"location": "SF"},
            },
        }).encode()

        result = parse_mcp(payload)

        assert result["type"] == "request"
        assert result["mcp_version"] == "1.0"
        assert result["tool_name"] == "weather"
        assert result["function"] == "get_current_temp"
        assert result["args"] == {"location": "SF"}

    def test_request_missing_optional_fields(self) -> None:
        payload = json.dumps({
            "mcp_version": "1.0",
            "call": {},
        }).encode()

        result = parse_mcp(payload)

        assert result["type"] == "request"
        assert result["tool_name"] == "unknown"
        assert result["function"] == "unknown"
        assert result["args"] == {}


class TestParseResponse:
    """Tests for valid MCP response parsing."""

    def test_success_response(self) -> None:
        payload = json.dumps({
            "mcp_version": "1.0",
            "response": {
                "status": "success",
                "data": {"temp": 72},
            },
        }).encode()

        result = parse_mcp(payload)

        assert result["type"] == "response"
        assert result["status"] == "success"
        assert result["data"] == {"temp": 72}

    def test_error_response(self) -> None:
        payload = json.dumps({
            "mcp_version": "1.0",
            "response": {
                "status": "error",
                "message": "API key invalid",
            },
        }).encode()

        result = parse_mcp(payload)

        assert result["type"] == "response"
        assert result["status"] == "error"
        assert result["message"] == "API key invalid"


class TestMalformedInput:
    """Tests for graceful error handling on bad input."""

    def test_malformed_json(self) -> None:
        result = parse_mcp(b"this is not json{{{")

        assert result["type"] == "error"
        assert "Failed to decode JSON" in result["message"]

    def test_empty_payload(self) -> None:
        result = parse_mcp(b"")

        assert result["type"] == "error"
        assert "Failed to decode JSON" in result["message"]

    def test_non_object_json(self) -> None:
        result = parse_mcp(b'"just a string"')

        assert result["type"] == "error"
        assert "not a JSON object" in result["message"]

    def test_missing_call_and_response(self) -> None:
        payload = json.dumps({"mcp_version": "1.0"}).encode()

        result = parse_mcp(payload)

        assert result["type"] == "error"
        assert "Unrecognised" in result["message"]

    def test_call_field_not_object(self) -> None:
        payload = json.dumps({"mcp_version": "1.0", "call": "bad"}).encode()

        result = parse_mcp(payload)

        assert result["type"] == "error"
        assert "'call' field is not an object" in result["message"]

    def test_response_field_not_object(self) -> None:
        payload = json.dumps({"mcp_version": "1.0", "response": 42}).encode()

        result = parse_mcp(payload)

        assert result["type"] == "error"
        assert "'response' field is not an object" in result["message"]
