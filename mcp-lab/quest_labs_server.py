"""
Quest Labs MCP server  -- a real, usable custom server.
=======================================================
Gives an MCP host (Claude Code / Claude Desktop) first-class access to the
Lab*.py teaching files in this repo, so you can ask questions like:

    "which lab covers autograd?"        -> search_labs("autograd")
    "show me lab 17"                    -> read_lab(17)
    "what labs do I have?"              -> list_labs()

...and the model reads the files on demand instead of you pasting code.

Run:      py quest_labs_server.py
Inspect:  mcp dev quest_labs_server.py
Register: claude mcp add quest-labs -- py "<abs path>/quest_labs_server.py"
"""

import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("quest-labs")

# The repo root is the parent of this mcp-lab/ folder.
REPO_ROOT = Path(__file__).resolve().parent.parent
LAB_GLOB = "Lab*.py"


def _lab_files() -> list[Path]:
    """All Lab*.py files, sorted by lab number then name."""
    def key(p: Path):
        m = re.match(r"Lab(\d+)", p.name)
        return (int(m.group(1)) if m else 999, p.name)

    return sorted(REPO_ROOT.glob(LAB_GLOB), key=key)


def _title_of(path: Path) -> str:
    """Pull a human title from the file's header comment, if present."""
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"[#\s]*Lab\s*\d+\s*:\s*(.+)", line)
        if m:
            return m.group(1).strip()
    return path.stem


def _find_lab(number: int) -> Path | None:
    for p in _lab_files():
        m = re.match(r"Lab0*(\d+)", p.name)
        if m and int(m.group(1)) == number:
            return p
    return None


@mcp.tool()
def list_labs() -> str:
    """List every lab in the repo as 'NN - Title', one per line."""
    lines = []
    for p in _lab_files():
        m = re.match(r"Lab0*(\d+)", p.name)
        num = m.group(1) if m else "?"
        lines.append(f"{num:>2} - {_title_of(p)}  ({p.name})")
    return "\n".join(lines) if lines else "No Lab*.py files found."


@mcp.tool()
def read_lab(number: int) -> str:
    """Return the full source code of a lab by its number (e.g. 17)."""
    p = _find_lab(number)
    if p is None:
        return f"No lab found with number {number}. Try list_labs()."
    return f"# {p.name}\n\n{p.read_text(encoding='utf-8', errors='replace')}"


@mcp.tool()
def search_labs(keyword: str, ignore_case: bool = True) -> str:
    """Find which labs mention a keyword, with the matching lines and line numbers."""
    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(re.escape(keyword), flags)
    hits: list[str] = []
    for p in _lab_files():
        matches = []
        for i, line in enumerate(
            p.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
        ):
            if pattern.search(line):
                matches.append(f"    L{i}: {line.strip()}")
        if matches:
            hits.append(f"{p.name} ({len(matches)} hit(s)):")
            hits.extend(matches[:5])  # cap noise
            if len(matches) > 5:
                hits.append(f"    ... +{len(matches) - 5} more")
    return "\n".join(hits) if hits else f"No labs mention '{keyword}'."


if __name__ == "__main__":
    mcp.run()
