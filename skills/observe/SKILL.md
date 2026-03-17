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
For each convention category, check whether sentinel files exist on disk that contradict what CONTEXT.md currently records. Only re-scan categories where a mismatch is found.

**Sentinel files per category:**
| Category | Check for existence of |
|---|---|
| Git | `.gitattributes`, `CONTRIBUTING.md` |
| Code Quality | `.pre-commit-config.yaml`, `ruff.toml`, `.eslintrc*`, `.prettierrc*`, `.flake8`, `pyproject.toml` (check for `[tool.ruff]` or `[tool.black]`) |
| Testing | `pytest.ini`, `jest.config.*`, `vitest.config.*`, `tests/`, `__tests__/`, `test/`, `spec/` |
| CI/CD | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/` |
| Dependencies | `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt` and their lockfiles |
| Workspace Tooling | `.cursor/rules/`, `AGENTS.md`, `.claude/` |

**Detection logic:**
1. For each category, glob for its sentinel files.
2. Compare results against what CONTEXT.md says for that category:
   - If CONTEXT.md says "None detected" but sentinel files now exist → drift. Re-scan that category using the init skill's full scan logic and update CONTEXT.md.
   - If CONTEXT.md describes specific tools but their config files no longer exist → drift. Update to reflect removal.
   - If sentinel files match what CONTEXT.md already records → no drift. Skip.
3. If any category was updated, bump the "Last refreshed" timestamp.
4. If nothing drifted, skip entirely -- do not touch CONTEXT.md.

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
Create `.oodaloop/<slug>.task.md`. If this observe was triggered by a blocking discovery from another task, include `Parent: <parent-slug>` and inherit only the blocker context (not the entire parent task):

```markdown
# Task: <slug>
Parent: <parent-slug, if spawned from a blocking discovery; omit otherwise>

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
