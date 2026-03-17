---
name: init
description: Initialize OODALOOP state directory in a target project.
---

## Trigger

User runs `/oodaloop-init` or starting a new project.

## Workflow

1. Check for existing `.oodaloop/`. If exists, warn and abort.
2. Create `.oodaloop/` directory.
3. Copy `STATE.md` and `PROJECT.md` from templates.
4. Set initial phase to `"ready"` in `STATE.md`.
5. Confirm initialization.

## Output

Initialized `.oodaloop/` directory with `STATE.md` and `PROJECT.md`.
