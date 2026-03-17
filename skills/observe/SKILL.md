---
name: observe
description: Research and gather requirements through structured discovery.
---

## Trigger

`/oodaloop-observe` or entering Observe phase after init.

## Preconditions

- `.oodaloop/` must exist. If not, prompt for `/oodaloop-init` first.
- `.oodaloop/STATE.md` must show phase `ready` or `observe` (re-entry from loop RESCOPE is valid).

## Workflow

### 1. Read current state
Read `.oodaloop/STATE.md` and `.oodaloop/PROJECT.md` for existing context. If PROJECT.md already has observations from a prior run, build on them rather than starting from scratch.

### 2. Clarify scope
If the user hasn't provided a task description or objective:
- Ask what they want to accomplish.
- Update the Objective section in `PROJECT.md`.

If the user has provided a clear task, proceed directly.

### 3. Research the codebase
Use the researcher agent (readonly) to explore. Focus on:
- **Structure**: directory layout, key files, entry points, configuration
- **Dependencies**: package manifests, imports, external services
- **Existing documentation**: READMEs, inline docs, architecture notes
- **Patterns**: conventions, naming, testing approach, state management
- **Risks**: complexity hotspots, missing tests, tight coupling, stale code

Aim for breadth first, then depth on areas relevant to the objective.

### 4. Gather requirements
From user input + codebase research, identify:
- **Functional requirements**: what must the deliverable do
- **Constraints**: technology, performance, compatibility, time
- **Assumptions**: what we're taking as given (mark confidence level)
- **Open questions**: things we don't know yet (mark as uncertain)

### 5. Write findings to PROJECT.md
Update `.oodaloop/PROJECT.md` with structured sections:

```markdown
## Requirements
### R1: <requirement title>
<description>

### R2: ...

## Constraints
- <constraint>

## Observations
### O1: <observation title>
<finding with evidence -- file paths, patterns, concrete examples>

### O2: ...

## Scope Boundaries
- **In scope**: <what we will do>
- **Out of scope**: <what we won't do>
- **Deferred**: <what we'll do later>
```

### 6. Assess sufficiency
Observations are sufficient when:
- The objective is clear
- Key requirements are identified (even if some are uncertain)
- Scope boundaries are defined
- Major risks or unknowns are surfaced

If gaps remain, state them explicitly in PROJECT.md and ask the user whether to research further or proceed with known uncertainty.

### 7. Update state
Set `.oodaloop/STATE.md` phase to `orient`. Update the Task Progress and Last Updated fields.

## Output

- `.oodaloop/PROJECT.md` populated with requirements, constraints, observations, and scope
- `.oodaloop/STATE.md` phase advanced to `orient`
- Summary of findings reported to the user with recommendation to proceed to `/oodaloop-orient`
