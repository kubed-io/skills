---
tags: [kubed-claude]
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

In CI we run `claude -p --strict-mcp-config --mcp-config ci.json` and the prompt delegates to our `reviewer` subagent. ci.json defines one server, docs. The repo's .mcp.json has grafana and github, and the account has claude.ai connectors (GitHub, Context7). The reviewer agent file has `mcpServers:` with `- grafana` (just the name) and an inline http server called tickets. Which MCP servers can the reviewer actually use? Answer without running anything.
