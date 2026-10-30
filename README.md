# skills

**Agent skills for the tools we actually use, packaged as a Claude Code plugin marketplace.** Each
plugin is one tool's worth of know-how: the traps, the cheap way to do things, and where the docs live.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

```
/plugin marketplace add kubed-io/skills
/plugin install drawio@kubed
```

Or skip installing: anything that reads skills over MCP, or straight from a git repo, can load the
same folders.

---

## 🎨 drawio

Draw and edit [draw.io](https://www.drawio.com) diagrams. With
[lgazo/drawio-mcp-server](https://github.com/lgazo/drawio-mcp-server) connected, the agent works in
the diagram you have open: one new box, one re-pointed arrow, while you watch. No editor? It writes a
`.drawio` file instead.

- **Small edits, small bills.** It reads only the cells it needs, checks its work as XML instead of
  images, and skips the editor's traps (an import that wipes the page, an export path on someone
  else's disk). In testing, adding a cache to a diagram took less than half the time and a third of
  the tool traffic.
- **Prompts for the everyday asks.** `/drawio:draw`, `edit`, `tidy`, `explain` — and `note`, which
  files what a session learned back into the skill.
- **Real icons, not guesses.** Kubernetes, AWS, GCP and Azure styles that render, instead of
  confidently named empty boxes.
- **A map of the docs.** Every style key, shape index, file format and API — with the cheap way to
  fetch each one.
- **Grows as you use it.** One reference file per kind of diagram. Learn something, add a line.

[`plugins/drawio`](plugins/drawio/skills/drawio/SKILL.md)

---

## ⚡ ultrapowers

The turns of an issue-to-pull-request agent flow, as prompts on top of
[superpowers](https://github.com/obra/superpowers). Each one starts a turn from an event with no words
of its own: a label, a push, a review, red checks.

- **From issue to plan.** `spec-draft` drafts the spec by brainstorming; `spec-approved` writes the
  plan of record by writing-plans.
- **A task at a time.** `plan-approved` and `next-task` build the plan by subagent-driven
  development, one task per turn.
- **Answers, not excuses.** `checks-failed` debugs red checks; `review-came-in` answers every open
  review thread by receiving-code-review.
- **A review with a security pass.** `review` reviews the whole branch, after a subagent
  security-reviews the diff.

[`plugins/ultrapowers`](plugins/ultrapowers/commands)

---

## Adding a plugin

One folder under `plugins/`, one entry in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).
[AGENTS.md](AGENTS.md) has the conventions.
