"""MCP Tool server entrypoint for agents.

This wrapper keeps the public tool path under tools/ while reusing the
implementation in mcp/wiki_mcp_server.py.
"""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "mcp" / "wiki_mcp_server.py"), run_name="__main__")
