---
name: start
description: Decide whether OODALOOP is warranted, then enter only when the extra orientation will pay for itself.
---

# start

## Trigger

`/oodaloop-start`, or an explicit request to assess whether work should enter OODALOOP.

Do not use this command as the automatic beginning of every software task.

## Workflow

### 1. Route before touching OODALOOP state

Make a cheap preflight from the user's objective and immediately available context. Do **not** initialize `.oodaloop/`, run sync, create a task file, dispatch an agent, or write any artifact yet.

Ask internally:

1. **Executable now?** Can the task be safely executed and verified without making consequential decisions that the current instructions/context have not resolved?
2. **Ordinary planning enough?** If not, can lightweight local planning resolve the remaining decisions without substantial discovery, decomposition, coordination, or risk?

If either answer is yes, choose **NORMAL**.

Choose **OODALOOP** only when meaningful residual consequential uncertainty remains. Relevant signals include unfamiliar territory, architectural/cross-system coupling, assumptions that could invalidate the approach, unclear interfaces or acceptance semantics, difficult proof, high blast radius, or decomposition needed to prevent implementers from inventing consequential intent.

Do not route by file count or task count alone. Do not default to OODALOOP merely because you are uncertain about the classification.

### 2. NORMAL route

If OODALOOP is not warranted:

- state that ordinary agent planning/execution is the cheaper path;
- do not initialize or read OODALOOP state unless the user separately asked for status/history;
- do not recommend `/oodaloop-quick` as a substitute framework path;
- continue with the host agent's normal workflow if the surrounding environment permits it.

Output should be concise. The purpose of the router is to keep the framework out of the way.

### 3. OODALOOP route: reconcile only now

Only after choosing OODALOOP:

1. Read `.oodaloop/CONTEXT.md` directly.
2. If it does not exist, recommend `/oodaloop-init`; initialize only with user approval when the host requires approval.
3. If state exists, run `/oodaloop-sync` before resuming or starting a cycle.
4. Read active `*.task.md` files only as needed to determine whether this objective is resuming existing work.

Do not read BACKLOG merely because the framework started; read it only when selecting/deconflicting future work is relevant.

### 4. Capture only the objective needed for Observe

If the user already supplied a concrete objective, do not interview them again.

If the objective is genuinely missing, ask only for the missing fact required to begin discovery. Avoid mandatory kickoff questionnaires.

Pass into Observe:
- objective,
- explicit constraints already supplied,
- why OODALOOP was warranted (the unresolved uncertainty/risk that ordinary planning could not cheaply eliminate),
- parent/resume context if applicable.

### 5. Enter Observe or resume

- New qualifying work → `/oodaloop-observe`.
- Existing task → resume at the phase indicated by reconciled state.

## Output

Exactly one routing result:

- **NORMAL** — OODALOOP not warranted; no framework state/artifacts created.
- **OODALOOP** — brief reason the additional orientation is justified, followed by initialization/sync/resume as needed.

The routing decision itself must remain cheaper than the process it is deciding whether to invoke.
