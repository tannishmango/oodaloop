---
name: oodaloop-status
description: Report current OODALOOP project state and active tasks.
---

Read-only. No side effects.

For resumed sessions after interruptions, model refreshes, or unrelated work, run `/oodaloop-sync` first to reconcile state before reading status.

1. Check if `.oodaloop/` exists. If not, report "No OODALOOP state found. Run `/oodaloop-start` first." and stop.

2. Read `.oodaloop/CONTEXT.md`. Report:
   - **Project**: name from header
   - **Objective**: current objective
   - **Last refreshed**: timestamp
   - **Conventions**: one-line summary per category (detected/not detected)
   - **Active decisions**: count and most recent entry
   - **Deconfliction**: summary line

3. List all `.oodaloop/*.task.md` files. Build parent-child chains by following `Parent:` references. Display as a tree:
   - Root tasks (no `Parent:` field) are top-level entries
   - Child tasks are indented under their parent
   - For each task, report: slug, phase, last updated, progress (task completion counts if Plan section exists)
   - Show chain depth if > 1 (e.g., "depth: 2")

   Example:
   ```
   fix-auth (decide, updated 2026-03-17, 2/4 tasks done)
     └─ fix-token-refresh (act, updated 2026-03-17, depth: 2)
   add-logging (observe, updated 2026-03-17)
   ```

4. If no active tasks exist, report "No active tasks."

5. If `.oodaloop/BACKLOG.md` exists, report:
   - **Backlog**: count of Next items, count of Later items
   - **Top Next item**: first item from the Next section

6. Report blockers if any are mentioned in task files.

Format as a concise structured summary. Do not modify any files.
