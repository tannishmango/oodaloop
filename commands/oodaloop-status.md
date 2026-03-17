---
name: oodaloop-status
description: Report current OODALOOP project state and active tasks.
---

Read-only. No side effects.

1. Check if `.oodaloop/` exists. If not, report "No OODALOOP state found. Run `/oodaloop-init` first." and stop.

2. Read `.oodaloop/CONTEXT.md`. Report:
   - **Project**: name from header
   - **Objective**: current objective
   - **Last refreshed**: timestamp
   - **Conventions**: one-line summary per category (detected/not detected)
   - **Active decisions**: count and most recent entry
   - **Deconfliction**: summary line

3. List all `.oodaloop/*.task.md` files. For each active task, report:
   - **Task**: slug (from filename)
   - **Phase**: current phase
   - **Last updated**: timestamp
   - **Progress**: task completion counts if Plan section exists

4. If no active tasks exist, report "No active tasks."

5. If `.oodaloop/BACKLOG.md` exists, report:
   - **Backlog**: count of Next items, count of Later items
   - **Top Next item**: first item from the Next section

6. Report blockers if any are mentioned in task files.

Format as a concise structured summary. Do not modify any files.
