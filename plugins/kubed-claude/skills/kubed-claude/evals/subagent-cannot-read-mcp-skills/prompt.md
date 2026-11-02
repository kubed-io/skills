---
tags: [kubed-claude]
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Our MCP server serves skills as resources: skill://superpowers/brainstorming/SKILL.md and so on, with an index at skill://superpowers/_index.md. The main Claude Code session reads them fine. But when it delegates to a subagent, the subagent says it has no way to read skill:// URIs. Why does that happen, and what's the cleanest fix that still keeps this server's tools out of the main session? Answer only, don't change any files.
