---
name: oodaloop-observe
description: Research and gather requirements for the current task or project.
---

## Workflow

Reads existing state. Dispatches researcher agent for codebase exploration and requirements gathering. Updates PROJECT.md with findings. Transitions to Orient when requirements are sufficient.

## Inputs

- `.oodaloop/STATE.md`, `.oodaloop/PROJECT.md`
- Optional: task scope or focus area

## Outputs

- Updated `.oodaloop/PROJECT.md` with structured observations
- STATE.md phase → Orient

## Escalation

- If requirements remain insufficient after research, re-run or refine scope.

## Reference

See `observe` skill for detailed procedure.
