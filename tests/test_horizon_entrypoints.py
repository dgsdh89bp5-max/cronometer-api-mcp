"""Horizon entrypoint compatibility and remote-schema tests."""

from __future__ import annotations

import asyncio

from test_server_import import EXPECTED_TOOLS

WRITE_TOOLS = {
    "add_custom_food",
    "add_food_entry",
    "copy_day",
    "mark_day_complete",
    "remove_food_entry",
}


def test_full_horizon_entrypoint_exposes_existing_surface():
    from fastmcp import FastMCP

    from main import mcp

    tools = asyncio.run(mcp.list_tools())

    assert isinstance(mcp, FastMCP)
    assert {tool.name for tool in tools} == EXPECTED_TOOLS
    assert all(tool.output_schema is None for tool in tools)

    annotations = {tool.name: tool.annotations for tool in tools}
    assert all(annotations[name].readOnlyHint is False for name in WRITE_TOOLS)
    assert annotations["remove_food_entry"].destructiveHint is True
    assert all(
        annotations[name].readOnlyHint is True for name in EXPECTED_TOOLS - WRITE_TOOLS
    )


def test_deployed_entrypoint_aliases_complete_surface():
    from horizon import mcp as full_mcp
    from horizon_readonly import mcp as deployed_mcp

    assert deployed_mcp is full_mcp
