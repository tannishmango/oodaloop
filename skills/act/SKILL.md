---
name: act
description: Verify execution outcomes against acceptance criteria.
---

## Trigger

`/oodaloop-act` or transitioning from Decide.

## Workflow

1. Read `PLAN.md` acceptance criteria and `SUMMARY.md` execution results.
2. Dispatch verifier agent (readonly).
3. For each task: check acceptance criteria, run relevant tests/checks, collect evidence.
4. Create `.oodaloop/VERIFICATION.md` with pass/fail per criterion and evidence links.
5. Report gaps with concrete next steps.
6. Update `STATE.md`.

## Output

`VERIFICATION.md` with per-criterion results, gap analysis, and recommended actions.
