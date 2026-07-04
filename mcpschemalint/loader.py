"""Load MCP tool definitions from a JSON file.

Accepts any of the shapes a server or an export produces:
- a bare list of tool objects
- an object with a top-level "tools" list (the shape of a tools/list response)
- an object with a "result": {"tools": [...]} (a full JSON-RPC response)

A tool object is expected to look like:
    {"name": "...", "description": "...", "inputSchema": {...}}
inputSchema uses "inputSchema" (MCP) but we also accept "input_schema".
"""

from __future__ import annotations

import json
from typing import Any


def _extract_tools(data: Any) -> list[dict]:
    if isinstance(data, list):
        return [t for t in data if isinstance(t, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("tools"), list):
            return [t for t in data["tools"] if isinstance(t, dict)]
        result = data.get("result")
        if isinstance(result, dict) and isinstance(result.get("tools"), list):
            return [t for t in result["tools"] if isinstance(t, dict)]
    raise ValueError(
        "could not find a tools list (expected a list, or an object with a "
        "'tools' or 'result.tools' array)"
    )


def load_tools(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    tools = _extract_tools(data)
    if not tools:
        raise ValueError("no tools found in the file")
    return tools


def get_input_schema(tool: dict) -> dict | None:
    schema = tool.get("inputSchema")
    if schema is None:
        schema = tool.get("input_schema")
    return schema if isinstance(schema, dict) else None
