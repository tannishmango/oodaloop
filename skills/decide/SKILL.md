---
name: decide
description: Execute plan tasks through the executor agent.
---

## Trigger

`/oodaloop-decide` or transitioning from Orient.

## Workflow

1. Read `PLAN.md`.
2. Process tasks in dependency order.
3. For each task: dispatch executor agent, implement the change, emit execution summary with evidence (what changed, what was tested).
4. Track progress in `STATE.md`.
5. Create `.oodaloop/SUMMARY.md` with cumulative results.
6. Pause and report after each batch for review.

## Output

Implementation complete, `SUMMARY.md` with evidence per task, updated `STATE.md`.
