# ============================================
# Lab 22: MCP Server (and using it)
# ============================================
# Agenda (~50 min):
#   1. What MCP is and why it matters            (~8 min)
#   2. The three things a server can expose      (~7 min)
#   3. A SIMPLE demo server (build + run)        (~10 min)
#   4. A USABLE server: "Quest Labs" tools       (~12 min)
#   5. Wiring it into a client (Claude Code/CLI) (~8 min)
#   6. How the plumbing actually works           (~5 min)
#
# Install first if needed:  pip install "mcp[cli]"
# (This lab is a guided read-along. The runnable servers live in ./mcp-lab/)

# ============================================
# 1. WHAT IS MCP?
# ============================================
# MCP = "Model Context Protocol". An open standard (from Anthropic) that lets an
# AI app (the "host", e.g. Claude Desktop or Claude Code) talk to external tools
# and data through a uniform interface.
#
# The mental model:
#   HOST  (Claude Code / Claude Desktop)  <-- the AI app the human uses
#     |
#   CLIENT  (one connection per server)   <-- lives inside the host
#     |
#   SERVER  (your code, this lab)         <-- exposes tools/data
#
# Before MCP, every integration was custom glue code. MCP is the "USB-C port"
# for AI: write a server once, and ANY MCP-aware host can plug into it.


# ============================================
# 2. WHAT A SERVER CAN EXPOSE
# ============================================
# A server offers three kinds of capabilities:
#
#   TOOLS      -> functions the model can CALL (add numbers, query a DB, send
#                 an email). These are actions. Analogous to POST endpoints.
#   RESOURCES  -> read-only DATA the model can LOAD (a file, a row, a config).
#                 Analogous to GET endpoints. Identified by a URI.
#   PROMPTS    -> reusable prompt templates the user can pick ("summarize this").
#
# For 90% of real work you write TOOLS. That's what both demos below focus on.


# ============================================
# 3. THE SIMPLE DEMO SERVER
# ============================================
# See ./mcp-lab/simple_server.py  -- the smallest useful server.
#
# The whole thing, conceptually:
#
#   from mcp.server.fastmcp import FastMCP
#   mcp = FastMCP("simple-demo")
#
#   @mcp.tool()
#   def add(a: int, b: int) -> int:
#       """Add two numbers."""      # <- the docstring becomes the tool description
#       return a + b
#
#   if __name__ == "__main__":
#       mcp.run()                   # speaks MCP over stdin/stdout ("stdio")
#
# Key ideas:
#   * FastMCP reads your type hints to build the tool's input SCHEMA automatically.
#   * The docstring is what the model reads to decide WHEN to use the tool.
#   * mcp.run() with no args uses the "stdio" transport: the host launches your
#     script as a subprocess and talks JSON-RPC over its stdin/stdout.


# ============================================
# 4. THE USABLE SERVER  (a real use case)
# ============================================
# See ./mcp-lab/quest_labs_server.py
#
# The use case: give the AI first-class access to THIS repo's lab files, so you
# can ask "which lab covers autograd?" or "show me lab 17" and it can actually
# read them on demand instead of you pasting code.
#
# It exposes three tools over the Lab*.py files sitting next to it:
#   list_labs()             -> every lab number + title
#   read_lab(number)        -> full source of one lab
#   search_labs(keyword)    -> which labs mention a term, with line hits
#
# Why this is a good "custom MCP server" example:
#   * It wraps data the model can't otherwise see (your local files).
#   * The tools are small, named clearly, and return plain text.
#   * It's genuinely useful day-to-day, not a toy.


# ============================================
# 5. USING IT FROM A CLIENT
# ============================================
# Option A -- Claude Code CLI (fastest to try):
#
#   claude mcp add quest-labs -- py "C:/.../mcp-lab/quest_labs_server.py"
#   claude mcp list                      # confirm it's registered
#   # then in a session:  "use quest-labs to list the labs"
#
# Option B -- Claude Desktop:
#   Edit claude_desktop_config.json (Settings > Developer > Edit Config) and add:
#
#   {
#     "mcpServers": {
#       "quest-labs": {
#         "command": "py",
#         "args": ["C:/Users/Sagar/Desktop/Everything/quest-ai-ml-python/mcp-lab/quest_labs_server.py"]
#       }
#     }
#   }
#   Restart Claude Desktop; the tools appear under the plug/tools icon.
#
# Option C -- inspect without any AI (great for debugging):
#   mcp dev mcp-lab/quest_labs_server.py     # opens the MCP Inspector in a browser


# ============================================
# 6. HOW THE PLUMBING WORKS
# ============================================
# Under the hood MCP is JSON-RPC 2.0 messages. A session looks like:
#
#   1. initialize            host <-> server handshake (capabilities, versions)
#   2. tools/list            host asks "what tools do you have?"
#   3. tools/call            host calls add(a=2, b=3); server returns 5
#
# Transports (how bytes move):
#   * stdio  -> local subprocess over stdin/stdout   (what these labs use)
#   * HTTP   -> a remote server you connect to by URL (for shared/hosted servers)
#
# The model never sees this JSON. It sees clean tool names + descriptions, decides
# to call one, and the client handles the wire format. That separation is the
# whole point: your server code stays plain Python.


# ============================================
# TRY IT
# ============================================
#   cd mcp-lab
#   pip install -r requirements.txt
#   py quest_labs_server.py        # runs; waits on stdio (Ctrl+C to quit)
#   # or, better, register it with a client per section 5 and just ask.
#
# Read ./mcp-lab/README.md for copy-paste setup commands.
print("Lab 22 is a read-along. The runnable servers are in ./mcp-lab/ -- see README.md")
