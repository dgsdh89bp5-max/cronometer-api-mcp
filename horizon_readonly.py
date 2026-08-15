"""Read-only Cronometer MCP surface for Horizon and Claude mobile.

Authentication belongs at Horizon's gateway. This entrypoint deliberately
omits every tool that can modify Cronometer so an authorization or client-side
approval mistake cannot turn a read request into a diary mutation.
"""

import sys
from pathlib import Path

# Horizon launches the entrypoint through the installed FastMCP CLI. With a
# ``src`` layout, that process must not depend on an editable-install .pth file
# being processed by the Python 3.14 runtime.
_SRC = str(Path(__file__).resolve().parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# Horizon is built and operated by the FastMCP team. Use the current native
# FastMCP server here rather than the legacy implementation vendored in the
# low-level ``mcp`` SDK. The latter is fine for the repository's original
# stdio entrypoint, but it does not expose the same HTTP/runtime metadata that
# Horizon and remote clients use during tool discovery.
from fastmcp import FastMCP

from cronometer_api_mcp.server import (
    get_biometrics,
    get_daily_nutrition,
    get_fasting_history,
    get_fasting_stats,
    get_food_details,
    get_food_log,
    get_macro_targets,
    get_nutrition_scores,
    list_biometrics,
    search_foods,
)

mcp = FastMCP(
    "cronometer-read-only",
    instructions=(
        "Read-only access to Cronometer nutrition, food search, targets, "
        "fasting history, and biometrics. This server cannot add, copy, "
        "complete, create, or remove diary data."
    ),
)

_READ_ONLY_ANNOTATIONS = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True,
}

for _tool in (
    get_food_log,
    get_daily_nutrition,
    get_nutrition_scores,
    search_foods,
    get_food_details,
    get_macro_targets,
    get_fasting_history,
    get_fasting_stats,
    list_biometrics,
    get_biometrics,
):
    # These functions return JSON text, not structuredContent. Disabling the
    # generated output schema keeps remote tool discovery honest and avoids
    # advertising a wrapper object that the implementations do not return.
    mcp.tool(
        annotations=_READ_ONLY_ANNOTATIONS,
        output_schema=None,
    )(_tool)

__all__ = ["mcp"]
