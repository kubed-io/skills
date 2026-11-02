---
name: kubed-claude
description: "Use when building on Claude Code itself: writing a subagent or agent file, deciding which tools, MCP servers or other agents an agent gets, running `claude -p` or `--agent` headless, packaging skills, commands or agents in a plugin, serving skills or prompts from an MCP server, or when Claude Code does something its docs didn't prepare you for. Also use before telling anyone what a subagent can see or do."
---

# Claude Code

Field notes: behaviour checked by running Claude Code, not by reading about it.
The official docs are good and change fast. This skill holds what they leave out,
what surprised us, and how to find out the next thing quickly.

Each fact says how we know it: **tested** (with the version) or **docs**. A
tested fact from an older version is a lead, not a guarantee: re-test before you
build on it.

## Find out, don't guess

Most wrong answers about Claude Code come from assuming the subagent, the plugin
or the headless run behaves like the session you are in. It usually doesn't.

| Question | Fastest true answer |
|---|---|
| What does this session have loaded? | `claude -p --output-format stream-json --verbose`: its `init` event lists `tools`, `skills`, `agents`, `plugins`, `slash_commands` and every `mcp_servers` entry with its status |
| What does a subagent really get? | Spawn it with "list every tool you have, loaded and deferred, grouped by MCP server prefix". Ask it, don't infer it from the definition |
| Does X work with these flags or this agent file? | A headless probe, prompt on stdin. [headless.md](references/headless.md) |
| What does an MCP server really offer? | `curl` its `initialize`, then `tools/list`. [mcp.md](references/mcp.md) |
| What does a field or flag mean? | The page in [docs-map.md](references/docs-map.md) |

## References

Load only the one you need.

| Topic | Read |
|---|---|
| Subagents: agent files, every frontmatter field, tools vs MCP servers, `--agent` vs subagent, which agents an agent may call | [agents.md](references/agents.md) |
| Prompts: plugin commands, MCP prompts, arguments, why one is missing from the slash menu | [prompts.md](references/prompts.md) |
| MCP: where servers come from, `--strict-mcp-config`, instructions, resources vs tools, skills served over MCP | [mcp.md](references/mcp.md) |
| Headless: `claude -p`, `--agents`/`--agent`, settings and hooks, channels, cost | [headless.md](references/headless.md) |
| Plugins: layout, what plugin agents ignore, `${CLAUDE_PLUGIN_ROOT}`, where to keep agents | [plugins.md](references/plugins.md) |
| Which official page answers what | [docs-map.md](references/docs-map.md) |

## Common mistakes

| Mistake | Instead |
|---|---|
| Telling a subagent to read a `skill://` (MCP resource) skill | A background subagent has no `ReadMcpResourceTool`. Serve the skills as MCP tools, on an MCP server in the agent's own `mcpServers` ([agents.md](references/agents.md)) |
| `tools: [mcp__a__x]` to limit an agent to one tool of its own MCP server | `tools` doesn't filter the agent's own `mcpServers`. Add `disallowedTools` for the rest |
| `- grafana` (a name) in `mcpServers` of an agent that runs under `--strict-mcp-config` | A name only reuses a session server, and strict removed it. Write the full definition |
| Counting on a subagent to see MCP server instructions | Sometimes it does, sometimes not. Name the starting point in the agent's own prompt |
| `mcpServers`, `hooks` or `permissionMode` on a plugin's agent | Ignored there. Use a user or project agent file |
| `claude -p --allowedTools 'x' "the prompt"` | `--allowedTools` takes every word after it. Pipe the prompt on stdin |
| Saying a new agent file is ready in the open session | It may not show until a later turn or a new session. Check the agent list first |
| A channel to message a headless run | Channels never register in `-p`. Use hooks that read an inbox ([headless.md](references/headless.md)) |
| An MCP prompt missing from the slash menu, blamed on Claude Code | Time that server's list calls; a slow server misses the menu ([prompts.md](references/prompts.md)) |
| MCP server instructions longer than 4,096 characters | They are cut. Shorten, or point at a skill that holds the rest |
| Naming a plugin `claude-code`, `claude-…` or `cc-plugin-…` | Reserved; `claude plugin validate` refuses it. Name it for what it does ([plugins.md](references/plugins.md)) |
| `claude mcp serve` as a way to run an agent | It is tool-only: no model, so `Skill` and `Agent` are stubs. Use `claude -p` |

## Add what you learn

When Claude Code surprises you, write it down where the next agent will look: a
row in Common mistakes, a line in the matching reference, or a new reference
copied from [_template.md](references/_template.md). One or two lines each, and
always how you know: **tested** (version, and how), or **docs** (the page). If
you can't edit this skill, tell the user what to add.
