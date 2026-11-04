# Hooks

What runs when a Claude Code event fires: settings hooks (five handler types)
and mods (a plugin's own code, running inside Claude Code). Open it before you
reach for a wrapper script.

## Handler types

A settings hook is more than a script path. **docs** (`hooks`)

| `type` | Runs | Answers through |
|---|---|---|
| `command` | A shell command, event JSON on stdin. `args` makes it exec form (no shell, safe for `${CLAUDE_PLUGIN_ROOT}` paths). `async`, and `asyncRewake` to wake Claude on exit 2 | Exit code, stdout |
| `http` | POSTs the event JSON to `url`. `headers` may use env vars only if listed in `allowedEnvVars` | A 2xx JSON body. Plain text or non-2xx is a non-blocking error, never context |
| `mcp_tool` | `tool` on a connected MCP `server` (a plugin's: `plugin:<plugin>:<server>`). `input` strings take `${tool_input.file_path}`-style paths from the event | The tool's text, read like stdout. `isError` is a non-blocking error |
| `prompt` | One model call; `$ARGUMENTS` is the event JSON | A JSON decision |
| `agent` | A subagent with Read, Grep, Glob (experimental) | A JSON decision |

Every type takes `if` (one permission rule, tool events only, best-effort),
`timeout`, `statusMessage`, and `onFailure: block` (2.1.295+). `once` works only
in skill frontmatter.

## Where hooks live

| Place | Active |
|---|---|
| Settings: user, project, local, managed | Always. Levels add up; they don't replace each other |
| A plugin: `hooks/hooks.json`, `plugin.json`, or inline in its marketplace entry | While the plugin is on |
| Skill frontmatter | From the skill's first use to the end of the session |
| Agent frontmatter | While that agent runs. `Stop` becomes `SubagentStop`. Ignored on a plugin's agent |

Settings and plugin hooks also fire inside subagents; the input then carries
`agent_id` and `agent_type`.

## Events worth knowing

- **`SessionStart`** takes only `command` and `mcp_tool`, and an `mcp_tool` hook
  is **skipped at launch** (no MCP servers yet; it runs after `/clear` or a
  compaction). It can return `additionalContext`, `initialUserMessage` (`-p`),
  `sessionTitle`, `watchPaths`, and `reloadSkills: true` so skills it just wrote
  load this session. `CLAUDE_ENV_FILE` sets env for later Bash calls. **docs**
- **`Setup`** fires only on `--init-only`, or `-p --init` / `--maintenance`.
- Others: `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`,
  `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`,
  `PostToolBatch`, `SubagentStart`/`Stop`, `TaskCreated`/`Completed`, `Stop`,
  `StopFailure`, `PreCompact`/`PostCompact`, `ConfigChange`, `CwdChanged`,
  `DirectoryAdded`, `FileChanged`, `InstructionsLoaded`, `Pre`/`PostModelSwitch`,
  `Elicitation`/`ElicitationResult`, `Notification`, `MessageDisplay`,
  `WorktreeCreate`/`Remove`, `TeammateIdle`, `SessionEnd`.

## Mods: hooks as code

A plugin whose `hooks/hooks.json` has `"modules": ["./register.js"]` loads that
module inside Claude Code. Its handlers can rewrite prompts, tool calls, skill
text and the system prompt, withhold agent types (`agent.offer`), draw
panes, and see every settings-hook event as `classic.<Event>`. They run in `-p`
too, without the drawing. **docs** (`plugins/mods/*`)

What it can add at `session.start` (Claude Code waits for that handler before
the first prompt):

| Call | Result |
|---|---|
| `$.tool.register` | A tool named `mcp__<plugin>__<name>`, answered in a `tool.call` handler |
| `$.command.register` | A `/command` that runs code with no Claude turn |
| `$.agent.register({ name, description, prompt, tools, model, mcpServers })` | An agent `<plugin>:<name>`, and **its inline `mcpServers` connect**, which a plugin's `agents/*.md` can't do. **tested** 2.1.316, `-p --plugin-dir` |
| `$.http.fetch(url)` | Works from the pod to cluster services. Returns `{ status, ok, headers, text }`: no `.json()`. **tested** 2.1.316 |

`$.mcp.call` reaches only tools, and `$.mcp.connect` only the plugin's own
servers. The type files for your build (`.claude-plugin/types/`) are written
only for an interactive `--plugin-dir` session, not `-p`.

**Shipping a mod.** It is plain `.js` or `.ts` (ES module) files inside the
plugin, loaded as they are: no `package.json`, no build, no npm. A hooks module
imports only its own files by relative path, plus `claude-code`. `claude plugin
validate` refuses `'yaml'` and even `'node:fs'`; use `$.fs`, `$.http` and
`$.process` instead, and vendor a library as a relative file. **tested** 2.1.316.
npm packages work only by relative path, and only if every file they reach is an
ES module that imports nothing but relative files. **tested** 2.1.316:

| `import` in the mod | Result |
|---|---|
| `'../node_modules/yaml/browser/index.js'` (pure ESM) | Loads and runs |
| `'../node_modules/yaml/dist/index.js'` (CommonJS) | Passes `validate`, then fails at load: `Missing 'default' export` |
| An ESM package that imports `'node:fs'` | Refused by `validate` and at load; the check follows imports |

A plugin with `package.json` and an npm or Bun lockfile gets `node_modules`
installed into its cache copy at install time. That doesn't happen for a plugin
loaded in place, so run `npm install` yourself there. The install has no scripts,
uses exact registry versions, and must finish in 60 s. Tests run with
`claude plugin test` (`*.test.ts`, imports `claude-code/testing`).

A mod is unsandboxed code with your permissions. `claude plugin validate`
lists the events it hooks and every `$` call it makes; read that first.

## Gotchas

- **Testing a permission hook with `echo` proves nothing:** read-only Bash
  commands run without asking anyway. Use `touch` or a Write. **tested** 2.1.316
- **An approve-all `PreToolUse` hook needs a guard.** `agent_type` in a tool
  call's input is the `--agent`/`agent`-setting agent, but inside a subagent it's
  the subagent's type. kubed-runner's guard has two parts:
  - its `SessionStart` hook records a `session_id` whose `agent_type` is
    `kubed-runner:*`;
  - its `PreToolUse` hook approves only recorded sessions.

  That covers the entry agent and its subagents, and nothing else. **tested**
  2.1.316
- **A plugin `headersHelper` sees the settings' `env`** and the job's environment,
  but no plugin options. **tested** 2.1.316

- An `mcp_tool` hook can't feed a session's start. Use a `command` hook.
- An `http` hook's URL must match `allowedHttpHookUrls` when any settings level
  sets it.
- A mod writes each `$` call in full (`$.agent.register(...)`), never
  `const a = $.agent`. Static analysis refuses the rest. A helper that takes `$`
  must be a function declared at the top of the file (or imported from the
  mod's own files), not a closure inside `register`. **tested** 2.1.316
- **`--strict-mcp-config` drops a mod-registered agent's own `mcpServers`.** The
  agent runs, and its inline server never connects. A file agent's inline servers
  do connect under strict (agents.md). **tested** 2.1.316
- `$.agent.register` takes effect from the next turn, so a `/command` can load
  agents again mid-session. A type can't be unregistered: hide a stale one with
  an `agent.offer` hook returning `{ isOffered: false }`.
- **A mod agent's own servers sign in** with static `headers` or a `headersHelper`
  (an absolute path; `$.plugin.root` is the mod's folder). A settings `env` value
  reaches `$.env.get`, so a mod can fetch a token itself and re-register its
  agents before it expires. **tested** 2.1.316
- **A `tool.call` hook on Read can answer a file that doesn't exist**, outside the working
  directories, with no prompt: it runs before validation and permissions. Its
  `{ result: { type: 'text', file: { filePath, content, numLines, startLine, totalLines } } }`
  reaches the model numbered like a real read. A hook on Bash can write files before `next(e)`;
  a script outside the working directories then needs only its Bash rule. **tested** 2.1.317
- **`$.fs.write` writes text files anywhere** (outside the working directories, in the
  scratchpad), but no bytes: a `Uint8Array` or `{ base64 }` is refused ("takes the text to
  write"). **tested** 2.1.317
- **A mod reads any connected server's resources with `$.tool.call({ tool:
  'ReadMcpResourceTool', server, uri })`**, on the session's own connection and sign-in (kb and
  penpot's `kb+skill://` through agentgateway, selenium-flow). `$.mcp.call` can't: it reaches a
  server's own tools only. Call it from a hook, not `session.start`. **tested** 2.1.317
- A mod has no scratchpad API, but the folder is `/tmp/claude-<uid>/<cwd with / as ->/<session
  id>/scratchpad` (`$.session.id()`); a mod's files there run like any other. Under `-p` the
  folder may not exist yet: the project's folder does. Seen, not documented. `$.fs.list` kinds
  are `file`, `dir`, `other`. **tested** 2.1.317
- **A Bash hook can rewrite the command**: `next({ ...e, command })`. A model's `python3
  skill://drawio/drawio/scripts/check.py f` ran after the hook wrote the file to the scratchpad and
  swapped the URI for its path; the permission rule (`Bash(python3 *)`) matched the rewritten
  command, and the transcript keeps the model's. A matcher takes literals only (a RegExp selects
  nothing), so the hook takes every Bash call and scans it. **tested** 2.1.317
- **Auto mode won't judge a rewritten call.** Its classifier reviews the model's input, so a
  hook that changes it gets "no verdict: a hook changed this call's input", with the rewritten
  input to send again. The model's second, identical call passes. A permission rule that matches
  the rewritten command (`Bash(python3 *)`) skips the classifier and the round trip. **tested**
  2.1.317
- **`prompt.compose` runs only for the default prompt.** A section added there never reaches an
  `--agent` main session or a subagent: an agent's own prompt replaces the default, and nothing is
  composed. To tell every session something, a mod answers `classic.SessionStart` (main sessions,
  `--agent` ones too) and `classic.SubagentStart` with `{ ...await next(e), additionalContext:
  [text] }`. **tested** 2.1.317, each with its own code word
