---
name: observe
description: Research and gather requirements through structured discovery.
---

> Boyd's Observe: Gather information from the environment. The raw input that feeds the loop. (foundation/OODALOOP.md)

> **Plugin paths**: `foundation/` references in this skill are relative to the OODALOOP plugin root, not the workspace. Resolve from this skill file's installed path.

## Trigger

`/oodaloop-observe` or entering Observe phase.

## Preconditions

- `.oodaloop/CONTEXT.md` must exist. **Verify by reading it** — if the Read tool returns an error, prompt for `/oodaloop-start`. Do not glob for `.oodaloop/**` (glob skips hidden directories).

## Workflow

### 1. Read persistent context
Read `.oodaloop/CONTEXT.md` for repo conventions, architecture patterns, and active decisions. This is the baseline -- do not rediscover what is already captured.

For non-trivial objectives or ambiguous scope, also read `foundation/PRINCIPLES-COMPRESSED.md` and apply only relevant heuristics. Skip for trivial work.

### 2. Check for convention drift
For each convention category, check whether sentinel files exist on disk that contradict what CONTEXT.md currently records. Only re-scan categories where a mismatch is found.

**Sentinel files per category:**
| Category | Check for existence of |
|---|---|
| Git | `.gitattributes`, `CONTRIBUTING.md` |
| Code Quality | `.pre-commit-config.yaml`, `ruff.toml`, `.eslintrc*`, `.prettierrc*`, `.flake8`, `pyproject.toml` (check for `[tool.ruff]` or `[tool.black]`) |
| Testing | `pytest.ini`, `jest.config.*`, `vitest.config.*`, `tests/`, `__tests__/`, `test/`, `spec/`, `integration/`, `e2e/`, `playwright/`, `cypress/`, `contract/`, `tests/integration/`, `tests/e2e/` |
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

When Testing drift is detected, re-evaluate and update the `Proof Infrastructure` subsection:
- posture (`none|weak|adequate|strong`)
- strongest available proof commands by area
- required environment for hard checks
- notable proof gaps and upgrade opportunities
- if the subsection is missing, create it as part of the update

If CONTEXT.md has no `Proof Infrastructure` subsection, or the subsection says `none` or `weak`, run a full proof inventory before proceeding. Dispatch the researcher agent to:
1. Inventory proof assets: test directories, configs, runners, project skill sources that define or wrap tests.
2. Inventory executable proof commands: package scripts, make/task targets, documented commands, commands embedded in skill markdown.
3. Inventory CI proof coupling: CI jobs that run tests, whether integration/e2e checks are required vs optional.
4. Inventory sandboxed test infrastructure: docker-compose files, testcontainers, localstack/mock-server setup, ephemeral fixtures. Document boundaries between sandbox and real-system validation.
5. Map strongest proof by area: for each major subsystem, record strongest available command.
6. Characterize coverage: posture (`none|weak|adequate|strong`), gaps (missing integration coverage, flaky suites, no reproducible command, env-gated checks without setup notes).
7. Update CONTEXT.md Proof Infrastructure subsection with findings.

Observe should not proceed on stale or shallow proof posture data.

### 3. Clarify scope
If the user has not provided a task description or objective, ask. Otherwise, proceed.

Determine a **task slug**: short, kebab-case, descriptive (e.g., `add-auth`, `fix-deploy`, `state-revision`). This names the task file.

### 4. Check for existing task files and persist skeleton
List any `*.task.md` files in `.oodaloop/`. If the user is resuming work on an existing task (slug matches), read that task file and build on it. If starting new work, **create the task file now** with skeleton content:

```markdown
# Task: <slug>
Parent: <parent-slug, if spawned from a blocking discovery; omit otherwise>

## Phase: observe
Started: <date>
Updated: <date>

## Objective
<objective from user input or intake -- even if preliminary>
```

