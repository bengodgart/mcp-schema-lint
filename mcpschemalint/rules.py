"""The lint rules. Each produces zero or more Findings for one tool.

Severities:
- error : the schema is broken or will actively mislead an agent.
- warn  : an agent-unfriendly pattern that causes unreliable tool use.
- info  : a soft suggestion; safe to ignore, nice to fix.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .loader import get_input_schema

ERROR = "error"
WARN = "warn"
INFO = "info"

MIN_DESC_CHARS = 12
VAGUE_PATTERNS = re.compile(
    r"^(this tool|a tool|does stuff|todo|tbd|test|the tool|tool that)\b", re.IGNORECASE
)


@dataclass
class Finding:
    tool: str
    rule: str
    severity: str
    field: str
    message: str


def _tool_name(tool: dict, index: int) -> str:
    name = tool.get("name")
    return str(name) if isinstance(name, str) and name else f"<tool #{index}>"


def check_tool(tool: dict, index: int) -> list[Finding]:
    name = _tool_name(tool, index)
    findings: list[Finding] = []

    # name present and reasonable
    if not tool.get("name"):
        findings.append(Finding(name, "name-missing", ERROR, "name", "tool has no name"))

    # description present, long enough, not vague
    desc = tool.get("description")
    if not desc or not isinstance(desc, str) or not desc.strip():
        findings.append(Finding(name, "description-missing", ERROR, "description",
                                "tool has no description; agents rely on it to choose the tool"))
    else:
        d = desc.strip()
        if len(d) < MIN_DESC_CHARS:
            findings.append(Finding(name, "description-too-short", WARN, "description",
                                    f"description is only {len(d)} chars; agents need more to pick the right tool"))
        elif VAGUE_PATTERNS.match(d):
            findings.append(Finding(name, "description-vague", WARN, "description",
                                    "description looks like a placeholder or generic filler"))

    # input schema present and an object
    schema = get_input_schema(tool)
    if schema is None:
        findings.append(Finding(name, "input-schema-missing", ERROR, "inputSchema",
                                "no inputSchema; agents cannot know the arguments"))
        return findings

    if schema.get("type") not in (None, "object"):
        findings.append(Finding(name, "input-schema-not-object", WARN, "inputSchema.type",
                                f"inputSchema type is '{schema.get('type')}', expected 'object'"))

    properties = schema.get("properties")
    properties = properties if isinstance(properties, dict) else {}
    required = schema.get("required")
    required = required if isinstance(required, list) else []

    # additionalProperties should be explicitly false so agents don't invent params
    if schema.get("additionalProperties") is not False:
        findings.append(Finding(name, "additional-properties-not-false", WARN, "inputSchema.additionalProperties",
                                "set additionalProperties: false so agents cannot pass invented parameters"))

    # required must reference real properties
    for req in required:
        if req not in properties:
            findings.append(Finding(name, "required-unknown-property", ERROR, f"required[{req}]",
                                    f"required lists '{req}' but it is not in properties"))

    # per-parameter checks
    for pname, pschema in properties.items():
        if not isinstance(pschema, dict):
            continue
        if not pschema.get("description"):
            findings.append(Finding(name, "param-missing-description", WARN, f"properties.{pname}",
                                    f"parameter '{pname}' has no description"))
        ptype = pschema.get("type")
        if ptype == "string" and "enum" not in pschema and "maxLength" not in pschema:
            findings.append(Finding(name, "unbounded-string", INFO, f"properties.{pname}",
                                    f"string '{pname}' is unbounded; consider an enum or maxLength"))
        if ptype == "array" and "maxItems" not in pschema:
            findings.append(Finding(name, "unbounded-array", INFO, f"properties.{pname}",
                                    f"array '{pname}' has no maxItems; consider bounding it"))

    return findings
