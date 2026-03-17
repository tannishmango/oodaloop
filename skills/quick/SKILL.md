---
name: quick
description: Fast path for trivial tasks -- skip ceremony, preserve safety minimums.
---

## Trigger

`/oodaloop-quick` or when task is assessed as low-risk and local.

## Preconditions

- `.oodaloop/CONTEXT.md` must exist. If not, prompt for `/oodaloop-init`.

## Workflow

1. Assess task complexity. If non-trivial (touches multiple files, has unclear scope, or high risk), escalate to `/oodaloop-observe`.

2. Read `.oodaloop/CONTEXT.md` conventions. These are binding even for quick tasks.

3. Execute directly. Follow repo conventions (commit format, test patterns, linter rules).

4. Create an ephemeral task file `.oodaloop/quick-<brief-slug>.task.md` with a compressed record:

```markdown
# Task: quick-<slug>

## Phase: complete
Started: <date>
Updated: <date>

## Summary
<what changed, what was verified, any side effects>
```

5. Absorb if anything durable was learned: update CONTEXT.md decisions or conventions.

6. Delete the task file.

7. If complexity is discovered mid-execution, stop and escalate to `/oodaloop-observe`.

## Output

- Changes implemented following repo conventions
- Ephemeral task file created and deleted
- CONTEXT.md updated if learnings were produced
- Summary reported to user
