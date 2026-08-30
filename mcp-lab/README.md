# Lab 22 — MCP Servers

Two runnable [Model Context Protocol](https://modelcontextprotocol.io) servers:

| File | What it is |
|------|------------|
| `simple_server.py` | Smallest useful demo: `add`, `greet` tools + a `clock://now` resource |
| `quest_labs_server.py` | **Usable custom server** — exposes this repo's `Lab*.py` files as tools (`list_labs`, `read_lab`, `search_labs`) |

Read-along notes: [`../Lab22_MCP_Server_And_Client.py`](../Lab22_MCP_Server_And_Client.py)

## 1. Install

```bash
pip install -r requirements.txt
```

(Windows note: this repo's Python launcher is `py`. Swap `py` for `python`/`python3` on other machines.)

## 2. Poke at it without any AI — the Inspector

The fastest feedback loop. Opens a browser UI where you can list and call tools by hand:

```bash
mcp dev quest_labs_server.py
```

## 3. Use it from Claude Code

```bash
claude mcp add quest-labs -- py "C:/Users/Sagar/Desktop/Everything/quest-ai-ml-python/mcp-lab/quest_labs_server.py"
claude mcp list
```

Then in a session just ask: *"use quest-labs to search the labs for autograd"*.

Remove it later with `claude mcp remove quest-labs`.

## 4. Use it from Claude Desktop

Settings → Developer → **Edit Config**, then add (merge into any existing `mcpServers`):

```json
{
  "mcpServers": {
    "quest-labs": {
      "command": "py",
      "args": ["C:/Users/Sagar/Desktop/Everything/quest-ai-ml-python/mcp-lab/quest_labs_server.py"]
    },
    "simple-demo": {
      "command": "py",
      "args": ["C:/Users/Sagar/Desktop/Everything/quest-ai-ml-python/mcp-lab/simple_server.py"]
    }
  }
}
```

Restart Claude Desktop — the tools appear under the tools/plug icon.

## How it works (one paragraph)

The host launches the script as a subprocess and speaks **JSON-RPC over stdio**.
`FastMCP` turns your Python type hints into each tool's input schema and your
docstrings into the descriptions the model reads to decide when to call a tool.
The model never sees the JSON — it sees clean tool names and calls them; the
client handles the wire format.
