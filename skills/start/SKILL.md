---
name: start
description: Kick off a new OODALOOP flow with guided intake and next-step routing.
---

# start

## Trigger

`/oodaloop-start` when starting work, especially at the beginning of a new conversation or project task.

## Workflow

### 1. Ensure state exists

Read `.oodaloop/CONTEXT.md` directly. Do not glob for `.oodaloop/**` (glob skips hidden directories).

- If the Read tool returns an error (file not found): explain that OODALOOP state is not initialized and recommend running `/oodaloop-init` now.
  - If the user agrees, run `/oodaloop-init` first, then continue this start flow.
  - If the user does not agree, stop with a concise note: "Cannot start OODALOOP flow without initialization."
- If it returns content: `.oodaloop/` exists. Continue.

### 2. Reconcile existing state (sync-first)

If `.oodaloop/` exists, invoke `/oodaloop-sync` before any kickoff intake or routing.

Rationale: start should begin from reconciled state so task integrity, convention drift, and readiness are current before deciding whether to resume or start new.

If sync reports blocking integrity issues, stop and present the recommended recovery path before continuing.

### 3. Read active state

Read:

- `.oodaloop/CONTEXT.md`
- `.oodaloop/BACKLOG.md` if present
- existing `.oodaloop/*.task.md` files (if any)

Determine whether there is already active work (open task files). If active tasks exist, ask whether the user wants to resume one of them or start a new task.

### 4. Guided intake (required when context is missing)

If the user did not provide a concrete objective, run a short kickoff interview. Keep it brief and actionable:

1. What do you want to achieve in this session? (feature, bug fix, refactor, docs, or exploration)
2. What area of the repo is involved?
3. What constraints matter most? (deadline, risk tolerance, compatibility, test expectations)

If the user is unsure, offer concise prompts:

- "Name one user-visible outcome you want by the end of this session."
- "Name one pain point to remove."
- "Name one question you want answered before coding."

Convert the intake into:

- objective statement (1-2 sentences)
- initial requirement list
- scope hints (in/out, known unknowns)

### 5. Route to the right flow

Use adaptive rigor:

- **Trivial, low-risk, local change** -> recommend `/oodaloop-quick`.
- **Anything non-trivial or unclear** -> recommend `/oodaloop-observe`.

Default to `/oodaloop-observe` when uncertain.

### 6. Handoff cleanly

If user agrees, invoke the recommended command immediately and continue in that flow.

When handing off to `/oodaloop-observe`, pass the distilled objective and requirements from step 4 so observe starts with concrete context instead of re-asking broad questions.

When handing off to `/oodaloop-quick`, ensure the task is truly low-risk; otherwise escalate to observe.

### 7. Report kickoff state

Provide a concise kickoff summary:

- initialization status
- sync status (ran + key result)
- whether resuming or starting new
- objective captured
- selected next command and rationale

## Output

- Clear "start here" entrypoint behavior for OODALOOP
- Sync-aware kickoff that reconciles state before routing
- Guided intake when user context is missing
- Deterministic routing to `/oodaloop-quick` or `/oodaloop-observe`
- Immediate handoff into execution flow when user confirms
