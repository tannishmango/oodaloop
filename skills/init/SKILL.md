---
name: init
description: Initialize OODALOOP state directory in a target project.
---

## Trigger

User runs `/oodaloop-init` or starting a new OODALOOP-tracked project.

## Workflow

1. Determine the project name from the workspace root directory name (e.g., `my-app`). If the user provides a name, use that instead.

2. Check if `.oodaloop/` already exists in the workspace root.
   - If it exists: warn the user and **stop**. Do not overwrite existing state.
   - If it does not exist: proceed.

3. **Scan for plugin conflicts.** Check which Cursor plugins are active in this workspace. For each, assess interference risk against OODALOOP using these criteria:
   - **High risk** (recommend disable): plugin injects mandatory context via hooks, enforces unconditional hard gates on all tasks, or overrides workflow autonomy. Example: `superpowers` -- its session hook injects "EXTREMELY_IMPORTANT" context and forces rigid skill-first behavior that conflicts with adaptive rigor.
   - **Medium risk** (recommend deprioritize): plugin runs background processes or follow-up loops that add noise during focused work. Example: `continual-learning` -- its stop hook triggers autonomous memory updates.
   - **Low risk** (keep): plugin provides scoped, opt-in capabilities that don't conflict. Examples: `create-plugin` (quality gates), `cursor-team-kit` (CI/review tools), domain-specific skills (database, etc.).

   Report findings to the user as a concise table:
   ```
   | Plugin | Risk | Recommendation | Reason |
   ```
   Let the user decide what to disable. Do not disable anything automatically.

4. Create the `.oodaloop/` directory.

5. Create `.oodaloop/STATE.md` with this content, substituting the project name, today's date, and deconfliction findings:

```markdown
# OODALOOP State: <project_name>

## Current Phase
- **Phase**: ready
- **Started**: <today's date YYYY-MM-DD>
- **Last Updated**: <today's date YYYY-MM-DD>

## Task Progress
No active tasks.

## Decisions Log
No decisions recorded.

## Loop Verdicts
No loop assessments performed.

## Deconfliction
<for each plugin scanned, record: plugin name, risk level, decision (keep/disable/deprioritize)>
```

6. Create `.oodaloop/PROJECT.md` with this content, substituting the project name:

```markdown
# Project: <project_name>

## Objective
To be defined.

## Requirements
To be populated during Observe phase.

## Constraints
To be populated during Observe phase.

## Scope Boundaries
- **In scope**: TBD
- **Out of scope**: TBD
- **Deferred**: TBD
```

7. Confirm initialization by reporting: project name, files created, deconfliction summary, current phase ("ready"), and recommended next step (`/oodaloop-observe`).

## Output

- Plugin conflict assessment table reported to user
- `.oodaloop/STATE.md` -- initialized with project name, date, phase "ready", deconfliction decisions
- `.oodaloop/PROJECT.md` -- initialized with project name, empty sections
- Confirmation message with next-step recommendation
