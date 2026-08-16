"""Horizon-compatible Cronometer MCP with the complete tool surface.

Horizon provides the remote transport and OAuth boundary. This wrapper uses
the current native FastMCP runtime for reliable remote tool discovery while
re-registering all tools from the repository's original stdio server,
including diary writes.
"""

import sys
from pathlib import Path

_SRC = str(Path(__file__).resolve().parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from fastmcp import FastMCP

from cronometer_api_mcp.server import (
    add_custom_food,
    add_food_entry,
    copy_day,
    get_biometrics,
    get_daily_nutrition,
    get_fasting_history,
    get_fasting_stats,
    get_food_details,
    get_food_log,
    get_macro_targets,
    get_nutrition_scores,
    list_biometrics,
    mark_day_complete,
    remove_food_entry,
    search_foods,
)

mcp = FastMCP(
    "cronometer",
    instructions=(
        "Cronometer nutrition tracking with food search, diary management, "
        "daily nutrition data, macro targets, biometrics, and fasting history. "
        "Use search_foods and get_food_details before add_food_entry. Treat "
        "remove_food_entry as destructive and confirm the intended entry IDs."
    ),
)

_READ_ONLY = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True,
}
_WRITE = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": False,
    "openWorldHint": True,
}
_IDEMPOTENT_WRITE = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True,
}
_DESTRUCTIVE_WRITE = {
    "readOnlyHint": False,
    "destructiveHint": True,
    "idempotentHint": True,
    "openWorldHint": True,
}

_TOOLS = (
    (get_food_log, _READ_ONLY),
    (add_food_entry, _WRITE),
    (remove_food_entry, _DESTRUCTIVE_WRITE),
    (mark_day_complete, _IDEMPOTENT_WRITE),
    (copy_day, _WRITE),
    (get_daily_nutrition, _READ_ONLY),
    (get_nutrition_scores, _READ_ONLY),
    (search_foods, _READ_ONLY),
    (get_food_details, _READ_ONLY),
    (add_custom_food, _WRITE),
    (get_macro_targets, _READ_ONLY),
    (get_fasting_history, _READ_ONLY),
    (get_fasting_stats, _READ_ONLY),
    (list_biometrics, _READ_ONLY),
    (get_biometrics, _READ_ONLY),
)

for _tool, _annotations in _TOOLS:
    # The implementations return JSON text. Avoid advertising a generated
    # structured-output wrapper that the functions do not actually return.
    mcp.tool(annotations=_annotations, output_schema=None)(_tool)

__all__ = ["mcp"]
