# Headless

`claude -p` runs one prompt with no UI, for CI, scripts and experiments. It loads
the same project skills, agents, plugins and MCP servers as an interactive
session.

## A probe

The quickest way to settle "does Claude Code do X?":

```bash
cat > prompt.txt <<'EOF'
Delegate to the subagent `probe` this task: "List every tool you have, loaded and
deferred, grouped by MCP server prefix. Facts only." Relay its answer verbatim,
then answer the same for yourself.
EOF
claude -p --agents "$(cat agents.json)" --allowedTools 'mcp__x__*' < prompt.txt
```

- **Prompt on stdin.** `--allowedTools` and `--disallowedTools` take every word
  after them, so a prompt argument behind them is swallowed ("Input must be
  provided…"). Tested 2.1.316.
- `--agents '<json>'` defines throwaway agents without touching `.claude/agents/`:
  `{"probe": {"description": "…", "prompt": "…", "tools": […], "mcpServers": […]}}`.
- Ask the agent to report; don't infer from its definition. Compare two runs
  that differ in one flag.
- A tool the run isn't allowed comes back as "Claude requested permissions to
  use X, but you haven't granted it yet". Allow it, or expect it.

## Seeing what loaded

`--output-format stream-json --verbose` starts with hook events, then an `init`
event (`subtype: init`) holding `tools`, `skills`, `agents`, `plugins`,
`slash_commands`, `mcp_servers` (name and status) and `claude_code_version`.
Read that instead of asking the model.

## Flags that shape a run

| Flag | Does |
|---|---|
| `--agent <name>` | Run the session as that agent: its body replaces the system prompt ([agents.md](agents.md)) |
| `--agents '<json>'` | Session-only agent definitions, priority above project and user files |
| `--mcp-config <file>`, `--strict-mcp-config` | Add servers, or use only those ([mcp.md](mcp.md)) |
| `--settings <file>` | Settings and hooks for this run |
| `--json-schema '<schema>'` | Structured final output |
| `--permission-mode`, `--allowedTools`, `--disallowedTools`, `--max-turns`, `--model` | As named |
| `--output-format json` | One result object, with `session_id`; `--resume <id>` continues it |

## Settings and hooks

With `CLAUDE_CONFIG_DIR` set, `~/.claude/settings.json` is never read: the
user settings are `$CLAUDE_CONFIG_DIR/settings.json`. claude-code-action's
`settings` input writes the former. Pass a run's hooks with `--settings <file>`.

## Messages mid-run

A channel (`notifications/claude/channel`) never registers in `-p`, stream-json
input, the Agent SDK or claude-code-action; it is dropped silently. To reach a
running headless agent, keep the MCP server as an inbox and add a
`PostToolBatch` hook and a `Stop` hook that return new lines as
`additionalContext`. (Tested on a self-hosted runner, 2026-10.)

## Differences from an interactive session

| | Headless (`-p`) | Interactive |
|---|---|---|
| Slash commands | Send `/<name> args` as the prompt; it resolves | Menu |
| MCP sign-in | Impossible: OAuth servers that need it are skipped | Browser flow |
| A subagent's resource tools | Listed (tested 2.1.316) | Missing in background subagents |

## Cost

Every `-p` run primes Claude Code's system prompt again: a one-line Haiku answer
cost about $0.02 (tested 2.1.220). Fine for a probe or a job, wrong for a tool
called in a loop.
