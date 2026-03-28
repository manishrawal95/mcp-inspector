"""Core proxy logic built as a mitmproxy addon to intercept MCP traffic."""

from __future__ import annotations

from mitmproxy import http

from mcp_inspector.parser import parse_mcp
from mcp_inspector.printer import MCPPrinter


class MCPInterceptor:
    """A mitmproxy addon that intercepts HTTP flows and pretty-prints MCP messages."""

    def __init__(self) -> None:
        self.printer = MCPPrinter()

    def request(self, flow: http.HTTPFlow) -> None:
        """Intercept and display an MCP request.

        Args:
            flow: The mitmproxy HTTP flow whose request content will be parsed.
        """
        content = flow.request.content
        if content:
            parsed = parse_mcp(content)
            self.printer.print_request(parsed)

    def response(self, flow: http.HTTPFlow) -> None:
        """Intercept and display an MCP response.

        Args:
            flow: The mitmproxy HTTP flow whose response content will be parsed.
        """
        if flow.response and flow.response.content:
            parsed = parse_mcp(flow.response.content)
            self.printer.print_response(parsed)
