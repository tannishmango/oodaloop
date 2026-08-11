---
name: sync
description: Reconcile minimal OODALOOP state after interruption without re-running the framework.
---

# sync

## Trigger

`/oodaloop-sync` when resuming OODALOOP work after context loss, interruption, or a different conversation.

Do not run sync for ordinary work that never entered OODALOOP.

## Preconditions

- `.oodaloop/CONTEXT.md` exists. If not, report that no initialized OODALOOP state exists and stop.

## Workflow

### 1. Read only active state

Read:
- `.oodaloop/CONTEXT.md`,
- active `.oodaloop/*.task.md` files,
- BACKLOG only when future-work reconciliation is actually relevant.

Build parent/child relationships from `Parent:` and `## Waiting` references.

### 2. Repair factual integrity

Use the state-hygiene rule to check only restartability facts:
- phase has its minimum evidence,
- parent/child references resolve,
- no parent cycle exists,
- Waiting points to a real child/result,
- resume point is understandable.

Repair automatically only when the correct state is unambiguous. Do not launch agents or framework phases merely to fix metadata.

### 3. Determine the next consequential judgment

For each active node, identify the lightest valid resume point:
- missing/contradictory evidence → Observe,
- evidence exists but interpretation changed → Orient,
- leaf/task tree needs revision → Decide,
- plan remains valid and a leaf is ready → Act,
- implementation is complete and only boundary reconciliation remains → Loop,
- waiting on child → report the child and stop that branch.

Do not restart from Observe by default just because time passed or CONTEXT is older than 24 hours. Check staleness only where current work depends on facts likely to have changed.

### 4. Resume completed children

When a child completed:
- read its result/evidence,
- determine whether that evidence changes parent assumptions or only resolves the blocked leaf,
- remove the parent's Waiting section when safe,
- resume at the phase justified by the returned evidence.

Do not replay the child's full phase history into parent context.

### 5. Report compressed state

Return:
- active root/child nodes,
- any factual repairs,
- what each node is waiting on,
- exact lightest next phase/command and why.

Do not emit framework diagnostics that do not change the next action.

## Output

A minimal cold-start reconstruction of where the work actually is—not a re-audit of the entire OODALOOP process.
