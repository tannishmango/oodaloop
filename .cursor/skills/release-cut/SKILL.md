---
name: release-cut
description: Cuts a versioned release for the oodaloop plugin by graduating [Unreleased] content in CHANGELOG.md to a named version, then committing and pushing. Use when the user says "cut a release", "release this", "tag a version", or "ship a release".
---

# Release Cut

Graduates the `[Unreleased]` block in `CHANGELOG.md` to a named version entry, commits, and pushes.

## When to use

- User says "cut a release", "ship a release", "tag this as a version", or "release these changes"
- After a coherent capability batch is complete (a feature, safety layer, or governance initiative)
- When `[Unreleased]` has meaningful content and the user wants it pinned to a reference-able version

## When NOT to use

- `[Unreleased]` is empty — nothing to release
- The user just wants to commit without versioning — use `/commit-push` instead

## Release trigger heuristic

A release is warranted when the `[Unreleased]` block represents a coherent batch: a new capability, a safety or governance layer, an architectural change. Single-file tweaks or minor fixes can accumulate further before cutting. When in doubt, ask the user.

## Versioning scheme

Format: `M<major>.<minor>` with date `YYYY-MM-DD`.

- **Major bump** (`M5`, `M6`, ...): architectural rewrite, phase redesign, or breaking change to core OODA flow
- **Minor bump** (`.x`): new capability, safety layer, governance fix, or significant behavioral change within the existing architecture
- Minor increments are not necessarily sequential — use judgment to skip numbers if the delta is large

To determine the next version:
1. Read the most recent versioned entry in CHANGELOG.md (first `## [M...]` below `[Unreleased]`)
2. Assess whether the unreleased content warrants a major or minor bump
3. Propose the version to the user if uncertain; otherwise proceed

## Workflow

1. **Read CHANGELOG.md**
   Check that `[Unreleased]` has content. If empty, report and stop.

2. **Determine next version**
   Read the most recent versioned entry. Propose version based on the delta heuristic above. If user provided a version, use it.

3. **Consolidate sections**
   The `[Unreleased]` block must have at most one `### Added`, one `### Changed`, one `### Fixed`, and one `### Removed`. If there are duplicate typed sections from multiple commits, merge their bullet lists under one heading each before cutting. Remove any empty typed sections.

4. **Cut the release**
   Replace `## [Unreleased]` with:
   ```
   ## [Unreleased]

   ## [M<version>] - <YYYY-MM-DD>
   ```
   Move all content from `[Unreleased]` under the new version header.

5. **Commit and push**
   Stage `CHANGELOG.md`. Commit with message: `Release M<version>`. Push to main.

6. **Confirm**
   Report the version, date, and that it is pushed to main.

## Notes

- This skill is project-scoped (`.cursor/skills/`). It is not part of the oodaloop plugin and must not be added to the plugin manifest or skill list.
- Pre-commit hooks will run on commit. If they fail, fix reported issues before retrying.
- Do not create git tags unless the user explicitly requests it.
