---
name: observe
description: Research and gather requirements through structured discovery.
---

## Trigger

`/oodaloop-observe` or entering Observe phase.

## Preconditions

- `.oodaloop/` must exist. If not, prompt for `/oodaloop-init`.
- `.oodaloop/CONTEXT.md` must exist.

## Workflow

### 1. Read persistent context
Read `.oodaloop/CONTEXT.md` for repo conventions, architecture patterns, and active decisions. This is the baseline -- do not rediscover what is already captured.

### 2. Check for convention drift
Compare CONTEXT.md's conventions against what is currently on disk. For each convention category: if the config files mentioned have been added, removed, or meaningfully changed since the last refresh date, update that section in CONTEXT.md and bump the refresh timestamp. If nothing changed, skip. This keeps context current without redundant re-scanning.

### 3. Clarify scope
If the user has not provided a task description or objective, ask. Otherwise, proceed.

Determine a **task slug**: short, kebab-case, descriptive (e.g., `add-auth`, `fix-deploy`, `state-revision`). This names the task file.

### 4. Check for existing task files
List any `*.task.md` files in `.oodaloop/`. If the user is resuming work on an existing task (slug matches), read that task file and build on it. If starting new work, create a new task file.

### 5. Research the codebase
Use the researcher agent (readonly). Focus on:
- **Structure**: directory layout, key files, entry points, configuration
- **Dependencies**: package manifests, imports, external services
- **Patterns**: naming conventions, testing approach, state management, error handling
- **Risks**: complexity hotspots, missing tests, tight coupling, stale code

Breadth first, then depth on areas relevant to the objective.

### 6. Gather requirements
From user input + codebase research, identify:
- **Functional requirements**: what the deliverable must do
- **Constraints**: technology, performance, compatibility, time
- **Assumptions**: what we take as given (mark confidence level)
- **Open questions**: unknowns (mark as uncertain)

### 7. Create or update task file
Create `.oodaloop/<slug>.task.md`:

```markdown
# Task: <slug>

## Phase: observe
Started: <date>
Updated: <date>

## Objective
<what we are accomplishing>

## Requirements
### R1: <title>
<description>

### R2: ...

## Observations
### O1: <title>
<finding with evidence -- file paths, patterns, concrete examples>

### O2: ...

## Scope
- **In**: <what we will do>
- **Out**: <what we will not do>
- **Deferred**: <what we will do later>
```

### 8. Assess sufficiency
Sufficient when: objective is clear, key requirements identified, scope defined, major risks surfaced. If gaps remain, state them explicitly in the task file and ask the user whether to research further or proceed with known uncertainty.

### 9. Report
Summarize findings to user. Recommend `/oodaloop-orient` to create the plan.

## Output

- `.oodaloop/CONTEXT.md` updated if conventions drifted
- `.oodaloop/<slug>.task.md` created with requirements, observations, scope
- Summary reported with next-step recommendation
