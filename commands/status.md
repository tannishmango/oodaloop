---
name: oodaloop-status
description: Report current OODALOOP project state and phase.
---

## Workflow

Reads `.oodaloop/` state files. Outputs current phase, task progress, open decisions, recent verdicts, and blockers. No side effects — read-only.

## Inputs

- `.oodaloop/STATE.md`
- `.oodaloop/PLAN.md`, `.oodaloop/VERIFICATION.md`, `.oodaloop/SUMMARY.md` (if present)

## Outputs

- Current phase
- Task progress (completed, in-flight, blocked)
- Open decisions
- Recent verdicts
- Blockers (if any)

## Notes

Read-only command. No corresponding skill -- status reporting is self-contained.
