---
name: orient
description: Decompose observations into a sequenced, executable plan.
---

## Trigger

`/oodaloop-orient` or transitioning from Observe phase.

## Preconditions

- `.oodaloop/PROJECT.md` must have populated Requirements and Observations sections.
- `.oodaloop/STATE.md` phase should be `orient` (set by observe skill).
- If PROJECT.md lacks requirements, recommend returning to `/oodaloop-observe`.

## Workflow

### 1. Read observations
Read `.oodaloop/PROJECT.md`. Identify:
- All requirements (R1, R2, ...)
- Constraints
- Scope boundaries (in/out/deferred)
- Risks and open questions from observations

### 2. Identify work streams
Group related requirements into logical streams. Look for:
- Natural clusters (e.g., "data layer tasks" vs "UI tasks")
- Shared dependencies between requirements
- Independent streams that can be parallelized

### 3. Decompose into atomic tasks
For each work stream, break down into tasks where each task:
- Has a single concern (one thing changes)
- Can be verified independently
- Has clear acceptance criteria
- Takes no more than one focused session to complete

### 4. Define dependencies and parallelism
For each task, identify:
- Which tasks must complete before it can start
- Which tasks can run in parallel
- Draw or describe the dependency graph

### 5. Write PLAN.md
Create `.oodaloop/PLAN.md` using this format:

```markdown
# Plan: <milestone or feature name>

## Tasks

### T1: <task title>
**Depends on**: <task IDs or "none">
**Acceptance**: <concrete, verifiable criteria>

### T2: <task title>
**Depends on**: T1
**Acceptance**: <criteria>

...

## Dependency Graph
<ASCII diagram or description showing task ordering>

## Execution Strategy
Batch 1: <tasks that can run in parallel>
Batch 2: <next tasks after batch 1 completes>
...
```

### 6. Review the plan
Before finalizing, check:
- Every requirement from PROJECT.md is covered by at least one task
- No task has ambiguous acceptance criteria
- Dependencies form a valid DAG (no cycles)
- The plan is executable without reinterpretation

If gaps exist, add tasks or flag them.

### 7. Update state
Set `.oodaloop/STATE.md` phase to `decide`. Update Task Progress with task count and batch count.

## Output

- `.oodaloop/PLAN.md` with atomic tasks, dependencies, acceptance criteria, and execution strategy
- `.oodaloop/STATE.md` phase advanced to `decide`
- Summary reported to user with recommendation to proceed to `/oodaloop-decide`
