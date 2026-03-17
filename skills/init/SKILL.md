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

3. Create the `.oodaloop/` directory.

4. Create `.oodaloop/STATE.md` with this content, substituting the project name and today's date:

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
No deconfliction decisions recorded.
```

5. Create `.oodaloop/PROJECT.md` with this content, substituting the project name:

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

6. Confirm initialization by reporting: project name, files created, current phase ("ready"), and recommended next step (`/oodaloop-observe`).

## Output

- `.oodaloop/STATE.md` -- initialized with project name, date, phase "ready"
- `.oodaloop/PROJECT.md` -- initialized with project name, empty sections
- Confirmation message with next-step recommendation
