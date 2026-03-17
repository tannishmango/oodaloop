---
name: oodaloop-quick
description: Fast path for trivial tasks — minimal ceremony, clear summary.
---

## Workflow

For low-risk, local changes that don't warrant full OODA ceremony. Executes directly, emits a concise summary with what changed and verification result. Updates STATE.md minimally. Escalates to full loop if complexity discovered mid-execution.

## Inputs

- Task description (user-provided)
- Optional: `.oodaloop/` state (if initialized)

## Outputs

- Concise summary: what changed, verification result
- Minimal STATE.md update (if state exists)

## Escalation

- If complexity discovered mid-execution, halt and recommend full Observe → Orient → Decide → Act flow.

## Reference

See `quick` skill for detailed procedure.
