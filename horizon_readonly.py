"""Read-only Cronometer MCP surface for Horizon and Claude mobile.

Authentication belongs at Horizon's gateway. This entrypoint deliberately
omits every tool that can modify Cronometer so an authorization or client-side
approval mistake cannot turn a read request into a diary mutation.
"""

from mcp.server.fastmcp import FastMCP

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
    mcp.tool(annotations=_READ_ONLY_ANNOTATIONS)(_tool)

__all__ = ["mcp"]
