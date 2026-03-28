"""Pretty-prints parsed MCP data to the console using Rich."""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table


class MCPPrinter:
    """Renders parsed MCP requests and responses as colorized console output."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def print_request(self, parsed_data: dict[str, Any]) -> None:
        """Display a parsed MCP request inside a Rich panel.

        Args:
            parsed_data: Dictionary produced by :func:`parser.parse_mcp` with
                ``type == "request"``.
        """
        if parsed_data.get("type") == "error":
            self._print_parse_error(parsed_data)
            return

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Key", style="bold cyan")
        table.add_column("Value")
        table.add_row("Tool", parsed_data.get("tool_name", "unknown"))
        table.add_row("Function", parsed_data.get("function", "unknown"))

        args_json = json.dumps(parsed_data.get("args", {}), indent=2)
        args_syntax = Syntax(args_json, "json", theme="monokai", word_wrap=True)

        panel = Panel.fit(
            table,
            title="[bold yellow]➡️  MCP Request[/bold yellow]",
            border_style="yellow",
        )
        self.console.print(panel)
        self.console.print(
            Panel.fit(args_syntax, title="Arguments", border_style="yellow")
        )

    def print_response(self, parsed_data: dict[str, Any]) -> None:
        """Display a parsed MCP response inside a Rich panel.

        Args:
            parsed_data: Dictionary produced by :func:`parser.parse_mcp` with
                ``type == "response"``.
        """
        if parsed_data.get("type") == "error":
            self._print_parse_error(parsed_data)
            return

        status = parsed_data.get("status", "unknown")
        is_success = status == "success"
        border = "green" if is_success else "red"
        title_colour = "green" if is_success else "red"

        if is_success:
            body = json.dumps(parsed_data.get("data", {}), indent=2)
        else:
            body = parsed_data.get("message", "No details")

        syntax = Syntax(body, "json" if is_success else "text", theme="monokai", word_wrap=True)

        panel = Panel.fit(
            syntax,
            title=f"[bold {title_colour}]⬅️  MCP Response ({status})[/bold {title_colour}]",
            border_style=border,
        )
        self.console.print(panel)

    def _print_parse_error(self, parsed_data: dict[str, Any]) -> None:
        """Display a parse-level error."""
        msg = parsed_data.get("message", "Unknown parse error")
        panel = Panel.fit(
            f"[bold red]{msg}[/bold red]",
            title="[bold red]⚠️  Parse Error[/bold red]",
            border_style="red",
        )
        self.console.print(panel)
