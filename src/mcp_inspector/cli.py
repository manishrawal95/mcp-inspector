"""Command-line interface entry point for mcp-inspector."""

from __future__ import annotations

import asyncio
import sys

import typer
from rich.console import Console

app = typer.Typer(
    name="mcp-inspector",
    help="A local proxy for inspecting agent-tool MCP traffic.",
    add_completion=False,
)

console = Console()


@app.command()
def main(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Address to listen on."),
    port: int = typer.Option(8080, "--port", "-p", help="Port to listen on."),
) -> None:
    """Start the MCP Inspector proxy.

    Launches a local HTTP proxy that intercepts, parses, and pretty-prints
    Model Context Protocol (MCP) traffic.
    """
    from mitmproxy.options import Options
    from mitmproxy.tools.dump import DumpMaster

    from mcp_inspector.proxy import MCPInterceptor

    console.print(
        f"[bold green]MCP Inspector[/bold green] listening on "
        f"[bold]http://{host}:{port}[/bold]"
    )

    async def run_proxy() -> None:
        opts = Options(listen_host=host, listen_port=port)
        master = DumpMaster(opts)
        master.addons.add(MCPInterceptor())
        try:
            await master.run()
        except KeyboardInterrupt:
            master.shutdown()

    try:
        asyncio.run(run_proxy())
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down…[/yellow]")
        sys.exit(0)
