---
name: quick
description: Fast path for trivial tasks -- skip ceremony, preserve safety minimums.
---

## Trigger

`/oodaloop-quick` or when task is assessed as low-risk and local.

## Preconditions

- `.oodaloop/CONTEXT.md` must exist. **Verify by reading it** — if the Read tool returns an error, prompt for `/oodaloop-start`. Do not glob for `.oodaloop/**` (glob skips hidden directories).

## Workflow

1. Assess task complexity. If non-trivial (touches multiple files, has unclear scope, or high risk), escalate to `/oodaloop-observe`.

2. Read `.oodaloop/CONTEXT.md` conventions. These are binding even for quick tasks.

3. **Destructive operations check.** Even quick tasks must respect the `destructive-ops` rule. If the task involves mutating external state (databases, Docker, services, infrastructure), require explicit user confirmation before execution regardless of task simplicity. Quick does not mean unconfirmed.

4. Execute directly. Follow repo conventions (commit format, test patterns, linter rules).

5. Create an ephemeral task file `.oodaloop/quick-<brief-slug>.task.md` with a compressed record:

```markdown
# Task: quick-<slug>

## Phase: complete
Started: <date>
Updated: <date>

## Summary
<what changed, what was verified, any side effects>
```

6. Absorb if anything durable was learned: update CONTEXT.md decisions or conventions.

7. Delete the task file.

8. If complexity is discovered mid-execution, stop and escalate to `/oodaloop-observe`.

## Output

- Changes implemented following repo conventions
- Ephemeral task file created and deleted
- CONTEXT.md updated if learnings were produced
- Summary reported to user
