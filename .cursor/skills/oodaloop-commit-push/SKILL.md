---
name: oodaloop-commit-push
description: Commits staged changes and pushes to main for the oodaloop plugin repo. Use when the user wants to commit and push, ship changes, push to main, or save and push. Project-scoped; does not modify the plugin.
---

# Commit and Push to Main

Commits staged changes and pushes to the default branch (main) in the current oodaloop plugin repository. Use when the user wants to commit changes, push to main, ship changes, or save and push. Does not modify the plugin manifest or plugin skill registry.

## When to use

- User says "commit and push", "push to main", "ship it", or "commit my changes"
- After completing work and user wants changes on the remote
- Handoff or session end where pushing is requested

## Prerequisites

- Repository is the oodaloop plugin repo (workspace root)
- Git is available; remote is configured
- Pre-commit hooks will run (sync, ephemeral-file check, skill-file validation, deprecated-name block). If hooks fail, fix reported issues before retrying.

## Workflow

1. **Confirm scope**  
   Ensure working directory is the oodaloop repo root. If the user specified a message or branch, use it.

2. **Inspect change set and style**
   - Run `git status` and `git diff --stat` to understand scope.
   - Run `git log --oneline -5` to match recent commit message style.

3. **Ensure changelog entry exists**
   - Confirm `CHANGELOG.md` has an entry under `## [Unreleased]` that covers this change.
   - If missing, add it before staging (pre-commit expects `CHANGELOG.md` in staged files).

4. **Draft commit plan**
   - If the user provided a commit message, use it.
   - Otherwise propose a short, imperative message focused on *why* the change exists.
   - Proceed directly when invocation implies commit/push intent; include proposed message in the final report.

5. **Stage and commit**
   - Stage intended files (`git add -A` for full scope or specific paths).
   - Do not stage `.oodaloop/*.task.md` or other ephemeral state.
   - Run `git commit` with the selected message.

6. **Push**  
   Run `git push origin HEAD` (or the user-requested branch target). If push fails (e.g. auth, non-fast-forward), report the error and do not force-push unless the user explicitly requests it.

7. **Confirm clean state**
   - Run `git status` after push and confirm the working tree state.
   - Report branch and push result to the user.

8. **Release nudge** (optional, non-blocking)  
   After a successful push, check whether `CHANGELOG.md` has content under `## [Unreleased]`. If it does, briefly note: "The `[Unreleased]` block has content — run `/release-cut` when this batch is ready to version." Do not cut a release automatically; only nudge.

## Notes

- This skill is for the **project** (Cursor project skills under `.cursor/skills/`). It is not part of the oodaloop plugin and must not be added to the plugin's skill list or manifest.
- Do not commit or push on behalf of the user without their clear intent (e.g. "commit and push" or "push these changes").
