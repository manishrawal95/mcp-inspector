"""Unit tests for the MCP printer."""

from __future__ import annotations

from io import StringIO

from rich.console import Console

from mcp_inspector.printer import MCPPrinter


def _make_printer() -> tuple[MCPPrinter, StringIO]:
    buf = StringIO()
    console = Console(file=buf, force_terminal=True, width=120)
    return MCPPrinter(console=console), buf


class TestPrintRequest:
    def test_prints_request_fields(self) -> None:
        printer, buf = _make_printer()
        printer.print_request({
            "type": "request",
            "mcp_version": "1.0",
            "tool_name": "weather",
            "function": "get_current_temp",
            "args": {"location": "SF"},
        })
        output = buf.getvalue()
        assert "weather" in output
        assert "get_current_temp" in output
        assert "SF" in output

    def test_prints_error_on_parse_failure(self) -> None:
        printer, buf = _make_printer()
        printer.print_request({"type": "error", "message": "bad json"})
        output = buf.getvalue()
        assert "bad json" in output


class TestPrintResponse:
    def test_prints_success_response(self) -> None:
        printer, buf = _make_printer()
        printer.print_response({
            "type": "response",
            "status": "success",
            "data": {"temp": 72},
        })
        output = buf.getvalue()
        assert "success" in output
        assert "72" in output

    def test_prints_error_response(self) -> None:
        printer, buf = _make_printer()
        printer.print_response({
            "type": "response",
            "status": "error",
            "message": "API key invalid",
        })
        output = buf.getvalue()
        assert "error" in output
        assert "API key invalid" in output
