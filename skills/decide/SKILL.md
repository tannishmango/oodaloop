---
name: decide
description: Resolve consequential choices and decompose work only until executable leaves no longer require reinterpretation.
---

> Boyd's Decide: select a course of action from orientation. In OODALOOP, Decide should lower intent into executable work without over-specifying it.

## Trigger

`/oodaloop-decide` after Orient, or targeted re-entry when a supposed leaf is no longer executable under the current plan.

## Preconditions

- Active task file contains an Assessment.
- `.oodaloop/CONTEXT.md` exists.

## Workflow

### 1. Read the decision context

Read the Objective, relevant evidence, Assessment, and repo constraints/proof posture.

Focus on consequential decisions. Do not reload doctrine or state that cannot affect this plan.

### 2. Choose the weakest sufficient plan

Plan invariant:

> **Minimize residual consequential decisions while preserving maximum implementation optionality.**

Specify strongly where evidence requires it:
- objective/required behavior,
- invariants and constraints,
- known interfaces,
- dependencies,
- acceptance criteria,
- proof requirements,
- risk boundaries.

Avoid prescribing incidental file layout, function shapes, control flow, abstractions, or local implementation details unless they are actually constrained by the evidence.

### 3. Decompose only as far as useful

Represent the work as one or more task nodes. A task is a **leaf** when an executor can complete it without inventing a consequential decision absent from the spec.

Leaf-readiness test:

> Given this task, its relevant context, and acceptance/proof criteria, would a competent executor need to reinterpret product intent, choose architecture, discover substantial new scope, or make a high-impact trade-off in order to proceed?

- If no: it is executable.
- If yes: resolve the missing decision, research it, ask the user, or split/decompose further.

Do not split merely to satisfy an arbitrary task-count, file-count, or modification-count threshold. Mechanical multiplicity can remain one leaf when local judgment is negligible.

### 4. Define dependencies and execution freedom

Record dependencies only where ordering actually matters. Identify independent leaves that *may* execute concurrently.

The plan does not choose a permanent `direct`/`delegated` labor mode. Inline execution, subagents, parallelism, worktrees, and model selection are execution-substrate policies chosen by the host based on current capability, independence, context, and economics.

### 5. Define proportionate proof

Each leaf needs acceptance criteria and the strongest proportionate proof path available.

Do not require maximal test ceremony for low-risk work. Do not substitute easy proof for hard proof when the harder check is necessary to establish the claim.

For high-asymmetry external-state operations, record the safety boundary explicitly.

### 6. Optional independent plan review

There is **no mandatory plan assessor**.

Use a fresh-context reviewer only when the plan contains a judgment whose failure would be expensive and a second lens is likely to add information—for example architectural commitment, high blast radius, novel territory, or unresolved ambiguity that the planner may be anchoring on.

If used, review the actual decision/risk rather than forcing a fixed checklist. Incorporate useful evidence once; do not loop until a reviewer becomes stylistically satisfied.

### 7. Persist the plan

Use the smallest representation that preserves execution and recovery:

```markdown
## Plan

### Invariants
- <behavior/constraint that must hold>

### T1: <leaf title>
**Depends on**: <none | task ids>
**Intent**: <what this leaf accomplishes>
**Acceptance**: <observable criteria>
**Proof**: <proportionate proof path>

### T2: ...

### Open execution choices
- <implementation details intentionally left to executors, if useful>
```

A dependency graph is optional; add it only when it makes non-trivial ordering clearer.

Set phase to `act`.

## Output

An executable task tree whose leaves do not require consequential reinterpretation. No mandatory labor-strategy artifact, pre-mortem, steelman, assessor loop, or arbitrary decomposition quota.
