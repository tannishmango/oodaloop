---
name: quick
description: Fast path for trivial tasks -- skip ceremony, preserve safety minimums.
---

## Trigger

`/oodaloop-quick` or when task is assessed as low-risk and local.

## Workflow

1. Assess task complexity. If non-trivial, escalate to full Observe.
2. Execute directly without separate plan/verify phases.
3. Emit concise summary: what changed, what was tested/verified, any side effects.
4. Update `STATE.md` minimally.
5. If complexity discovered mid-execution, stop and escalate to `/oodaloop-observe`.

## Output

Execution summary with minimal verification evidence. `STATE.md` log entry.
