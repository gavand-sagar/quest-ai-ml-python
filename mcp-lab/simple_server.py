"""
Simple MCP demo server.
========================
The smallest server worth running: two tools and one resource.

Run standalone (it will wait on stdio):
    py simple_server.py

Inspect it in a browser UI:
    mcp dev simple_server.py

Register with Claude Code:
    claude mcp add simple-demo -- py "<abs path>/simple_server.py"
"""

from datetime import datetime

from mcp.server.fastmcp import FastMCP

# The name shows up in the client's tool list.
mcp = FastMCP("simple-demo")


# ---- A TOOL: an action the model can call ----
# Type hints -> input schema (auto). Docstring -> description the model reads.
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


# ---- Another tool: strings work the same way ----
@mcp.tool()
def greet(name: str, excited: bool = False) -> str:
    """Greet a person by name. Set excited=True for an exclamation."""
    punct = "!" if excited else "."
    return f"Hello, {name}{punct}"


# ---- A RESOURCE: read-only data addressed by a URI ----
# The client can load this without it being an "action".
@mcp.resource("clock://now")
def current_time() -> str:
    """The current server time as an ISO-8601 string."""
    return datetime.now().isoformat(timespec="seconds")


if __name__ == "__main__":
    # No transport arg => stdio: the host launches this file as a subprocess
    # and exchanges JSON-RPC over stdin/stdout.
    mcp.run()
