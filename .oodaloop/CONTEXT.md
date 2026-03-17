# Context: oodaloop

> Last refreshed: 2026-03-17 (M3.1 adapter architecture complete)

## Objective
Build OODALOOP into a functional plugin that orchestrates project delivery using an adaptive OODA loop. The plugin builds itself -- each milestone improves the tooling used to execute the next milestone.

## Conventions

### Git
Standard git workflow. No branch protection. Commit messages are descriptive, imperative mood. No `.gitattributes`. No `CONTRIBUTING.md`.

### Code Quality
None detected. Plugin is pure markdown/declarative -- no linters, formatters, or pre-commit hooks.

### Testing
No automated test framework. Plugin is tested by running commands against target projects (e.g., `/oodaloop-init` on `autotracing` repo). Structural validation via file existence checks.

### CI/CD
None detected. No `.github/workflows/`, no CI pipeline.

### Dependencies
None. Pure markdown plugin with no package manager, no lockfiles, no runtime dependencies.

### Workspace Tooling
This plugin has commands, skills, agents, rules, and templates, and supports local plugin loading for development.

## Architecture
Plugin follows commands → skills → agents pattern. Commands are thin wrappers invoking skills. Skills contain procedural logic. Agents define roles with readonly constraints (only executor writes). Doctrine lives in `foundation/` (PRINCIPLES.md, SYSTEMS-REFERENCE.md). State lives in `.oodaloop/` using CONTEXT.md (persistent) + task files (ephemeral).

## Decisions

### M1 (ground breaking)
- 2026-03-16: Plugin structure: 8 commands, 7 skills, 5 agents, 3 rules
- 2026-03-16: Doctrine canonical home = `foundation/`
- 2026-03-16: `superpowers` plugin disabled at workspace level; OODALOOP rules take precedence
- 2026-03-16: `START.md` deleted (absorbed into skills)

### M2 (working observe/orient)
- 2026-03-16: Flat `.oodaloop/` paths, no nested directories
- 2026-03-16: Commands slimmed to thin skill invocations
- 2026-03-16: License changed to UNLICENSED (internal/private)
- 2026-03-16: Plugin configured for local loading during development

### M2.5 (state architecture revision)
- 2026-03-16: RESCOPE from conventions-only plan to full state architecture revision
- 2026-03-16: Two file types: CONTEXT.md (persistent) + `<slug>.task.md` (ephemeral)
- 2026-03-16: Old 5-file model (STATE/PROJECT/PLAN/SUMMARY/VERIFICATION) replaced
- 2026-03-16: Conventions absorbed as section in CONTEXT.md, not standalone file
- 2026-03-16: Multi-task support via per-task file isolation
- 2026-03-16: Self-bootstrapping mandatory -- plugin must build itself
- 2026-03-16: All 7 skills + status command + 3 agents + 1 rule + ARCHITECTURE.md updated to new model
- 2026-03-16: Self-migration completed -- own `.oodaloop/` now uses new model (first successful bootstrap cycle)

### M3.1 (adapter architecture)
- 2026-03-17: Skills already portable via Agent Skills standard (SKILL.md) -- no changes needed
- 2026-03-17: Adapter layer maps 5 surfaces per host: commands, skills, agents, rules, manifest
- 2026-03-17: install.sh detects host (Cursor, Claude Code, OpenCode) and applies matching adapter
- 2026-03-17: Init skill enhanced to detect and record host environment in CONTEXT.md
- 2026-03-17: Adapters are install docs + symlink setup, not behavioral forks

## Deconfliction
- `superpowers`: disabled at workspace level
- `continual-learning`: enabled, deprioritized
- `create-plugin`: enabled (quality gates useful)
- `team-kit`: enabled (selective)
