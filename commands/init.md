---
name: oodaloop-init
description: Initialize .oodaloop/ state directory in the target project.
---

## Workflow

Creates `.oodaloop/` from templates (STATE.md, PROJECT.md). Validates no existing state. Sets initial phase to "ready".

## Inputs

- Target project root (default: current workspace)

## Outputs

- `.oodaloop/STATE.md` — phase, timestamps
- `.oodaloop/PROJECT.md` — project context placeholder

## Validation

- Fails if `.oodaloop/` already exists; user must confirm overwrite or choose different target.

## Reference

See `init` skill for detailed procedure.
