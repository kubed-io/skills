# MCP

## Where a session's servers come from

| Source | Notes |
|---|---|
| `.mcp.json` in the project | Needs approval, or `enableAllProjectMcpServers: true`. `${VAR}` is expanded from the environment |
| The user config (`claude mcp add`) | In `.claude.json` under `CLAUDE_CONFIG_DIR` or the home directory |
| claude.ai connectors | Added on claude.ai, show up as `claude.ai <Name>`, tools `mcp__claude_ai_<Name>__…`. Can be disabled per project in `/mcp` |
| An enabled plugin's MCP servers | Load into the main session, for every conversation the plugin is on |
| `--mcp-config <file>` | Added to the above |
| An agent file's `mcpServers` | Only that agent ([agents.md](agents.md)) |

`claude mcp list` shows each server's status: connected, needs authentication,
or disabled for this project.

### `--strict-mcp-config`

Tested 2.1.316: the session gets **only** the `--mcp-config` servers. `.mcp.json`,
the user config and the claude.ai connectors are all gone. An agent's inline
`mcpServers` still connect for that agent; a name reference to a server strict
removed is silently missing. Without strict, `--mcp-config` adds to everything
else. kubed-io/actions' issue-agent merges into one file because
claude-code-action keeps only the last of several `--mcp-config` flags.

## Server entry keys worth knowing

| Key | Does |
|---|---|
| `headers` | Static headers. `${VAR}` expands |
| `headersHelper` | A command whose stdout is a JSON object of headers, e.g. `{"Authorization": "Bearer …"}`. Good for client-credentials tokens in CI |
| `oauth: {clientId, callbackPort}` | OAuth with a fixed client and callback port. A non-interactive session can't sign in: the server shows `needs-auth` and its tools are missing |
| `alwaysLoad: true` | Startup waits for this server (capped at 5 s, tested 2.1.270) |

## Instructions

A server's `instructions` (from `initialize`) go into the main session's system
prompt and survive compaction; resource reads don't. Claude Code cuts them at
**4,096 characters** (`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` changes it). A
gateway that merges several servers merges their instructions into one budget,
and whatever comes last is cut first. A subagent may not see them at all
([agents.md](agents.md)).

## Tools, resources, prompts

| Primitive | In Claude Code |
|---|---|
| Tools | `mcp__<server>__<tool>`; spaces and dots in the server name become `_`. Most are **deferred**: only names are listed until `ToolSearch` (`select:<name>`) loads the schema |
| Resources | Read through the built-ins `ListMcpResourcesTool`, `ReadMcpResourceTool`, `ReadMcpResourceDirTool` (deferred). Directory listing needs server support; FastMCP has none |
| Prompts | Slash commands `/mcp__<server>__<prompt>` ([prompts.md](prompts.md)) |

The resource tools are built-ins, so a **background subagent doesn't have
them**. Anything a subagent must read should be a tool.

## Skills served over MCP

A server can serve skills as resources (`skill://<library>/<name>/SKILL.md`), as
kubed-io/mcp-kb does. Claude Code reads them with the core resource tools only;
it doesn't use the MCP skills extension (`skills/list`, `skills/get`). So:

| Reader | Works |
|---|---|
| The main session | Yes, with `ReadMcpResourceTool`. Instructions that name the index help it start |
| A background subagent | No. Give the agent the server in tools mode (mcp-kb: `?resources=off` → `list_resources`, `read_resource`) |
| A client without resources (n8n, claude.ai) | Tools mode again |
| Behind a multiplexing gateway (agentgateway) | Resource URIs are rewritten to `<target>+<uri>` and bare ones refused. Tools mode, or a resource prefix the server applies itself |

## Long-running work

**docs** (`mcp`, Claude Code 2.1.316; MCP spec 2026-07-28):

- **No monitors in MCP.** A plugin monitor (`monitors/monitors.json`) is a shell
  command whose output reaches Claude as notifications. It is interactive only, and
  never starts under `-p`.
- **MCP tasks:**
  - **What it is.** The tasks extension, `io.modelcontextprotocol/tasks`. In
    2025-11-25 tasks were core and experimental; in 2026-07-28 they are an
    extension.
  - **How it runs.** A server answers `tools/call` with `resultType: "task"`.
    Claude Code then polls `tasks/get`, may send `tasks/cancel`, and doesn't use
    `tasks/result` or `tasks/list`.
  - **Where it works.** Beta, 2.1.304+, main conversation only (never a subagent),
    on the 2026-07-28 runtime. Interactive sessions, or `-p --input-format
    stream-json` with `CLAUDE_AUTO_BACKGROUND_TASKS=1`. A one-shot `claude -p
    "…"` gets none.
- **Plain long calls.** A main-conversation call past two minutes moves to
  `/tasks` (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`). `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`
  turns that off, and issue-agent sets it. Progress notifications keep a call
  alive against the idle timeout, not the wall-clock one.
- **Watching data.** Claude Code acts on `list_changed`. Its docs never mention
  `resources/subscribe` / `notifications/resources/updated`, so assume they're not
  used until tested.

## Probe a server by hand

```bash
U='http://server.example.svc:8000/mcp'
H=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')
curl -sS -D headers.txt "${H[@]}" "$U" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}'
SID=$(grep -i mcp-session-id headers.txt | awk '{print $2}' | tr -d '\r')
curl -sS "${H[@]}" -H "Mcp-Session-Id: $SID" "$U" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
curl -sS "${H[@]}" -H "Mcp-Session-Id: $SID" "$U" -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

Replies arrive as server-sent events: take the `data: ` line. The `initialize`
reply shows the capabilities and the instructions exactly as Claude Code gets
them. Time `tools/list`, `resources/list` and `prompts/list` when something is
missing from a session ([prompts.md](prompts.md)).

## `claude mcp serve`

Claude Code as an MCP server: **tools only** (no resources, no prompts), and no
model. `Bash`, `Read`, `Write` really run, with no approval prompt, so never
expose it. `Skill` and `Agent` are stubs. To run an agent, use `claude -p`.
(Tested 2.1.220.)
