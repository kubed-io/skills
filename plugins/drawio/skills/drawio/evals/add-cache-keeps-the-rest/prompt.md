---
tags: [drawio]
max_turns: 40
timeout_seconds: 900
---

In the draw.io diagram I have open, on the page named `cache-test`, add a Redis cache between the API and Postgres: the API should talk to Redis, and Redis should fall through to Postgres on a cache miss. Keep everything else as it is.
