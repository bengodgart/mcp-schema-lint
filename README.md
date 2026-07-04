# mcp-schema-lint

**Catch agent-hostile MCP tool schemas before you ship them.** Point it at your server's tool definitions and it flags the schema mistakes that make tools unreliable for agents: missing `additionalProperties: false`, vague or missing descriptions, `required` fields that do not exist, and unbounded parameters.

MCP has thousands of servers, and a documented pattern of shipping tools that are technically reachable but hard for an agent to use. Even official servers have shipped invalid schemas. The existing checker, MCP Inspector, is interactive: you click through it by hand. This is a linter: non-interactive, exits non-zero on errors, drops into CI.

## What it catches

```
$ python -m mcpschemalint lint tools.json

MCP schema lint
tools: 3   errors: 4   warnings: 5   info: 2

run
  [ERROR] required-unknown-property: required lists 'timeout' but it is not in properties  (required[timeout])
  [WARN ] additional-properties-not-false: set additionalProperties: false so agents cannot pass invented parameters
  [WARN ] param-missing-description: parameter 'command' has no description  (properties.command)
  [info ] unbounded-string: string 'command' is unbounded; consider an enum or maxLength
<tool #2>
  [ERROR] name-missing: tool has no name  (name)
  [ERROR] input-schema-missing: no inputSchema; agents cannot know the arguments
```

Exit code is `0` when clean, `1` when the gate fails, so a broken schema fails the build instead of confusing an agent in production.

## Quickstart (3 commands)

```bash
git clone https://github.com/bengodgart/mcp-schema-lint
cd mcp-schema-lint
python -m mcpschemalint lint fixtures/bad_server.json
```

Then lint your own: `python -m mcpschemalint lint your_tools.json`. Python 3.9+, standard library only.

## The input

A JSON file of MCP tool definitions. It accepts any of:
- a bare list of tool objects
- an object with a `tools` array (a `tools/list` response)
- a full JSON-RPC response with `result.tools`

Get it by capturing your server's `tools/list` response, or by exporting your registered tools to JSON.

## The rules

| Rule | Severity | Why it matters |
|---|---|---|
| `name-missing` | error | agents select tools by name |
| `description-missing` | error | agents choose a tool from its description |
| `input-schema-missing` | error | without it, an agent cannot know the arguments |
| `required-unknown-property` | error | a `required` field not in `properties` is a broken schema |
| `additional-properties-not-false` | warn | without it, agents can pass invented parameters |
| `param-missing-description` | warn | undescribed params get filled with guesses |
| `description-too-short` / `description-vague` | warn | placeholder descriptions cause wrong tool selection |
| `unbounded-string` / `unbounded-array` | info | an enum or a max keeps agent inputs in range |

Use `--strict` to fail on warnings too. Add `--html report.html` or `--md report.md` for a shareable report.

## In CI

```yaml
- run: pip install . && python -m mcpschemalint lint tools.json --strict
```

A non-zero exit fails the job before an agent-hostile schema reaches your users.

## Tests

```bash
python -m unittest discover -s tests -v   # 11 tests, no dependencies
```

## Why I built it

MCP servers keep shipping tool schemas that agents struggle with, and the common failures are boring and mechanical: a missing `additionalProperties: false`, a vague description, a `required` field that does not exist. Mechanical problems want a linter, not a human clicking through an inspector. So I wrote the linter.

## License

MIT. See [LICENSE](LICENSE).
