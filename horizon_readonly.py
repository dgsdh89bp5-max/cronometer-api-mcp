"""Deprecated entrypoint retained so the existing Horizon deploy stays live.

The hosted project originally targeted this filename. It now aliases the
complete authenticated server so the deployed URL gains write tools without a
Horizon configuration change. New deployments should use ``horizon.py:mcp``.
"""

from horizon import mcp

__all__ = ["mcp"]
