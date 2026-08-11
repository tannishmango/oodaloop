---
name: observe
description: Gather only the evidence needed to reduce consequential uncertainty before planning.
---

> Boyd's Observe: gather information from the environment. In OODALOOP, Observe exists to improve the map before expensive action.

## Trigger

`/oodaloop-observe` after `/oodaloop-start` has determined that ordinary planning is insufficient, or targeted re-entry after implementation produces material surprise.

## Preconditions

- `.oodaloop/CONTEXT.md` exists.
- A concrete objective is known. If the user already supplied it, do not interview them again.

## Workflow

### 1. Create or resume the persistence anchor

For new work, create `.oodaloop/<slug>.task.md` early with only:

```markdown
# Task: <slug>
Parent: <parent-slug, only when this is genuinely a child node>

## Phase: observe
Started: <date>
Updated: <date>

## Objective
<objective>

## Why OODALOOP
<the unresolved uncertainty/risk that justified entering the framework>
```

For re-entry, reuse the existing task. Do not create a new child merely because new research is needed.

### 2. Read persistent context selectively

Read `.oodaloop/CONTEXT.md` for relevant architecture, conventions, prior decisions, proof infrastructure, and known surprises.

Do not perform a full convention/proof inventory by default. Re-scan only where the current objective depends on stale, missing, or contradictory context.

### 3. Research the territory

Use the researcher agent when isolation or breadth is useful. Research breadth-first, then deepen only where evidence can change the approach.

Capture facts with evidence:
- relevant structure and dependencies,
- existing patterns and constraints,
- proof paths,
- historical decisions when discoverable,
- risks or couplings that affect the objective.

Do not turn ordinary repo exploration into an exhaustive survey.

### 4. Blind-spot pass when novelty warrants it

For unfamiliar, high-consequence, or poorly framed work, ask:

> What might an expert in this codebase/domain know to investigate that is not implied by the current framing?

Use references, prototypes, targeted searches, or user questions only when they can materially reduce uncertainty.

The four-quadrant lens may help internally:
- known knowns,
- known unknowns,
- unknown knowns,
- unknown unknowns.

Do **not** create a mandatory quadrant worksheet. Unknown unknowns cannot be exhaustively enumerated; the runtime loop must also detect surprise later.

### 5. Persist the useful map

Write concise sections:

```markdown
## Observations
- <fact + evidence>

## Requirements
- <required behavior / constraint>

## Assumptions
- <assumption> — confidence: <high|medium|low>; invalidated by: <specific evidence>

## Open Decisions
- <consequential decision still unresolved, if any>

## Scope
- In: <...>
- Out: <...>
- Deferred: <...>
```

Do not persist ordinary search history or facts that will not affect planning or future recovery.

### 6. Sufficiency check

Observe is sufficient when the important unknowns are either:
- resolved,
- explicitly represented as assumptions/open decisions,
- or intentionally deferred because they do not block a safe plan.

If more evidence is likely to change the approach, keep researching. If a missing answer requires user judgment, ask that specific question.

Do not require ceremonial interactive checkpoints for observations, requirements, and scope separately.

### 7. Transition

Set phase to `orient` and update timestamp.

## Output

A compact evidence-backed map of the work, including the assumptions and unresolved decisions that actually matter. The value of Observe is uncertainty reduction, not artifact volume.
