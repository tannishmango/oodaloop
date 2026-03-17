---
name: oodaloop-decide
description: Execute the current plan by implementing atomic tasks.
---

## Workflow

Reads PLAN.md. Dispatches executor agent for implementation. Processes tasks in dependency order. Emits execution summaries with evidence. Updates STATE.md.

## Inputs

- `.oodaloop/PLAN.md`
- `.oodaloop/STATE.md`

## Outputs

- Execution summaries with evidence per task
- STATE.md phase → Act
- Optional: SUMMARY.md for recent execution

## Escalation

- If a task blocks or fails, halt and report; user decides next step.

## Reference

See `decide` skill for detailed procedure.