This is the **persistence anchor**. All subsequent steps update this file in place. If the agent's turn ends unexpectedly at any point after this step, partial state is preserved on disk rather than lost in chat memory.

Also check for parent/child state:
- If any task file has phase `paused` with a `Child-slug` that doesn't match an existing task file, report: the parent is waiting for a child that hasn't been created yet. Offer to start the child cycle.
- If any task file has a `Parent:` field but the parent task file doesn't exist, report: this child is orphaned.
- If this observe was triggered to resolve a blocking discovery (either by a subagent dispatch, user following new-chat instructions, or in-chat flow), read the parent task file's Paused section for context. The `Child-objective`, `Reason`, and `Blocked-during` fields provide the starting context for this child cycle -- use them directly rather than re-discovering from scratch.

### 5. Research the codebase
Use the researcher agent (readonly). Focus on:
- **Structure**: directory layout, key files, entry points, configuration
- **Dependencies**: package manifests, imports, external services
- **Patterns**: naming conventions, testing approach, state management, error handling
- **Risks**: complexity hotspots, missing tests, tight coupling, stale code

Breadth first, then depth on areas relevant to the objective. Focus on what exists — facts and evidence, not interpretations of significance (that is Orient's job).

**Persist findings**: append the `## Observations` section to the task file with research results before presenting to the user. Write to disk first, then share.

**Interactive checkpoint**: share research findings with the user. "Here's what I found about the structure and patterns. Does this match your understanding? Anything I should look at more closely?" Incorporate feedback (update the task file with any corrections) before continuing.

### 6. Gather requirements
From user input + codebase research, identify:
- **Functional requirements**: what the deliverable must do
- **Constraints**: technology, performance, compatibility, time
- **Assumptions**: what we take as given (mark confidence level)
- **Open questions**: unknowns (mark as uncertain)

**Persist requirements**: append the `## Requirements` section to the task file before presenting to the user. Write to disk first, then share.

**Interactive checkpoint**: share identified requirements with the user. "Here are the requirements I've identified. What's missing? What's wrong?" Incorporate feedback (update the task file with any corrections) before continuing.

### 7. Verify task file completeness
The task file was created at step 4 and updated incrementally through steps 5-6. Before proceeding, **verify** it exists on disk and contains all required sections:

- `## Objective` (from step 4)
- `## Observations` (from step 5)
- `## Requirements` (from step 6)

If any section is missing, write it now. Do not proceed to step 8 with an incomplete task file.

```markdown
# Task: <slug>
Parent: <parent-slug, if spawned from a blocking discovery; omit otherwise>

## Phase: observe
Started: <date>
Updated: <date>

## Objective
<what we are accomplishing -- for child tasks, derived from parent's Child-objective>

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

### 8. Assess sufficiency and confirm scope
Sufficient when: objective is clear, key requirements identified, scope defined, major risks surfaced.

**Persist scope**: append the `## Scope` section to the task file before presenting to the user. Write to disk first, then share.

**Interactive checkpoint**: share the proposed scope with the user. "Here's the proposed scope — in, out, deferred. Are these the right boundaries?" Confirm before finalizing.

**Adaptive compression**: for simple, well-understood tasks, the three interactive checkpoints (steps 5, 6, 8) can compress into a single summary: "I've scanned the codebase and gathered requirements. Here's everything — does this look right?" When compressing, still persist all sections to the task file before presenting the combined summary. For complex or uncertain tasks, each checkpoint is a full pause.

If gaps remain, state them explicitly in the task file and ask the user whether to research further or proceed with known uncertainty.

### 9. Report and transition
Update task file phase from `observe` to `orient`. Update timestamp.

Summarize findings to user. Recommend `/oodaloop-orient` to analyze findings and form a situational assessment.

## Output

- `.oodaloop/CONTEXT.md` updated if conventions drifted
- `.oodaloop/<slug>.task.md` created with requirements, observations, scope
- Task file phase updated from `observe` to `orient`
- Summary reported with next-step recommendation
