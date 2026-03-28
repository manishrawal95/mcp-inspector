# mcp-inspector: A local proxy for inspecting agent-tool MCP traffic.

[![Build Status](https://img.shields.io/github/actions/workflow/status/mrawal/mcp-inspector/ci.yml?branch=main&style=for-the-badge)](https://github.com/mrawal/mcp-inspector/actions)
[![PyPI version](https://img.shields.io/pypi/pyversions/mcp-inspector?style=for-the-badge)](https://pypi.org/project/mcp-inspector/)
[![License](https://img.shields.io/pypi/l/mcp-inspector?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/mrawal/mcp-inspector?style=for-the-badge)](https://github.com/mrawal/mcp-inspector)

`mcp-inspector` is a CLI tool that acts as a local proxy to intercept, parse, and pretty-print Model Context Protocol (MCP) traffic. It provides human-readable, colorized logs of tool calls, arguments, and responses in your terminal. This drastically simplifies debugging for any developer building with the new AI agent and tool-use stack.

### See Your Agent's Tool Calls in Real-Time

Imagine your terminal lighting up with a crystal-clear, structured view of every tool call your AI agent makes. `mcp-inspector` turns a black box of HTTP requests into an organized, color-coded log, showing you exactly what function was called, the arguments passed, and the data returned -- all in real-time. No more `print()` statements or digging through raw server logs.

<!-- Add demo GIF here -->
![MCP Inspector Demo GIF](https://raw.githubusercontent.com/mrawal/mcp-inspector/main/docs/demo.gif)

### Quick Start

Get up and running in under 30 seconds.

1.  **Install the tool:**
    ```bash
    pip install mcp-inspector
    ```

2.  **Run the proxy:**
    ```bash
    mcp-inspector
    # 🕵️ MCP Inspector listening on http://127.0.0.1:8080
    ```

3.  **Point your agent's tool server endpoint to the proxy** (e.g., update your environment variable from `https://api.weather.com` to `http://127.0.0.1:8080`). Watch the structured logs roll into your terminal.

### Features

*   **Zero-Config Proxy:** Runs a local proxy that automatically intercepts HTTP traffic.
*   **Automatic MCP Parsing:** Detects and validates MCP requests and responses on the fly.
*   **Rich, Colorized Output:** Uses `rich` to render tool calls, arguments, and responses in beautiful, easy-to-read panels.
*   **Structured Data Tables:** Displays function arguments in clean tables for quick scanning.
*   **Pretty-Printed JSON:** Colorizes and formats JSON in responses for maximum readability.

### Examples

#### Inspecting a Tool Call Request

When your agent calls a tool, `mcp-inspector` prints a clear summary of the request.

```bash
# Terminal output from mcp-inspector

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ REQUEST ━━┓
┃                                                                          ┃
┃ ➡️ Tool Call                                                             ┃
┃ ┌─────────────┬────────────────────────────────────────────────────────┐ ┃
┃ │ Field       │ Value                                                  │ ┃
┃ ├─────────────┼────────────────────────────────────────────────────────┤ ┃
┃ │ Tool Name   │ weather                                                │ ┃
┃ │ Function    │ get_current_temp                                       │ ┃
┃ │ MCP Version │ 1.0                                                    │ ┃
┃ └─────────────┴────────────────────────────────────────────────────────┘ ┃
┃                                                                          ┃
┃ ➡️ Arguments                                                             ┃
┃ ┌──────────┬───────────────────────────────────────────────────────────┐ ┃
┃ │ Name     │ Value                                                     │ ┃
┃ ├──────────┼───────────────────────────────────────────────────────────┤ ┃
┃ │ location │ "San Francisco, CA"                                       │ ┃
┃ └──────────┴───────────────────────────────────────────────────────────┘ ┃
┃                                                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

#### Inspecting a Tool Call Response

The corresponding response from the tool server is captured and formatted, showing you exactly what data the agent received.

```bash
# Terminal output from mcp-inspector

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RESPONSE ━━┓
┃                                                                          ┃
┃ ➡️ Result: ✅ SUCCESS                                                     ┃
┃                                                                          ┃
┃ ➡️ Data                                                                   ┃
┃ {                                                                        ┃
┃   "temperature": 72,                                                     ┃
┃   "units": "fahrenheit",                                                 ┃
┃   "forecast": "partly_cloudy"                                            ┃
┃ }                                                                        ┃
┃                                                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### How It Works

`mcp-inspector` is built as an addon for the powerful `mitmproxy` library.

1.  The `mcp-inspector` command starts a `mitmproxy` instance with a custom addon script (`proxy.py`).
2.  The `MCPInterceptor` addon intercepts every HTTP request and response flow.
3.  For each flow, the raw byte payload is passed to a parser (`parser.py`) which decodes it and validates the MCP structure.
4.  If valid MCP is found, the parsed dictionary is handed to a printer (`printer.py`).
5.  The printer uses the `rich` library to render the structured data into colorized tables and panels in your terminal.
6.  The entire application is wrapped in a simple CLI (`cli.py`) using `typer`.

### Contributing

Contributions are welcome! This project is young, and we appreciate any help. Please feel free to open an issue to discuss a feature or submit a pull request.

1.  Fork the repository.
2.  Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
3.  Install development dependencies: `pip install -e '.[dev]'`
4.  Make your changes and add tests.
5.  Run tests: `pytest`
6.  Submit a pull request.

### License

This project is licensed under the MIT License.

---

If this saves you time, consider giving it a ⭐

Crafted by [Manish Rawal](https://github.com/mrawal).