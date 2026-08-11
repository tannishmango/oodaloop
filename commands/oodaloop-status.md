---
name: oodaloop-status
description: Read-only summary of active OODALOOP state; ordinary work outside the framework has no status.
---

Read-only. No side effects.

1. Read `.oodaloop/CONTEXT.md` directly. If missing, report `No OODALOOP state found.` Do not recommend entering OODALOOP unless the user's current work actually warrants it.

2. Report only useful persistent context:
   - project/objective,
   - last refreshed,
   - current architecture/active decisions relevant to active work,
   - proof posture when relevant.

3. List active `.oodaloop/*.task.md` nodes and build parent-child relationships from `Parent:` fields.

For each node report:
- slug,
- phase (the next consequential judgment),
- updated timestamp,
- ready/complete/blocked leaves when evident,
- `Waiting` child + blocked leaf when present,
- material recorded surprise if unresolved.

Do not report obsolete labor mode, pause strategy, assessor state, or recursion-depth policy.

4. If state may be inconsistent or the session is resuming after context loss, use `/oodaloop-sync` to reconcile factual restartability. Do not run sync automatically for a simple status read unless inconsistency is evident.

5. BACKLOG is optional in status. Show only the top Next item/count when the user is choosing future work; otherwise leave it out of hot context.

6. Finish with the lightest valid next action for each active root: Observe, Orient, Decide, Act, Loop, waiting on child, or no action.

Keep the report compressed. Status exists to restore orientation, not narrate the framework.
