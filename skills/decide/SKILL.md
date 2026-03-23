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
- Flags external state mutations with `**Destructive**: yes — <what state is mutated and how>` so the act phase enforces confirmation gates. Any task involving database operations, Docker state, deployment, or service mutations MUST carry this flag.
- Takes no more than one focused session

**Scope stress test** — apply after initial decomposition, before finalizing:
- Count distinct code modifications per task (not files — modifications). A task claiming "single concern" but requiring >3-4 distinct modifications with per-site judgment is under-scoped regardless of conceptual unity. "Modify 22 call sites" is 22 modifications. "Rename 10 files with cross-imports" is 10+ modifications. Split multiplicative tasks unless modifications are truly mechanical find-replace requiring zero per-site judgment.
- Enumerate concretely: if acceptance criteria reference "every X" or "all Y," list the concrete instances in the task. Vague quantifiers defer scope discovery to the executor, causing drift during implementation.
- Separate separable concerns: if a task addresses two independently verifiable concerns (e.g., "strip PII AND demote log levels"), split them — even if they touch overlapping files.

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
- No task contains under-scoped work — scope stress test passed (Step 3)
- All vague quantifiers ("every X", "all Y") resolved to concrete enumerated instances
- Convention constraints from CONTEXT.md are reflected in relevant tasks
- Proof plans match repo proof posture (hardest available checks are selected when relevant)
- Failure modes identified for non-trivial plans

If any check fails, fix the plan (re-decompose failing tasks, re-enumerate, update dependencies) and re-run this review. Do not proceed to Step 8 with known defects.

### 8. Plan assessment
Dispatch the **assessor agent in plan mode** (Type 3) to evaluate the plan's executability and recommend a labor strategy. The assessor receives:
- The assessor agent definition (`agents/assessor.md`) — this is the governing specification for the assessment. Do NOT override the assessor's checks, mode vocabulary, or output format in the dispatch prompt.
- The full task file (all sections through Plan)
- `.oodaloop/CONTEXT.md`

The assessor's labor strategy uses exactly two modes: `direct` (roughly ≤6 tasks) or `delegated` (more than ~6 tasks), determined by cumulative context load — not per-task complexity or parallelism structure. Do not prompt the assessor with alternative vocabularies.

Read the assessor's output. **Validate before accepting:**
- Mode is exactly `direct` or `delegated`. Any other value (e.g., "hybrid", "sequential", "parallel") means the assessor deviated from spec — re-dispatch with the agent definition explicitly referenced.
- Rationale references task count and cumulative context load.
- Pre-scoping flags identify specific task IDs with concrete ambiguity.

Append a `### Labor Strategy` subsection at the end of the Plan section with the assessor's structured result (mode, rationale, pre-scoping flags, notes).

If the assessor flags under-scoped tasks or pre-scoping issues: resolve them (split tasks, enumerate deferred scope, refine acceptance criteria, update dependency graph). Then **re-dispatch the assessor** on the revised plan — task count and dependencies have changed, which may affect the labor strategy mode. Repeat until the assessor returns no blocking scope issues.

Include any unresolved pre-scoping flags in the phase transition summary so the user is aware before act begins.

### 9. Update task file phase
Set the task file phase to `act`. Update the timestamp.

## Output

- Plan section appended to `.oodaloop/<slug>.task.md` with Labor Strategy subsection
- Task file phase set to `act`
- Summary reported with recommendation to proceed to `/oodaloop-act`
