---
name: orient
description: Decompose observations into a sequenced, executable plan.
---

## Trigger

`/oodaloop-orient` or transitioning from Observe phase.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with populated Requirements and Observations.
- `.oodaloop/CONTEXT.md` must exist.
- If the task file lacks requirements, recommend returning to `/oodaloop-observe`.

## Workflow

### 1. Read task observations
Read the active task file. Identify all requirements, constraints, scope boundaries, risks, and open questions.

Read `.oodaloop/CONTEXT.md` for repo conventions that constrain implementation.

### 2. Identify work streams
Group related requirements into logical streams. Look for:
- Natural clusters (e.g., "data layer" vs "UI")
- Shared dependencies between requirements
- Independent streams that can be parallelized

### 3. Decompose into atomic tasks
For each stream, break into tasks where each task:
- Has a single concern (one thing changes)
- Can be verified independently
- Has clear acceptance criteria
- Takes no more than one focused session

### 4. Define dependencies and parallelism
For each task, identify:
- Which tasks must complete first
- Which can run in parallel
- The dependency graph

### 5. Write plan into task file
Append the plan section to the existing task file:

```markdown
## Plan

### T1: <title>
**Depends on**: none
**Acceptance**: <concrete, verifiable criteria>

### T2: <title>
**Depends on**: T1
**Acceptance**: <criteria>

...

### Dependency Graph
<ASCII diagram or description>

### Execution Strategy
Batch 1: <parallel tasks>
Batch 2: <next tasks>
...
```

### 6. Review
Check before finalizing:
- Every requirement covered by at least one task
- No ambiguous acceptance criteria
- Dependencies form a valid DAG (no cycles)
- Plan is executable without reinterpretation
- Convention constraints from CONTEXT.md are reflected in relevant tasks

### 7. Update task file phase
Set the task file phase to `decide`. Update the timestamp.

## Output

- Plan section appended to `.oodaloop/<slug>.task.md`
- Task file phase set to `decide`
- Summary reported with recommendation to proceed to `/oodaloop-decide`
