---
tags: [kubed-claude]
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm writing a subagent in .claude/agents/searcher.md. Its frontmatter has mcpServers with two inline http servers, docs and tickets, and each one exposes about 10 tools. I also set `tools: mcp__docs__search` because I want this agent to have exactly one tool and nothing else. Will it? If not, what should the frontmatter say instead? Just answer, don't create or run anything.
