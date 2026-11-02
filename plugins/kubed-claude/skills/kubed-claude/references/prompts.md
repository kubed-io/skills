# Prompts

A **skill** is read by the model when it decides to. A **prompt** is picked by a
person, as a slash command, who may fill in arguments before the model sees
anything. Claude Code gets prompts from three places, and all of them land in
the same slash menu.

## Where slash commands come from

Tested 2.1.316 (`init` event of a `-p` run):

| Source | Shows as | Example |
|---|---|---|
| `.claude/commands/<name>.md`, `.claude/skills/<name>/` | `/<name>` | `/new-app` |
| A plugin's `commands/<name>.md` or `skills/<name>/` | `/<plugin>:<name>` | `/anthropic-skills:pdf` |
| An MCP server's prompts | `/mcp__<server>__<prompt>` | `/mcp__kb__superpowers_review` |

A user-invocable skill is a slash command too: the `skills` list and
`slash_commands` overlap.

## A command file

Commands and skills are one thing now (docs): `.claude/commands/deploy.md` and
`.claude/skills/deploy/SKILL.md` both make `/deploy`, with the same frontmatter.
A skill folder can also hold files, and the model can load it by itself.

```markdown
---
description: Open an incident for a workload.
argument-hint: "[app] [severity]"
arguments: [app, severity]
---
Open an incident for $app at severity $severity.
```

| Placeholder | Means (docs) |
|---|---|
| `$ARGUMENTS` | Everything typed after the command |
| `$ARGUMENTS[N]`, `$N` | One word, **0-based**: `$0` is the first. Quote multi-word values |
| `$name` | A name from `arguments:`, by position |
| none in the body | The text is appended as `ARGUMENTS: <text>` |

- `description` is what the menu shows and what the model matches on.
  `disable-model-invocation: true` makes it person-only; `user-invocable: false`
  model-only.
- **Quote `argument-hint`.** Bare `[app] [severity]` is two YAML lists in a row,
  which a strict parser rejects (mcp-kb skips the file and says why in `/health`).
- In a local command, `` !`cmd` `` (or a ```` ```! ```` block) runs before the
  model sees the body and is replaced by its output; `@path` attaches a file
  (docs). Served over MCP, or synced, they stay plain text: nothing fetched is
  executed.
- `context: fork` runs it in a subagent (`agent:` picks which).

## Prompts served over MCP

An MCP server can serve prompts (`prompts/list`, `prompts/get`). Claude Code
lists them as `/mcp__<server>__<prompt>` and asks for the arguments.

| Thing | What to know |
|---|---|
| Argument types | Strings only. A free-text argument is how `$ARGUMENTS` travels |
| Name | One flat namespace per server; the client adds the server. mcp-kb names them `<library>_<file stem>` so two libraries' `debug.md` don't collide |
| A prompt missing from the menu | The menu is built from servers that answered in time. Time the server's `prompts/list` and `resources/list` before blaming the client. Tested 2.1.270: a 5 s `resources/list` hid its prompts. `"alwaysLoad": true` on the server makes startup wait (capped at 5 s) |
| `${CLAUDE_PLUGIN_ROOT}` in a served body | mcp-kb rewrites it to `skill://<library>`, so a prompt can point at its plugin's skill |
| Client-only placeholders (`${CLAUDE_PROJECT_DIR}`, `@path`) | Served as written; the model reads them as text |
| A client without prompts (n8n) | mcp-kb's `?prompts=off` mirrors them as tools: `list_prompts`, `get_prompt` |

kubed-io/mcp-kb serves the same file whether it is a Claude command, a Copilot
`.prompt.md` or its own dialect. Its wiki page *Prompts* has the details.

## Prompt or skill?

| When | Use |
|---|---|
| A person starts it, with a few blanks to fill | Prompt (command) |
| The model should find it when the task calls for it | Skill |
| A headless agent's turn ("the plan was approved, carry on") | A prompt the workflow fetches and sends as the turn. kubed-io/skills' `ultrapowers` is this |

## Headless

`-p` has no menu, but a command still resolves: send `/<name> args` as the
prompt (tested 2.1.316, a project skill ran from `echo "/name" | claude -p`). The
`init` event's `slash_commands` lists what is available.
