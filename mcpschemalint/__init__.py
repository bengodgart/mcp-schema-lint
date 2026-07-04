"""mcp-schema-lint: lint MCP tool definitions for agent-unfriendly schemas.

Flags the schema anti-patterns that make MCP tools unreliable for agents:
missing `additionalProperties: false`, vague or missing descriptions, unbounded
params, and broken `required` lists. Non-interactive and CI-friendly (non-zero
exit on errors). Stdlib-only, offline. See README.md.
"""

__version__ = "0.1.0"
