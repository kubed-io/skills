# AGENTS.md

A public plugin marketplace. Claude Code installs from it, and kubed's mcp-kb serves it over MCP
(`github://kubed-io/skills?ref=<sha>`, one library, scoped by each plugin's `category`).

## Layout

```
.claude-plugin/marketplace.json     every plugin, with its category
plugins/<plugin>/
  .claude-plugin/plugin.json        name, version, description
  skills/<skill>/
    SKILL.md                        short: when, how, common mistakes, where to look next
    references/                     loaded on demand; one topic per file
    evals/<case>/                   test cases in the `claude plugin eval` layout
```

## Writing a skill

- Start from a failing run, not from what seems useful: run the task without the skill, see what
  the agent gets wrong or wastes, and write the skill against that. Re-run with it.
- `description` says when to use the skill, never how it works. Agents follow a summary instead
  of reading the body.
- SKILL.md stays short and tabular. Heavy material goes in `references/`, linked from a table that
  says when to open each file.
- Claims about a tool or format are checked against the live tool or its source, not memory.
  A guessed style key or icon name fails silently.

## Growing a skill

Skills here are meant to be added to as they are used. When a run hits something new:

- a tool surprise → a row in the skill's Common mistakes;
- a kind of diagram, service or format → a file in the matching `references/` folder, copied from
  its `_template.md`;
- a doc that answered the question → a line in the skill's docs map.

One or two lines each. Bump `version` in the plugin's `plugin.json` when a change should reach
installed copies.

## Public repo rules

- No hostnames, realm names or other details from the homelab. Examples use `example.com`.
- No personal names, emails or handles. The maintainer is Dr K; the owner is `kubed-io`.
- Paraphrase other projects' docs; don't paste them. jgraph's draw.io repos are Apache-2.0.

## Testing

Each skill's `evals/` cases run with `claude plugin eval .` from the skill folder. Live-editor cases
need a draw.io editor connected through the MCP, with the page the case names.
