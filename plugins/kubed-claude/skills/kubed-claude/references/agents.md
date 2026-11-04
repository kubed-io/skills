# Agents

A subagent is a Markdown file: YAML frontmatter, then a body that becomes its
system prompt. The same file can run two ways: as a **subagent** the main
conversation delegates to, or as the **main session** with `claude --agent <name>`.
What it gets differs a lot between the two.

## Where agent files come from

When two share a name, the higher one wins (docs).

| Priority | Location | Notes |
|---|---|---|
| 1 | Managed settings | Organisation-wide |
| 2 | `--agents '<json>'` | This session only. JSON keys mirror the frontmatter; `prompt` is the body |
| 3 | `.claude/agents/` | The project |
| 4 | `~/.claude/agents/` | The user. With `CLAUDE_CONFIG_DIR` set, it is `$CLAUDE_CONFIG_DIR/agents/` |
| 5 | A plugin's `agents/` | Lowest, and ignores several fields ([plugins.md](plugins.md)) |

A user or project agent named like a built-in (`Explore`) replaces it (docs).

**New files mid-session** (docs: picked up within seconds, no restart). Tested
2.1.316 in VS Code: a new `.claude/agents/` file was not callable a minute later
("Agent type not found"), and was by the next user turn. The watcher only
covers directories that existed at session start: create `agents/` and the first
file needs a new session.

## Frontmatter fields

From the docs page, 2026-11. Only `name` and `description` are required.

| Field | What it does |
|---|---|
| `name` | Unique id, at most 256 characters, no `:` (reserved for `plugin:agent`). Needn't match the filename |
| `description` | When to delegate. The main agent sees only this, so it is the routing rule |
| `tools` | Allowlist, a string `Read, Bash` or a YAML list. Omitted: everything subagents get. `mcp__server__*` patterns work. **Doesn't filter the agent's own `mcpServers`** (below) |
| `disallowedTools` | Denylist, applied before `tools`. `Bash(git push *)` still removes all of Bash. **Does** remove the agent's own servers' tools |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, a full id, or `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, `manual` |
| `maxTurns` | Stops after N turns; the output comes back marked partial and can be resumed |
| `autoCompactWindow` | Compact earlier: a plain integer from 100000 to 1000000 (`200k` reads as 200 and is ignored) |
| `skills` | Preloads these skills' full text at startup. The agent can still load any other skill with the Skill tool |
| `mcpServers` | A name (reuse a session server) or an inline definition (connects when the agent starts, disconnects when it ends) |
| `hooks` | Hooks that apply only while this agent runs |
| `memory` | Persistent memory: `user`, `project` or `local` |
| `background` | `true` keeps it in the background even when asked to wait |
| `omitClaudeMd` | `true` starts it without the CLAUDE.md files |
| `effort` | `low` to `max` |
| `isolation` | `worktree`: a temporary git worktree, branched from the default branch |
| `color` | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | First user turn, only when it runs as the main session |
| `experimental` | Map; today only `cacheTtl: 5m` or `1h` |

## What a subagent gets

It starts fresh (docs): its own prompt plus environment details (not Claude
Code's system prompt), the delegation message, the CLAUDE.md files, a git status
snapshot, and any `skills` it preloads. Not your conversation, not the skills
you loaded, not the files you read. A **fork** is the exception: it inherits the
whole conversation, system prompt and tools.

### Tools: inherited, then filtered

Subagents inherit the session's built-in and MCP tools, then two filters apply (docs):

1. **Every subagent loses** `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode`
   (unless `permissionMode: plan`), `ScheduleWakeup`, `Workflow`, and `Agent` at
   the depth limit.
2. **A background subagent**, which is the default from the main conversation,
   keeps every MCP tool but only these built-ins: `Read`, `Grep`, `Glob`, `LSP`,
   `Bash`, `PowerShell`, `Edit`, `Write`, `NotebookEdit`, `WebFetch`,
   `WebSearch`, `TodoWrite`, `Skill`, `ToolSearch`, `EnterWorktree`,
   `ExitWorktree`, `Monitor`, `TaskStop`, `SendMessage`, `Artifact`.

So a background subagent has **no `ReadMcpResourceTool` or
`ListMcpResourcesTool`**. Tested 2.1.316: it could see the MCP server's
instructions listing `skill://…` URIs, and had no tool that could read one. A
subagent in a `claude -p` run did list `ReadMcpResourceTool`.

**Skills over MCP in a subagent.** Expose them as MCP *tools* and give the agent
that server inline. kubed-io/mcp-kb does this with `?resources=off`
(`list_resources`, `read_resource`). Tested 2.1.316:

```yaml
---
name: kb-reader
description: Reads skills from the knowledge base for tasks that need one.
mcpServers:
- kb-tools:
    type: http
    url: http://kb.example.svc:8000/mcp?resources=off&prompts=off
---
Start with list_resources, then read_resource on skill://<library>/_index.md.
```

