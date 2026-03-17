---
name: loop
description: Sentinel reassessment of scope validity based on execution evidence.
---

## Trigger

`/oodaloop-loop` or after Act phase completion.

## Workflow

1. Read `STATE.md`, recent `SUMMARY.md`, `VERIFICATION.md`, and `PROJECT.md` scope.
2. Dispatch sentinel agent (readonly).
3. Assess: are original assumptions still valid? Has scope drifted? New risks?
4. Emit exactly one verdict: **CONTINUE** (proceed), **REFINE** (adjust tasks/priorities), or **RESCOPE** (re-enter Observe).
5. Each verdict must include: evidence, decision rationale, confidence level, required state updates, next recommended command.
6. Update `STATE.md`.

## Output

Loop verdict with evidence and next-step recommendation. Updated `STATE.md`.
