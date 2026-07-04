# PRD — mcp-schema-lint (mcpschemalint)

**One-liner (from brief 04):** A free, non-interactive linter that scans an MCP server's tool definitions and flags the schema anti-patterns that make tools unreliable for agents, so a server builder can catch them in CI before shipping.

**Usefulness (from brief 04):** Malformed tool schemas are a documented, recurring MCP failure (official servers have shipped invalid schemas; scans of many servers found high-severity issues). MCP Inspector is interactive; there is no CI-friendly schema linter. A builder runs this against their tool list and gets a fix list in seconds, at $0.

## v1 scope (capped)

1. Ingest MCP tool definitions from a static JSON (bare list, `tools` array, or `result.tools`).
2. A rule set of agent-unfriendliness checks: missing `additionalProperties: false`, empty/vague descriptions, unbounded string/array params, `required` referencing unknown properties, missing name / inputSchema.
3. Per-tool report (error/warn/info) with the exact offending field and a one-line fix, plus a non-zero exit so it gates CI.
4. README opening with a real before/after finding. Text always; `--html` and `--md` optional; `--strict` fails on warnings.

## Non-goals (NOT v1 - expansion paths, parked)

- A hosted scanner service, accounts.
- Runtime security scanning / pentesting (a separate, heavier project).
- Auto-fixing schemas.
- Live connection to a running server (v1 is static JSON; connect-once is a v2 expansion).

## Demo path (stranger sees value in under 2 minutes)

Clone -> `python -m mcpschemalint lint fixtures/bad_server.json` -> see 4 errors, 5 warnings, 2 infos with exact fields and fixes, exit 1. Run against `fixtures/good_server.json` -> clean, exit 0. Then lint their own tools JSON.

## Done when

- Lints a real tools JSON and prints the report in under 2 minutes on a fresh clone.
- One flagged issue is confirmed against the MCP spec (paste the spec note).
- README opens with a real finding; no em-dashes in user-facing copy.
- Public repo, MIT-licensed, offline; smoke tests pass.
