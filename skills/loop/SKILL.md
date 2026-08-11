---
name: loop
description: Reconcile implementation evidence with the objective and re-open the map only when something actually changed.
---

> Boyd's feedback loop matters because action changes what we know. The invariant is reorientation when evidence warrants it—not a mandatory second audit of every completed task.

## Trigger

`/oodaloop-loop` after Act completes the leaves needed for the current node, or at a meaningful subtree/root integration boundary.

## Preconditions

- Active task file contains execution evidence.
- `.oodaloop/CONTEXT.md` exists.

## Workflow

### 1. Reconcile evidence with intent

Read the Objective, Assessment/Plan invariants, and compact Execution evidence.

Ask only the questions that can change the next action:
- Did the completed work satisfy the objective?
- Did any surprise invalidate an assumption or parent decision?
- Did actual mutation/dependency scope materially differ from the map?
- Is proof adequate for the claims being made?
- Do individually valid leaves compose coherently at this boundary?

Do not re-run per-leaf verification simply because Loop exists.

### 2. Decide whether independent review is informative

There is **no mandatory aggregate assessor**.

Use a fresh-context reviewer only when the boundary contains material surprise, architecture/security risk, cross-leaf integration uncertainty, unexpected scope, or a proof gap where another semantic judgment can add information.

If the evidence is straightforward and all invariants/proof hold, skip review.

### 3. Verdict

Emit the lightest truthful outcome:

- **CONTINUE** — objective/invariants hold; proof is adequate; no new evidence requires replanning.
- **REFINE** — the objective/approach still holds, but a leaf, decomposition, integration, or proof path needs adjustment. Re-enter Decide at the affected node.
- **RESCOPE** — new evidence invalidates a fundamental assumption, objective framing, or approach. Re-enter targeted Observe/Orient with that evidence.

Do not require steelman paragraphs, ritual falsifiability prose, or confidence scores for routine CONTINUE verdicts.

For REFINE/RESCOPE, cite the concrete evidence that caused re-entry. For consequential CONTINUE decisions after material surprise, state why the surprise does not invalidate the parent trajectory.

### 4. Reconcile upward

If this task/node has a parent, propagate only information the parent needs:
- whether the child objective resolved,
- evidence that changes parent assumptions/invariants,
- the parent's resume point.

A child resolving does not imply its parent must repeat every phase. Resume at the lightest phase justified by the returned evidence.

### 5. Persist only reusable learning

Update `.oodaloop/CONTEXT.md` only when the cycle discovered something that would materially shorten or improve a future agent trajectory, especially:
- surprising repo behavior,
- non-obvious invariant,
- architectural constraint/decision,
- reusable proof requirement,
- failed approach with a causal lesson likely to recur.

Do not persist ordinary execution history.

Update BACKLOG only for real future work. Do not use it as a dumping ground for every observation.

### 6. Lightweight trajectory telemetry

Append one compact line to `.oodaloop/CYCLES.log` when available:

```text
<ISO date> slug=<slug> verdict=<CONTINUE|REFINE|RESCOPE> tasks=<n|?> surprises=<n|?> reviews=<n|?> children=<n|?>
```

Telemetry should be automatic and cheap. It exists to answer future empirical questions about routing and escalation—not to justify more process today.

### 7. Lifecycle

- **REFINE**: keep task file; phase → `decide`.
- **RESCOPE**: keep task file; phase → `observe` (or `orient` when the needed evidence is already present and only interpretation changed).
- **CONTINUE, root complete**: absorb reusable learning, then delete the ephemeral task file.
- **CONTINUE, child complete**: propagate the child result, delete the child file when safe, and resume the parent at the phase justified by the evidence.

## Output

A cheap reconciliation boundary that closes clean work quickly and makes new evidence capable of changing the trajectory when it actually should.
