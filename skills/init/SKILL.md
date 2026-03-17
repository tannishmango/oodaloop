---
name: init
description: Initialize OODALOOP state directory in a target project.
---

## Trigger

User runs `/oodaloop-init` or starting a new OODALOOP-tracked project.

## Workflow

1. Determine the project name from the workspace root directory name (e.g., `my-app`). If the user provides a name, use that instead.

2. Check if `.oodaloop/` already exists in the workspace root.
   - If it exists: warn the user and **stop**. Do not overwrite existing state.
   - If it does not exist: proceed.

3. **Scan for plugin conflicts.** Check which Cursor plugins are active in this workspace. For each, assess interference risk against OODALOOP:
   - **High risk** (recommend disable): injects mandatory context via hooks, enforces unconditional hard gates, or overrides workflow autonomy.
   - **Medium risk** (recommend deprioritize): runs background processes or follow-up loops that add noise.
   - **Low risk** (keep): provides scoped, opt-in capabilities that don't conflict.

   Report as a table: `| Plugin | Risk | Recommendation | Reason |`
   Let the user decide. Do not disable anything automatically.

4. **Scan repo conventions.** For each category, check for known config files and extract key facts. If nothing found for a category, record "None detected."

   **Git**: `.gitattributes`, recent commit messages (sample 5 for format patterns), branch naming from `git branch -a`, any `CONTRIBUTING.md`.
   **Code Quality**: `.pre-commit-config.yaml` (list hooks), linter configs (`ruff.toml`, `.eslintrc*`, `.prettierrc*`, `pyproject.toml [tool.ruff]`, `pyproject.toml [tool.black]`, `.flake8`).
   **Testing**: test runner config (`pytest.ini`, `pyproject.toml [tool.pytest]`, `jest.config.*`, `vitest.config.*`), test directories (`tests/`, `__tests__/`, `test/`, `spec/`), coverage config.
   **CI/CD**: `.github/workflows/` (list files), `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`.
   **Dependencies**: manifest (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`), lockfiles (`poetry.lock`, `uv.lock`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`).
   **Cursor**: `.cursor/rules/` (list files), `AGENTS.md`, `.cursorrules`.

5. Create the `.oodaloop/` directory.

6. Create `.oodaloop/CONTEXT.md` with the following content, substituting project name, today's date, convention scan findings, and deconfliction findings:

```markdown
# Context: <project_name>

> Last refreshed: <today YYYY-MM-DD>

## Objective
To be defined during Observe phase.

## Conventions

### Git
<findings or "None detected.">

### Code Quality
<findings or "None detected.">

### Testing
<findings or "None detected.">

### CI/CD
<findings or "None detected.">

### Dependencies
<findings or "None detected.">

### Cursor
<findings or "None detected.">

## Architecture
To be populated during Observe phase.

## Decisions
No decisions recorded.

## Deconfliction
<for each plugin: name, risk, decision>
```

7. Confirm initialization: project name, file created, convention summary, deconfliction summary, current state ("ready for observe"), recommended next step (`/oodaloop-observe`).

## Output

- Plugin conflict assessment table reported to user
- Convention scan findings reported to user
- `.oodaloop/CONTEXT.md` initialized with conventions and deconfliction
- Confirmation with next-step recommendation
