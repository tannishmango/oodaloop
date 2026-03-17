---
name: oodaloop-loop
description: Reassess scope validity based on execution evidence.
---

## Workflow

Reads STATE.md, recent SUMMARY.md, VERIFICATION.md. Dispatches sentinel agent. Outputs exactly one verdict: CONTINUE, REFINE, or RESCOPE.

## Verdicts

- **CONTINUE** — scope valid; proceed to next phase or task
- **REFINE** — adjust upcoming tasks; update PLAN.md
- **RESCOPE** — core assumptions broken; return to Observe

Each verdict includes: evidence, rationale, confidence, required state updates, next recommended command.

## Inputs

- `.oodaloop/STATE.md`
- `.oodaloop/SUMMARY.md` (recent)
- `.oodaloop/VERIFICATION.md`

## Outputs

- Verdict with structured fields
- State updates per verdict type

## Reference

See `loop` skill for detailed procedure.
