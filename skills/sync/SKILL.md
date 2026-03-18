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

### 2. Refresh persistent context (targeted)

Run the same sentinel-file drift check used by `observe` step 2:

- only re-scan convention categories that drifted
- if any category changed, update `.oodaloop/CONTEXT.md`
- bump `Last refreshed` timestamp if anything changed

If no drift is detected, do not modify convention sections.

### 3. Reconcile task integrity

For each task file, run state-hygiene checks and classify issues as:

- **blocking**: missing required section for current phase, orphaned parent/child links, or cyclic parent chain
- **non-blocking**: stale timestamps, minor metadata mismatch

When repair is unambiguous, repair in place:

- If phase metadata is ahead of available sections, set phase back to the last fully evidenced phase.
- If task is `paused` but has no `Paused` section, set phase back to `decide`.
- If parent has `Paused` section waiting on a child task that no longer exists, remove `Paused` and set parent phase to `decide`.

When repair is ambiguous or high-risk, do not mutate; report and recommend the next command.

Update task `Updated:` timestamp only for files actually modified.

### 4. Check completion and next-step readiness

For each task, determine status:

- **done**: explicit `CONTINUE` verdict exists
- **ready-for-loop**: verification is present and phase is `act` or `loop`
- **ready-for-act**: implementation appears complete and phase is `decide`
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
- integrity issues found (blocking/non-blocking)
- task status table (done/ready/blocked/active)
- exact next commands (for example `/oodaloop-act`, `/oodaloop-loop`, `/oodaloop-decide`)

## Output

- `.oodaloop/CONTEXT.md` refreshed if convention drift was detected
- any unambiguous task-state repairs applied
- completion/readiness status for active task files
- explicit next-step command recommendations
