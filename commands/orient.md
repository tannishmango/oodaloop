---
name: oodaloop-orient
description: Decompose observations into an executable plan with sequenced tasks.
---

## Workflow

Reads observations from Observe phase. Dispatches planner agent for task decomposition. Creates PLAN.md with atomic tasks, dependencies, and acceptance criteria. Updates STATE.md with phase.

## Inputs

- `.oodaloop/PROJECT.md` (observations)
- `.oodaloop/STATE.md`

## Outputs

- `.oodaloop/PLAN.md` — atomic tasks, dependencies, acceptance criteria
- STATE.md phase → Decide

## Escalation

- If observations are incomplete, return to Observe.

## Reference

See `orient` skill for detailed procedure.
