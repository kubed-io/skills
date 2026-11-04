---
description: The bug report is approved and the fix has no plan. Read the code agent's skills, then build the report's fix test-first, in one run.
---
The bug report is approved, and the fix has no plan: the report in the linked issue's notes (`.issue/issues.md`) is the whole task. First read these skills:

- `skill://superpowers/test-driven-development/SKILL.md`
- `skill://superpowers/receiving-code-review/SKILL.md`
- `skill://superpowers/verification-before-completion/SKILL.md`

Then build the fix. Check the report's cause against the code as it is now. Write a test that fails for the reason the report gives, then the smallest change that makes it pass. Run the checks the report names, and this repository's. When the fix is in, review the whole branch as subagent-driven development's final review does, and say `done`.

If the cause turns out not to be what the report says, or the fix is bigger than it looked, stop: hand over what is safe, and say in your reply what you found and that it needs a plan.
