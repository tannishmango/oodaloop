---
name: orient
description: Analyze observations and form a situational assessment.
---

> Boyd's Orient: Process observations through experience and mental models to form a perception of reality. The cognitive engine of the OODA Loop. (foundation/OODALOOP.md)

> **Plugin paths**: `foundation/` references in this skill are relative to the OODALOOP plugin root, not the workspace. Resolve from this skill file's installed path.

## Trigger

`/oodaloop-orient` or transitioning from Observe phase.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with populated Requirements, Observations, and Scope sections.
- `.oodaloop/CONTEXT.md` must exist.
- If an Assessment section already exists (re-entry after rescope), note it — the previous assessment is being revised, not started from scratch.

**If no task file exists**: this means Observe did not persist its output. Do NOT silently reconstruct from chat memory or proceed without a task file. Instead:
1. Report the gap: "Observe completed in conversation but the task file was not written to disk."
2. Recommend re-running `/oodaloop-observe` to persist findings properly.
3. Do not proceed with Orient until the task file exists on disk with the required sections.

## Workflow

### 1. Read observations and context
Read the active task file: requirements, observations, scope, and any existing assessment.

Read `.oodaloop/CONTEXT.md` for prior decisions, architecture patterns, and conventions — Boyd's "repertoire of mental models." This is the experience dimension that transforms raw observation into understanding.

For non-trivial planning and trade-off decisions, also read `foundation/PRINCIPLES-COMPRESSED.md` and apply only relevant heuristics.

### 2. Interpret findings
Transform facts into meaning. For each significant observation, state what it means for the current work — not what was found, but what it implies.

If a sentence in the interpretation could appear unchanged in the Observations section, it is not interpretation. "The test suite has no integration tests" is an observation. "We cannot verify API behavior with existing infrastructure" is interpretation.

When codebase investigation is needed during analysis, dispatch the researcher agent (readonly).

### 3. Compare against prior decisions
Review decisions recorded in CONTEXT.md. For each relevant prior decision:
- Does it constrain the current work? (e.g., "chose library X" limits technology choices)
- Does it enable a faster path? (e.g., "pattern Z adopted" means we follow it, not reinvent)
- Does it conflict with what the observations suggest?

### 4. Narrow the option space
Evaluate viable approaches for the current work:
- For each approach: what it entails, its trade-offs, and constraints that apply.
- If only one approach is viable, state why alternatives were eliminated.
- Recommend one approach with rationale. Orient recommends; Decide commits.

### 5. Identify risks to the understanding
Stress-test the interpretation, not a plan (there is no plan yet):
- What could be wrong about the assessment?
- What assumptions are being made, and what would invalidate them?
- Where is confidence lowest, and what additional information would help?

### 6. Assess sufficiency
Is the understanding clear enough for Decide to produce a plan?
- If yes: proceed to write the Assessment section.
- If no: state what's missing and recommend returning to `/oodaloop-observe` for targeted research.

### Mid-execution re-entry
When re-entering after a rescope (existing execution log and Paused section in the task file), read the execution log and Paused section. Account for existing work:
- What is salvageable and still valid?
- What needs modification given the new understanding?
- What should be discarded?

The revised assessment must reflect the current state, not just the original observations.

## Output

Append to the task file:

```markdown
## Assessment

### Situational interpretation
<what the observations mean — not restating findings, interpreting them>

### Viable approaches
<narrowed options, trade-offs, constraints per approach>

### Risks and assumptions
<stress-tested understanding, not plan risks>

### Constraints
<from conventions, architecture, prior decisions, proof posture>

### Recommendation
<which approach and why — orient recommends, decide commits>
```

- Update task file phase from `orient` to `decide`. Update timestamp.
- Recommend `/oodaloop-decide` to formulate the plan.
