---
name: decide
description: Decompose the assessment into a sequenced, executable plan.
---

> Boyd's Decide: Select a course of action from the understanding formed during orientation. (foundation/OODALOOP.md)

> **Plugin paths**: `foundation/` references in this skill are relative to the OODALOOP plugin root, not the workspace. Resolve from this skill file's installed path.

## Trigger

`/oodaloop-decide` or transitioning from Orient phase.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with an Assessment section (from orient).
- `.oodaloop/CONTEXT.md` must exist.
- Task file phase should be `decide`.

## Workflow

### 1. Read assessment and context
Read the active task file's Assessment section — the situational interpretation, viable approaches, risks, constraints, and recommendation from orient.

Read the Observations section for underlying facts.

Read `.oodaloop/CONTEXT.md` conventions — these are binding constraints on the plan (commit format, linter rules, test patterns, etc.).
Extract `Proof Infrastructure` details as binding for verification selection.

For non-trivial, uncertain, or high-impact implementation choices, also read `foundation/PRINCIPLES-COMPRESSED.md` and apply only relevant heuristics.

### 2. Identify work streams
Group related requirements into logical streams. Look for:
- Natural clusters (e.g., "data layer" vs "UI")
- Shared dependencies between requirements
- Independent streams that can be parallelized

### 3. Decompose into atomic tasks
For each stream, break into tasks where each task:
- Has a single concern (one thing changes)
- Can be verified independently
- Has clear acceptance criteria that specify the required test type: unit tests for logic, integration tests for external systems/APIs/data pipelines. If CONTEXT.md shows the repo has integration test infrastructure for the area being changed, acceptance criteria must require integration tests pass — not just unit tests.
- Includes a **Proof Plan** naming the strongest available verification command(s) for that task and when they will be run.
- Takes no more than one focused session

Never downshift to weaker proof when stronger repo-native proof exists, unless explicitly justified (e.g., missing credentials, destructive side effects, excessive runtime). Any downshift must be written into acceptance criteria as a gap with rationale.

Dispatch the planner agent (readonly) for decomposition work.

### 4. Define dependencies and parallelism
For each task, identify:
- Which tasks must complete first
- Which can run in parallel
- The dependency graph

### 5. Write plan into task file
Append the plan section to the existing task file:

```markdown
## Plan

### T1: <title>
**Depends on**: none
**Acceptance**: <concrete, verifiable criteria>
**Proof Plan**: <commands + expected evidence tier + any gating prerequisites>

### T2: <title>
**Depends on**: T1
**Acceptance**: <criteria>
**Proof Plan**: <commands + expected evidence tier + any gating prerequisites>

...

### Dependency Graph
<ASCII diagram or description>

### Execution Strategy
Batch 1: <parallel tasks>
Batch 2: <next tasks>
...
```

### 6. Pre-mortem and steelman
Before finalizing, confront the plan's weaknesses:
- **Pre-mortem**: assume the plan fails. What are the most likely failure modes? For each, state what signal would reveal it during execution and what the fallback is. Append to the plan:
  ```markdown
  ### Failure modes
  - <failure mode>: signal = <what you'd see>, fallback = <what to do>
  ```
- **Steelman**: if an alternative approach was considered and rejected, state the strongest argument for it and why the chosen approach still wins. If no alternative was considered, state that explicitly — it may indicate the orient phase was too shallow.

Skip this step only for trivial tasks where the plan is obvious and the risk is negligible.

### 7. Review
Check before finalizing:
- Every requirement covered by at least one task
- No ambiguous acceptance criteria
- Dependencies form a valid DAG (no cycles)
- Plan is executable without reinterpretation
- Convention constraints from CONTEXT.md are reflected in relevant tasks
- Proof plans match repo proof posture (hardest available checks are selected when relevant)
- Failure modes identified for non-trivial plans

### 8. Update task file phase
Set the task file phase to `act`. Update the timestamp.

## Output

- Plan section appended to `.oodaloop/<slug>.task.md`
- Task file phase set to `act`
- Summary reported with recommendation to proceed to `/oodaloop-act`
