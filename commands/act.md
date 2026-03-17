---
name: oodaloop-act
description: Verify execution outcomes against acceptance criteria.
---

## Workflow

Reads execution summaries. Dispatches verifier agent for acceptance checks. Reports pass/fail with evidence and gap analysis. Updates STATE.md. Creates VERIFICATION.md.

## Inputs

- Execution summaries from Decide phase
- `.oodaloop/PLAN.md` (acceptance criteria)
- `.oodaloop/STATE.md`

## Outputs

- `.oodaloop/VERIFICATION.md` — pass/fail, evidence, gaps
- STATE.md phase → Loop

## Escalation

- Failures trigger gap analysis; user may re-run Decide for fixes or Loop for rescoping.

## Reference

See `act` skill for detailed procedure.