The main session never sees `kb-tools`. The body names the starting point
because the subagent may not get the server's instructions (below).

### Tools the main agent doesn't have

Built-in tools are always a subset of the session's. **MCP tools needn't be:**
an inline `mcpServers` entry gives the agent tools the main conversation never
loads, and keeps their descriptions out of its context (docs; tested 2.1.316).
Agents that each carry their own servers, found by their `description`, is how
to stop loading every tool into the main session.

### `tools` vs the agent's own MCP servers

Tested 2.1.316 with two inline servers of four tools each:

| Frontmatter | Result |
|---|---|
| `tools: [mcp__a__read]` | Built-ins and session servers gone. **All eight tools of `a` and `b` kept**, and an unlisted one worked |
| `disallowedTools: [mcp__b]` | Every `b` tool gone, the rest kept |

The docs call `tools` an allowlist and don't mention this; it may change. To
narrow an agent's own server, use `disallowedTools`, or scope the server itself.

### Inline server vs session server

Tested 2.1.316:

| Case | Result |
|---|---|
| Inline entry with the same name as a session server | The inline one replaces it, for this agent only. The main session keeps its own |
| Different names | Added: the agent has the session's servers and its own |
| A name reference (`- grafana`) to a server the session doesn't have | Silently missing. No error, no warning |
| Session started with `--strict-mcp-config` | Session gets only `--mcp-config` servers; inline servers still connect for the agent |

### MCP server instructions

Not reliable in a subagent. Across tested runs (2.1.316) a subagent saw none,
saw them only later attached to a tool result, or saw every session server's
instructions while having none of their tools. Put what the agent must know in
its body.

## `--agent` vs a subagent

| | `claude --agent foo` | `foo` as a subagent |
|---|---|---|
| System prompt | The body **replaces** Claude Code's prompt (like `--system-prompt`), unless empty | The body plus environment details |
| Conversation | It is the conversation | Fresh; returns one final message |
| Tools | No background filter: `AskUserQuestion`, resource tools, all of it, narrowed by `tools` | Filtered as above |
| `initialPrompt` | Sent as the first turn | Ignored |
| `omitClaudeMd`, `autoCompactWindow` | Ignored | Apply |
| The agent's own `mcpServers` | **Don't connect.** Give the servers with `--mcp-config`, `.mcp.json` or a plugin, and narrow them with `tools` | Connect for the run |

**tested** 2.1.316: an agent's `mcpServers` were ignored under `--agent`, whether
it came as `--agents` JSON or as a project agent file, with or without
`--strict-mcp-config`. The same `--agents` definition run as a subagent connected
its server. A plugin's own MCP servers do reach an `--agent` plugin agent through
`tools` (a whole server can be one entry, `mcp__plugin_<plugin>_<server>`), but
`--strict-mcp-config` drops plugin servers. Agents a mod registers can't be
picked with `--agent` at all: the name is resolved before the mod runs. Nor can
a `SessionStart` hook write the file in time: an unknown `--agent` name fails
before any hook runs. A dynamic main agent has to exist before launch, as
`--agents` JSON or a file a step wrote first.

**`tools` lists what exists; it grants nothing.** Under `claude -p`, an MCP tool in
an agent's `tools` was still denied ("you haven't granted it yet") until
`permissions.allow` named it. No frontmatter field grants permissions. A rule
can cover one server (`mcp__plugin_ap_kbA`, `mcp__plugin_ap_kbA__*`), not a
plugin's servers (`mcp__plugin_ap_*` was denied). A plugin's own `PreToolUse`
hook returning `permissionDecision: "allow"` for `mcp__plugin_<plugin>_.*`
approved them with no allow list; one with no matcher approved Bash and Write too, and a
`permissions.deny` rule still won over it. **tested** 2.1.316

The `agent` **setting** does what `--agent` does: `--settings
'{"agent":"kubed-runner:spec",…}'` made a plugin agent the main session, with its
`tools`. The agent's own `model` beat the settings' `model`. **tested** 2.1.316

An agent that reads `skill://` resources fine under `--agent` breaks when the
same file runs as a background subagent.

## Which agents an agent may call

| Want | Do | Scope |
|---|---|---|
| Only some subagent types | `tools: Agent(worker, researcher), Read, …` | Only for the `--agent` main session. In a subagent the list is ignored |
| No subagents | Leave `Agent` out of `tools` | Any |
| Any subagent | Omit `tools`, or plain `Agent` | Any |
| Block some types everywhere | `permissions.deny: ["Agent(Explore)"]` or `--disallowedTools "Agent(Explore)"` | Session |
| No Explore and Plan | `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` | Session |
| No built-ins at all | `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` | Headless and SDK only |
| Limit nesting | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (default 3; `1` = none) | Session |

All docs. With `tools:` set, every other tool the agent needs must be listed too.
