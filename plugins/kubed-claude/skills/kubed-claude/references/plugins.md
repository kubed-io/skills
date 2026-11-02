# Plugins

A plugin is a folder Claude Code installs from a marketplace (a git repository
with `.claude-plugin/marketplace.json`). Add one with `/plugin marketplace add
<owner>/<repo>`; a plugin installs as `<plugin>@<marketplace>`.

```
plugins/<plugin>/
  .claude-plugin/plugin.json   name, version, description
  skills/<skill>/SKILL.md      /<plugin>:<skill>, and the model can load it
  commands/<name>.md           /<plugin>:<name>
  agents/<name>.md             subagents, with fields ignored (below)
  hooks/, .mcp.json            hooks and MCP servers for every session it is on in
```

- **Bump `version`** in `plugin.json` when a change should reach installed
  copies.
- **Names are policed.** `claude plugin validate <dir>` refuses a third-party name
  that is `claude`, `claude-code`, `anthropic`…, or starts with `claude-`,
  `anthropic-` or `cc-plugin-`; one that merely contains `claude` passes with a
  warning. It also warns when there's no icon. Run it before the first push.
  (Tested 2.1.316.)
- `${CLAUDE_PLUGIN_ROOT}` in a body is the plugin's folder. kubed-io/mcp-kb
  rewrites it to `skill://<library>` when it serves the plugin.
- A plugin's MCP servers load into the **main** session. For a server only one
  agent should have, use a user or project agent with inline `mcpServers`.

## What a plugin agent ignores

Docs: `mcpServers`, `hooks` and `permissionMode` (and `initialPrompt`). A plugin
can't ship an agent that carries its own MCP servers. An agent that needs them
lives in `.claude/agents/` or the user's `agents/`, or is passed with `--agents`.

## Where to keep agents

| Agents for | Keep them in | Because |
|---|---|---|
| One repository | `.claude/agents/`, committed | Versioned with the code they serve |
| You, everywhere on one machine or shared config dir | `$CLAUDE_CONFIG_DIR/agents/` (or `~/.claude/agents/`) | Every session and every headless job sharing that config dir sees them. Keeps `mcpServers` and `hooks` |
| Anyone, anywhere | A plugin | Installable and versioned, but loses `mcpServers`, `hooks`, `permissionMode` |
| One CI job | `--agents '<json>'` built from a file | Highest priority below managed settings; no file left behind |

A config dir is live state, not history: keep the agent files in a repository
and copy them in. Never commit the config dir itself (`.credentials.json`,
`.claude.json` hold secrets).

Agents written for a job (they read job files, never commit, answer in a schema)
mislead in a chat. Keep job agents with the job and chat agents in the shared
dir. An `--agent` main session with `tools: Agent(a, b)` keeps the rest of the
shared dir out of its reach ([agents.md](agents.md)).
