# Docs map

The official docs live at `https://code.claude.com/docs/en/<page>`; add `.md` for the raw page, which `curl` can save and `grep`. Pages are
long (100k+ characters): fetch with a question, and read on with an offset when
the answer says it was cut.

| Question | Page |
|---|---|
| Agent file fields, tool filters, `--agent`, forks, nesting, scopes | `sub-agents` |
| Skill and command frontmatter, `$ARGUMENTS`, `` !`cmd` ``, `context: fork` | `skills` |
| Plugin layout, marketplaces, what plugin parts can do | `plugins`, `plugins/overview`, `plugins/components` |
| MCP config, scopes, OAuth, `--strict-mcp-config` | `mcp` |
| `claude -p`, output formats, the Agent SDK | `headless` |
| Every flag | `cli-reference` |
| Every environment variable (spawn depth, built-in agents, description length) | `env-vars` |
| Settings files, `permissions.deny`, `agent` setting | `settings`, `permissions` |
| Hook events, handler types and their input | `hooks` |
| How plugins load, are cached and versioned; marketplace and plugin sources | `plugins/loading`, `plugins/marketplace-reference` |
| Mods: events, `$` API, limits | `plugins/mods/overview`, `plugins/mods/reference` |
| Built-in tools and what each does | `tools-reference` |
| Prompt cache, TTL | `prompt-caching` |
| An error message | `errors` |

When a page doesn't answer, test it ([headless.md](headless.md)), then add the
answer to this skill.
