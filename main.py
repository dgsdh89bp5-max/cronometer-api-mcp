"""Horizon-compatible entrypoint for the complete Cronometer MCP server.

Use ``main.py:mcp`` when every tool, including diary write tools, is intended
to be available. For the safer Claude mobile deployment, use
``horizon_readonly.py:mcp`` instead.
"""

import sys
from pathlib import Path

# FastMCP/Horizon imports this file from an installed CLI entrypoint. Make the
# repository's ``src`` package importable without relying on editable-install
# path files, which are not reliable under the Python 3.14 deployment runtime.
_SRC = str(Path(__file__).resolve().parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from cronometer_api_mcp.server import mcp

__all__ = ["mcp"]
