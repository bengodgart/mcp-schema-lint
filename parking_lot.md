# Parking lot — mcp-schema-lint

Ideas that surfaced during the v1 build. NOT in v1 scope.

- **Live connect-once mode** - connect to a running MCP server, pull its tools/list, and lint that, instead of a static JSON file. v2.
- **Security-rule slice** - the "43% of servers had critical vulnerabilities" angle as a separate, clearly-scoped mode (prompt-injection surfaces, over-broad params). Keep it distinct from schema quality.
- **Publish as an MCP server itself** - a linter-as-server so it appears in the registries it audits.
- **Auto-fix suggestions** - emit a patched schema (suggest-only, never write in place).
- **Recurring "MCP schema health" report** - run over a set of public servers and publish findings as content (the launch writeup).

Product-creep tripwire (doctrine T11): a hosted scanner with accounts is an app. Stop and park.
