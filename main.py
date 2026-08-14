"""Horizon-compatible entrypoint for the complete Cronometer MCP server.

Use ``main.py:mcp`` when every tool, including diary write tools, is intended
to be available. For the safer Claude mobile deployment, use
``horizon_readonly.py:mcp`` instead.
"""

from cronometer_api_mcp.server import mcp

__all__ = ["mcp"]
