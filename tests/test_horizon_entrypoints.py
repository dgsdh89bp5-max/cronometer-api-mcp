"""Horizon entrypoint compatibility and safety-boundary tests."""

from __future__ import annotations

import asyncio

from test_server_import import EXPECTED_TOOLS

READ_ONLY_TOOLS = {
    "get_biometrics",
    "get_daily_nutrition",
    "get_fasting_history",
    "get_fasting_stats",
    "get_food_details",
    "get_food_log",
    "get_macro_targets",
    "get_nutrition_scores",
    "list_biometrics",
    "search_foods",
}


def test_full_horizon_entrypoint_exposes_existing_surface():
    from main import mcp

    tools = asyncio.run(mcp.list_tools())

    assert {tool.name for tool in tools} == EXPECTED_TOOLS


def test_read_only_horizon_entrypoint_omits_all_write_tools():
    from horizon_readonly import mcp

    tools = asyncio.run(mcp.list_tools())

    assert {tool.name for tool in tools} == READ_ONLY_TOOLS
    assert READ_ONLY_TOOLS < EXPECTED_TOOLS
    assert all(tool.annotations.readOnlyHint is True for tool in tools)
