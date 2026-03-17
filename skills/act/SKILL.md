---
name: act
description: Verify execution outcomes against acceptance criteria.
---

## Trigger

`/oodaloop-act` or transitioning from Decide.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with Plan and Execution Log sections.
- Task file phase should be `act`.

## Workflow

### 1. Read plan and execution log
From the task file, extract each task's acceptance criteria (from Plan) and execution evidence (from Execution Log).

Read `.oodaloop/CONTEXT.md` conventions -- verify that implementation respected repo conventions (correct test patterns, linter compliance, commit format, etc.).

### 2. Verify each task
For each task, check:
- Does the execution evidence satisfy the acceptance criteria?
- Were repo conventions followed?
- Are there side effects or regressions?

Run relevant checks: tests, linters, type checks, build commands. Use what CONTEXT.md says the repo uses.

### 3. Record verification in task file
Append to the task file:

```markdown
## Verification

### T1: <title>
**Result**: pass | fail | partial
**Evidence**: <test output, check results, manual inspection>
**Gaps**: <what's missing, if any>

### T2: ...

### Summary
- **Passed**: <count>
- **Failed**: <count>
- **Convention compliance**: <yes/no, details>
```

### 4. Report gaps
If any task failed or has gaps, report with concrete next steps: what needs fixing, which tasks need re-execution.

### 5. Update task file phase
Set phase to `loop`. Update timestamp.

## Output

- Verification section appended to task file with per-task results
- Task file phase advanced to `loop`
- Gap analysis reported with next-step recommendation: `/oodaloop-loop` to assess, or fix and re-verify
