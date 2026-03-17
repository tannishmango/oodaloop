---
name: orient
description: Decompose observations into a sequenced, executable plan.
---

## Trigger

`/oodaloop-orient` or transitioning from Observe.

## Workflow

1. Read `PROJECT.md` observations.
2. Use planner agent (readonly) for task decomposition.
3. Break work into atomic tasks with dependencies and acceptance criteria.
4. Create `.oodaloop/phases/<phase>/PLAN.md`.
5. Sequence tasks respecting dependencies.
6. Identify parallelizable vs sequential work.
7. Update `STATE.md`.

## Output

`PLAN.md` with atomic tasks, dependencies, acceptance criteria, and execution order.
