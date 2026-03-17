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

### 2. Verify each task independently
The verifier must produce its own evidence. Do not accept the executor's self-reported proof as verification -- reproduce it.

For each task:
- **Re-run checks independently.** If the executor claims "tests pass," run the tests yourself and show the output. If the executor claims "file changed correctly," read the file yourself and confirm. The executor's proof is a claim until the verifier reproduces it.
- Does the reproduced evidence satisfy the acceptance criteria?
- Were repo conventions followed?
- Are there side effects or regressions?
- **Were the right kind of tests run?** If the task touches integrations, APIs, or external systems, unit tests alone are not sufficient evidence. Check whether integration tests were written and run. If only unit tests exist for an integration claim, flag this as a verification gap -- do not mark as pass.
- **Surface verification evidence to the user.** Show the verification output in conversation. The user judges sufficiency.

Run checks based on what CONTEXT.md says the repo uses:
- **If repo has tests**: run the full test suite, report pass/fail counts with raw output. Check that tests match the risk profile of the changes (unit for logic, integration for external systems).
- **If repo has linters/formatters**: run them, show the output.
- **If repo has CI**: check that local changes wouldn't break CI checks.
- **If repo has no automated checks** (CONTEXT.md says "None detected" for testing/code quality): verify through structured file inspection -- read the changed files, trace the logic, confirm against acceptance criteria with specific line references. Check for regressions (broken imports, syntax errors, missing references). Note "verified by inspection" with the specific files and lines checked.

### 3. Record verification in task file
Append to the task file:

```markdown
## Verification

### T1: <title>
**Result**: pass | fail | partial
**Proof**: <raw output from independently-run checks -- not copied from execution log>
**Gaps**: <what couldn't be independently verified, and why>

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
