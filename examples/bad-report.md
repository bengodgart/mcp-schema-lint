# MCP schema lint

**Tools:** 3 &nbsp; **Errors:** 3 &nbsp; **Warnings:** 5 &nbsp; **Info:** 2

| Severity | Tool | Rule | Field | Message |
|---|---|---|---|---|
| error | `run` | required-unknown-property | `required[timeout]` | required lists 'timeout' but it is not in properties |
| error | `<tool #2>` | name-missing | `name` | tool has no name |
| error | `<tool #2>` | input-schema-missing | `inputSchema` | no inputSchema; agents cannot know the arguments |
| warn | `run` | description-vague | `description` | description looks like a placeholder or generic filler |
| warn | `run` | additional-properties-not-false | `inputSchema.additionalProperties` | set additionalProperties: false so agents cannot pass invented parameters |
| warn | `run` | param-missing-description | `properties.command` | parameter 'command' has no description |
| warn | `run` | param-missing-description | `properties.tags` | parameter 'tags' has no description |
| warn | `<tool #2>` | description-vague | `description` | description looks like a placeholder or generic filler |
| info | `run` | unbounded-string | `properties.command` | string 'command' is unbounded; consider an enum or maxLength |
| info | `run` | unbounded-array | `properties.tags` | array 'tags' has no maxItems; consider bounding it |