---
name: orient
description: Turn observations into the minimum sufficient understanding needed to make consequential decisions safely.
---

> Boyd's Orient: interpret observations through context and mental models. This is where OODALOOP should spend reasoning when uncertainty actually warrants it.

## Trigger

`/oodaloop-orient` after Observe, or targeted re-entry when new evidence changes the current map.

## Preconditions

- Active task file contains Objective, Observations, and enough Requirements/Scope to interpret the work.
- `.oodaloop/CONTEXT.md` exists.

If these are missing, return only to the missing evidence source. Do not improvise a full recovery workflow.

## Workflow

### 1. Interpret, do not restate

Read the task evidence and relevant persistent context.

For each important observation, state what it implies for the objective. Distinguish facts from interpretations.

### 2. Identify residual consequential decision load

Ask:

> What consequential judgment would an implementer still have to invent if work started now?

Consider:
- unresolved requirements,
- architectural/cross-system choices,
- assumptions that could change the approach,
- unclear interfaces or ownership,
- proof gaps,
- risk/blast-radius questions,
- dependencies that affect ordering or decomposition.

Do not score this numerically. The purpose is to expose the decisions, not manufacture a complexity metric.

### 3. Narrow the option space without overcommitting

Evaluate viable approaches only where a real choice remains. Prefer the weakest sufficient commitment:

> resolve what must be resolved for safe execution; preserve implementation optionality where evidence does not justify a prescription.

A recommendation may strongly constrain behavior, invariants, interfaces, safety, and proof while intentionally leaving local implementation details to the executor.

### 4. Re-check assumptions

For important assumptions, ensure an invalidation condition exists: what observable evidence would make this assumption unsafe to continue using?

If current evidence already triggers an invalidation condition, revise the interpretation before planning.

### 5. Decide whether planning is ready

Ready for Decide when:
- the objective is coherent,
- consequential unresolved decisions are either resolved or explicitly delegated to a higher-judgment planning choice,
- remaining local implementation choices can safely be made by executors,
- proof expectations are understood well enough to constrain the plan.

If targeted research would materially change the recommendation, return to Observe for that research only.

If the user must choose among materially different outcomes, ask the specific question instead of hiding the choice in the plan.

### 6. Persist a compact assessment

```markdown
## Assessment

### Interpretation
<what the evidence means for this objective>

### Consequential decisions
- <decision + chosen resolution, or explicitly unresolved>

### Assumptions / invalidation
- <assumption> → invalidated by <evidence>

### Constraints and invariants
- <what implementation must preserve>

### Recommendation
<preferred direction and why, including what is intentionally left open>
```

Set phase to `decide`.

## Output

A decision-ready interpretation that reduces consequential ambiguity without prescribing unevidenced implementation detail.
