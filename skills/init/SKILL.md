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

3. **Scan for plugin conflicts.** Check which plugins are active in this workspace. For each, assess interference risk against OODALOOP:
   - **High risk** (recommend disable): injects mandatory context via hooks, enforces unconditional hard gates, or overrides workflow autonomy.
   - **Medium risk** (recommend deprioritize): runs background processes or follow-up loops that add noise.
   - **Low risk** (keep): provides scoped, opt-in capabilities that don't conflict.

   Report as a table: `| Plugin | Risk | Recommendation | Reason |`
   Let the user decide. Do not disable anything automatically.

4. **Detect host environment.** Determine which agent environment is running OODALOOP by checking for host-specific markers:
   - `.cursor-plugin/` or `~/.cursor/` → Cursor
   - `.claude/` or `~/.claude/` → Claude Code
   - `.opencode/` or `~/.config/opencode/` → OpenCode
   - If ambiguous, ask the user.
   Record the detected host in the Workspace Tooling section of CONTEXT.md. This informs convention scanning and future command references.

5. **Scan repo conventions.** For each category, check for known config files and extract key facts. If nothing found for a category, record "None detected."

   **Git**: `.gitattributes`, recent commit messages (sample 5 for format patterns), branch naming from `git branch -a`, any `CONTRIBUTING.md`.
   **Code Quality**: `.pre-commit-config.yaml` (list hooks), linter configs (`ruff.toml`, `.eslintrc*`, `.prettierrc*`, `pyproject.toml [tool.ruff]`, `pyproject.toml [tool.black]`, `.flake8`).
   **Testing**: test runner config (`pytest.ini`, `pyproject.toml [tool.pytest]`, `jest.config.*`, `vitest.config.*`), test directories (`tests/`, `__tests__/`, `test/`, `spec/`), coverage config.
   **Proof Infrastructure**: identify highest-truth verification mechanisms and how to run them. At minimum scan for:
   - integration/e2e/contract suites (`integration/`, `e2e/`, `playwright/`, `cypress/`, `contract/`, `tests/integration/`, `tests/e2e/`)
   - test commands in manifests (`scripts.test:*`, `make test-*`, CI jobs that run integration/e2e checks)
   - environment requirements (credentials, services, docker compose, seeded databases)
   - mapping from major repo areas to strongest available proof command
   Then classify posture:
   - `none`: no meaningful automated proof beyond basic unit checks or ad-hoc manual testing
   - `weak`: proof exists but misses major integration surfaces, is flaky, or is rarely run
   - `adequate`: integration surfaces mostly covered with executable commands
   - `strong`: clear high-signal integration proof exists for critical paths and is enforced in CI
   Include explicit upgrade opportunities when posture is `none` or `weak`.
   **CI/CD**: `.github/workflows/` (list files), `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`.
   **Dependencies**: manifest (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`), lockfiles (`poetry.lock`, `uv.lock`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`).
   **Workspace Tooling**: workspace rule files, `AGENTS.md`, and local agent/tooling settings files.

6. Create the `.oodaloop/` directory.

7. Create `.oodaloop/CONTEXT.md` with the following content, substituting project name, today's date, convention scan findings, host environment, and deconfliction findings:

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

### Proof Infrastructure
Posture: <none|weak|adequate|strong>
<strongest available proof commands, coverage map, environment requirements, and upgrade opportunities>

### CI/CD
<findings or "None detected.">

### Dependencies
<findings or "None detected.">

### Workspace Tooling
Host: <detected host environment>
<findings or "None detected.">

## Architecture
To be populated during Observe phase.

## Decisions
No decisions recorded.

## Deconfliction
<for each plugin: name, risk, decision>
```

8. Create `.oodaloop/BACKLOG.md` with:

```markdown
# Backlog

Items discovered during OODA cycles and conversations. Curated by loop phase.

## Next
No items yet.

## Later
No items yet.

## Done
No completed items.
```

9. Confirm initialization: project name, host environment, files created (CONTEXT.md, BACKLOG.md), convention summary, proof-infrastructure posture and strongest commands, deconfliction summary, current state ("ready for observe"), recommended next step (`/oodaloop-observe`).

## Output

- Plugin conflict assessment table reported to user
- Convention scan findings reported to user
- `.oodaloop/CONTEXT.md` initialized with conventions and deconfliction
- `.oodaloop/BACKLOG.md` initialized empty
- Confirmation with next-step recommendation
