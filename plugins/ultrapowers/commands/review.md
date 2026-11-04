---
description: Review this pull request, the whole branch against its base, as superpowers' code reviewer, with a security review by a subagent.
---
Review this pull request: the whole branch against its base (`main`, or the family branch `issue-<N>` for a sub-issue's change), as `skill://superpowers/requesting-code-review/SKILL.md`'s code reviewer does, against the plan it was built from and the linked issue's notes. A fix with no plan is reviewed against the bug report in those notes.

Before you review, dispatch a subagent to security-review the diff in `.issue/diff.md`: injection, authentication and authorisation, secrets, unsafe deserialisation, data exposure. High-confidence findings only, each with its file, line, severity and fix; nothing in docs, and no denial of service or rate limiting. Weigh what it finds in your review: a real finding is a line comment, and one that must be fixed means changes requested.
