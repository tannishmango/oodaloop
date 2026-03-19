---
name: sync
description: Reconcile and refresh OODALOOP state after interruptions or context resets.
---

# sync

## Trigger

`/oodaloop-sync` or when resuming after unrelated work, model refresh, or long context gaps.

## Preconditions

- `.oodaloop/` must exist. If not, report "No OODALOOP state found. Run `/oodaloop-start` first." and stop.
- `.oodaloop/CONTEXT.md` must exist.

## Workflow

### 1. Read current state

Read:

- `.oodaloop/CONTEXT.md`
- `.oodaloop/BACKLOG.md` (if present)
- all `.oodaloop/*.task.md` files

Build parent/child relationships from `Parent:` references.

### 2. Check persistent context staleness

Compare `.oodaloop/CONTEXT.md` "Last refreshed" timestamp against the current date.

- If stale (>24h or different day): report "CONTEXT.md may be outdated — conventions and proof infrastructure may have changed." Recommend running `/oodaloop-observe` before continuing execution.
- If current: no action needed.

Do not scan conventions. Do not audit proof infrastructure. Do not dispatch the researcher agent. These belong to observe during active cycles and init during bootstrap.

### 3. Reconcile task integrity

For each task file, run state-hygiene checks and classify issues as:

- **blocking**: missing required section for current phase, orphaned parent/child links, or cyclic parent chain
- **non-blocking**: stale timestamps, minor metadata mismatch

When repair is unambiguous, repair in place:

- If phase metadata is ahead of available sections, set phase back to the last fully evidenced phase.
- If task is `paused` but has no `Paused` section, set phase back to `act`.
- If parent has `Paused` section waiting on a child task that no longer exists, remove `Paused` and set parent phase to `act`.
- If task has a `## Ready to Resume` section, a child cycle completed and this task is ready to continue. Report the child result and recommend `/oodaloop-act` to resume execution. Remove the `Ready to Resume` section after reporting (it's a one-time signal).

When repair is ambiguous or high-risk, do not mutate; report and recommend the next command.

Update task `Updated:` timestamp only for files actually modified.

### 4. Check completion and next-step readiness

For each task, determine status:

- **done**: explicit `CONTINUE` verdict exists
- **resumable**: has `## Ready to Resume` section (child cycle completed, parent ready to continue)
- **ready-for-loop**: Execution Log is present and phase is `loop`
- **ready-for-act**: Plan is present and phase is `act`
- **blocked**: paused or waiting on dependency
- **active**: otherwise

Do not delete task files in sync. Deletion remains owned by `/oodaloop-loop` after verdict handling.

### 5. Reconcile backlog signals

If `.oodaloop/BACKLOG.md` exists:

- note if top Next item appears already done in task evidence
- note if tasks produced notable deferred work not represented in backlog

Recommend promotion/completion moves, but do not rewrite backlog unless the mapping is explicit and unambiguous.

### 6. Report compressed state

Return a concise sync report:

- what changed (if any)
- staleness warning (if CONTEXT.md is outdated)
- integrity issues found (blocking/non-blocking)
- task status table (done/ready/blocked/active)
- exact next commands (for example `/oodaloop-act`, `/oodaloop-loop`, `/oodaloop-decide`)

## Output

- staleness warning if CONTEXT.md is outdated
- any unambiguous task-state repairs applied
- completion/readiness status for active task files
- explicit next-step command recommendations
