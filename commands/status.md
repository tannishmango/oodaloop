---
name: oodaloop-status
description: Report current OODALOOP project state and phase.
---

Read-only. No side effects.

1. Check if `.oodaloop/` exists. If not, report "No OODALOOP state found. Run `/oodaloop-init` first." and stop.

2. Read `.oodaloop/STATE.md`. Extract and report:
   - **Phase**: current phase and last updated date
   - **Milestone**: if present
   - **Task progress**: summary line from Task Progress section

3. If `.oodaloop/PLAN.md` exists, count tasks and report:
   - Total tasks
   - Completed / in-progress / pending (if the plan uses status markers)

4. If `.oodaloop/VERIFICATION.md` exists, summarize:
   - Pass/fail counts
   - Any open gaps

5. Report the most recent entry from Decisions Log and Loop Verdicts (if any).

6. Report blockers if any are mentioned in state files.

Format the output as a concise structured summary. Do not modify any files.
