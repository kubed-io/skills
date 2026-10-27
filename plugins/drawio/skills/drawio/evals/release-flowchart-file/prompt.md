---
tags: [drawio]
max_turns: 40
timeout_seconds: 900
---

Write a draw.io flowchart of our release process to release-flow.drawio: PR merged → CI build → tests pass? If no, notify the author. If yes, deploy to staging → smoke test OK? If no, roll back; if yes, deploy to production.
