---
name: decide
description: Execute plan tasks through the executor agent.
---

## Trigger

`/oodaloop-decide` or transitioning from Orient.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with a Plan section.
- `.oodaloop/CONTEXT.md` must exist.
- Task file phase should be `decide`.

## Workflow

### 1. Read plan and context
Read the active task file's Plan section. Read `.oodaloop/CONTEXT.md` conventions -- these are binding constraints on implementation (commit format, linter rules, test patterns, etc.).

### 2. Process tasks in dependency order
For each batch in the execution strategy:
- Dispatch executor agent for each task in the batch.
- The executor follows the task specification and respects CONTEXT.md conventions.
- After each task: record what changed, what was tested, any side effects.

### 3. Handle mid-execution discoveries
During execution, the executor may discover issues, improvement opportunities, or prerequisite work not in the plan. For each discovery, assess:
- **Trivial** (one-line fix, no risk): handle inline, note in execution log.
- **Notable but non-blocking** (would improve things but isn't required now): add to `.oodaloop/BACKLOG.md` Next or Later section with a brief description and date. Continue execution.
- **Blocking** (can't proceed without fixing this): stop the current task, note the blocker in the execution log, and recommend the user either resolve it inline or spawn a new OODA cycle for it.

### 4. Update execution log in task file
After each batch, append to the task file:

```markdown
## Execution Log

### T1: <title>
**Status**: done | blocked | escalated
**Changes**: <files modified, created, deleted>
**Evidence**: <tests run, commands executed, output>
**Notes**: <side effects, discoveries, blockers>
**Backlog additions**: <items added to BACKLOG.md, if any>

### T2: ...
```

### 5. Pause after each batch
Report batch results to the user. If any task is blocked or reveals unexpected complexity, stop and recommend either resolving the blocker or running `/oodaloop-loop` to reassess.

### 6. Update task file phase
After all batches complete, set task file phase to `act`. Update timestamp.

## Output

- Execution log appended to task file with evidence per task
- Task file phase advanced to `act`
- Summary reported with recommendation to proceed to `/oodaloop-act`
