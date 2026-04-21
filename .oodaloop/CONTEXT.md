# Context: oodaloop

> Last refreshed: 2026-04-21 (I-1: cycle log + state-hygiene validators)

## Objective
Build OODALOOP into a functional plugin that orchestrates project delivery using an adaptive OODA loop. The plugin builds itself -- each milestone improves the tooling used to execute the next milestone.

## Conventions

### Git
Standard git workflow. No branch protection. Commit messages are descriptive, imperative mood. No `.gitattributes`. No `CONTRIBUTING.md`.

### Code Quality
Pre-commit hook at `.githooks/pre-commit` enforces: sync to local Cursor install, blocks committing ephemeral `.oodaloop/*.task.md` files, validates command→skill linkage, blocks deprecated naming, requires `CHANGELOG.md` in staged files (bypass with `SKIP_CHANGELOG=1`), validates `tests/fixtures/state-hygiene/*.task.md` for Mode vocabulary, Paused completeness, phase↔section pairing, and Parent depth/DAG (block #6). No linters or formatters (plugin is pure markdown/declarative).

### Testing
No automated test framework. Plugin is tested by running commands against target projects (e.g., `/oodaloop-init` on `autotracing` repo). Structural validation via file existence checks. State-hygiene validator fixtures live at `tests/fixtures/state-hygiene/`; invoked via `SKIP_CHANGELOG=1 git add <fixture> && .githooks/pre-commit` (see README in that directory).

### CI/CD
None detected. No `.github/workflows/`, no CI pipeline.

### Dependencies
None. Pure markdown plugin with no package manager, no lockfiles, no runtime dependencies.

### Workspace Tooling
This plugin has commands, skills, agents, rules, and templates, and supports local plugin loading for development.

## Architecture
Plugin follows commands → skills → agents pattern. Commands are thin wrappers invoking skills. Skills contain procedural logic. Agents define roles with readonly constraints (only executor writes). Doctrine lives in `foundation/` (PRINCIPLES.md, PRINCIPLES-COMPRESSED.md, SYSTEMS-REFERENCE.md, CODE-DESIGN.md). State lives in `.oodaloop/` using CONTEXT.md (persistent) + BACKLOG.md (persistent) + task files (ephemeral). Task files support pause/resume for recursive sub-cycles via Parent/Paused metadata. `CHANGELOG.md` tracks releases. `.oodaloop/CYCLES.log` is an append-only self-observation signal written by `loop/SKILL.md` Step 6 (gitignored; one line per verdict). Structural validation lives in `tests/fixtures/state-hygiene/` (enforced by pre-commit block #6).

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

### M3 (full loop)
- 2026-03-17: BACKLOG.md added as third persistent file type (what SHOULD BE). Updated decide, loop, init, status, state-hygiene, ARCHITECTURE.md.
- 2026-03-17: Decide skill gains mid-execution discovery assessment (trivial/notable/blocking triage)

### M3.1 (adapter architecture)
- 2026-03-17: Skills already portable via Agent Skills standard (SKILL.md) -- no changes needed
- 2026-03-17: Adapter layer maps 5 surfaces per host: commands, skills, agents, rules, manifest
- 2026-03-17: install.sh detects host (Cursor, Claude Code, OpenCode) and applies matching adapter
- 2026-03-17: Init skill enhanced to detect and record host environment in CONTEXT.md
- 2026-03-17: Adapters are install docs + symlink setup, not behavioral forks

### M3.2 (recursive sub-cycles)
- 2026-03-17: Blocking discoveries during decide trigger sub-cycle spawning. Small blockers → quick path (no pause). Complex blockers → pause parent, spawn child task with Parent reference.
- 2026-03-17: `paused` added as valid task file phase. Parent/child convention: child has `Parent: <slug>`, parent has `Paused` section.
- 2026-03-17: Loop skill un-pauses parent after child completes (CONTINUE verdict), recommends resuming parent at decide.
- 2026-03-17: Zero new file types, skills, or agents. Extended existing decide, observe, loop skills and state-hygiene rule.
- 2026-03-17: Backlog description was over-specified -- delivered with less machinery than prescribed. Principle: minimum effective process.

### M3.3 (convention drift detection)
- 2026-03-17: Observe Step 2 rewritten with concrete sentinel file table (6 categories) and 4-step detection logic.
- 2026-03-17: Drift detection uses file existence as primary signal -- no timestamps, no content diffing. Comparison against CONTEXT.md text.
- 2026-03-17: Only drifted categories re-scanned. No-change categories skipped entirely.

### M3.4 (error recovery)
- 2026-03-17: Recovery section added to state-hygiene rule (always-apply). 9 detection checks, 3-part reporting template, 4 recovery options.
- 2026-03-17: Approach: detect and report to user, not automatic repair. Follows "deference to expertise" -- human decides recovery path.
- 2026-03-17: Single touchpoint (state-hygiene rule) covers all skills. Zero per-skill modifications.

### M3.5 (readme update)
- 2026-03-17: README updated with state model section, self-bootstrapping section, current milestone (M3.4→M3.5), updated phase descriptions.

### M3.6 (skill followability audit)
- 2026-03-17: Audited all 7 skills. Most steps are concrete. Two fixes: loop Step 4 "durable knowledge" given concrete criteria, examples, and litmus test. Act Step 2 given branching logic for verification with/without automated checks.

### M3.7 (test rigor)
- 2026-03-17: Triggered by real failure: agent in autotracing wrote unit tests but avoided integration tests for API ingestion work. Root cause: five touchpoints lacked test-type awareness.
- 2026-03-17: Evidence contract gains two rules: evidence type must match claim risk, and never silently substitute easy tests for hard ones.
- 2026-03-17: Executor agent gains constraint: substituting unit for integration tests without user consent is a violation.
- 2026-03-17: Decide gains testing-during-implementation instruction (not deferred to act).
- 2026-03-17: Orient gains test-type in acceptance criteria for integration work.
- 2026-03-17: Act gains test-type adequacy check -- unit tests alone flagged as gap for integration claims.
- 2026-03-17: Defense in depth: 5 independent catches across the OODA cycle.

### M3.8 (proof of work)
- 2026-03-17: Root problem: agents narrate but don't demonstrate. Evidence was described, not shown. Users had no way to judge sufficiency.
- 2026-03-17: Evidence contract rewritten as proof-of-work contract. Defines 4-tier proof hierarchy (raw output > independent reproduction > structured inspection > narrative). Lower tiers are fallbacks, not preferences.
- 2026-03-17: Surface-to-user mandate: evidence must reach the human in conversation, not just the task file. User judges sufficiency.
- 2026-03-17: Counterfactual/steelman reasoning required for non-trivial decisions: pre-mortem, steelman of rejected alternatives, falsifiability of verdicts.
- 2026-03-17: Anti-cowardice clause: must confront hardest available test. Choosing easy over hard is a named violation.
- 2026-03-17: Honesty mandate: silent omission is the primary epistemic crime.
- 2026-03-17: Orient gains pre-mortem and steelman step (step 6). Plans must confront their own failure modes.
- 2026-03-17: Act rewritten for independent verification -- verifier reproduces evidence, does not rubber-stamp executor self-reports.
- 2026-03-17: Loop verdicts require proof references and falsifiability statements.
- 2026-03-17: Sentinel gains proof-scrutiny constraint -- rejects narrative-only evidence for non-trivial claims.
- 2026-03-17: Execution log and verification templates changed from `**Evidence**` to `**Proof**` with raw-output requirement.
- 2026-03-17: 7 independent catches across the OODA cycle (up from 5 in M3.7).

### M3.9 (nested sub-cycles)
- 2026-03-17: Existing Parent/child implementation already generic -- handles arbitrary depth without code changes to core logic.
- 2026-03-17: Decide gains depth check: count chain depth before spawning, ask user if > 3 levels deep.
- 2026-03-17: Status command shows parent-child chains as tree with depth indicator.
- 2026-03-17: State-hygiene gains two chain-specific detection checks: circular Parent references and depth > 3 without consent.
- 2026-03-17: ARCHITECTURE.md phase flow updated with arbitrary-depth diagram and task file section updated.
- 2026-03-17: 4 touchpoints updated: decide, status, state-hygiene, ARCHITECTURE.md. Zero new files.

### M3.10 (state sync command)
- 2026-03-18: Added `/oodaloop-sync` command + `sync` skill for interruption recovery and state reconciliation.
- 2026-03-18: Sync flow refreshes convention drift, repairs unambiguous metadata inconsistencies, and reports done/ready/blocked task status.
- 2026-03-18: Sync is non-destructive for task lifecycle; deletion remains owned by `/oodaloop-loop`.
- 2026-03-18: Plugin structure now 9 commands and 8 skills.

### M3.11 (adaptive doctrine injection)
- 2026-03-18: Added `foundation/PRINCIPLES-COMPRESSED.md` as a high-signal doctrine layer derived from canonical principles.
- 2026-03-18: Command-layer selective doctrine injection added to non-trivial OODA commands (`observe`, `orient`, `decide`, `act`, `loop`) with explicit trivial-path guardrails.
- 2026-03-18: Quick/init/status paths intentionally remain lean; no always-on doctrine rule added.
- 2026-03-21: Doctrine injection moved from commands to skills. Commands used bare `foundation/` paths that resolved against the workspace, not the plugin directory — agents in other repos couldn't find the files. Skills have `fullPath` context, so path resolution works. Commands are now thin dispatch wrappers again. Plugin paths note added to all 5 phase skills and assessor agent.

### M3.14 (subcycle redesign)
- 2026-03-19: Decide skill rewritten with mandatory per-task readonly checkpoint (execute-assess-repeat). Checkpoint dispatches subagent with 6-point assessment: acceptance, discovery review, plan validity, design review (against CODE-DESIGN.md), goal alignment, evidence.
- 2026-03-19: Three sub-cycle execution strategies: `subagent` (default, Task tool orchestration), `new-chat` (cold-start via Paused section), `in-chat` (inline). Subagent strategy uses 8-step phase-by-phase dispatch with task file as coordination layer.
- 2026-03-19: Enhanced Paused section format with 8 fields for cold-start resumption. Parent/child file lifecycle differs by strategy.
- 2026-03-19: `foundation/CODE-DESIGN.md` added: concrete code design principles with structural thresholds, composition criteria, and red flag table. Injected into checkpoint assessor.
- 2026-03-19: Executor agent gains structured discovery output (4-category classification feeding checkpoint).
- 2026-03-19: Loop skill handles per-strategy resumption. New-chat writes `Ready to Resume` section; sync detects and reports it.
- 2026-03-19: State-hygiene gains 6 new recovery checks for sub-cycle failure modes (stale subagent, dispatch failure, checkpoint ignored, conflicting Ready to Resume/Paused).
- 2026-03-19: 8 files touched, 1 new file, zero new commands/skills/agents. README rewritten.

### Phase alignment
- 2026-03-19: Phase alignment corrected to match Boyd's OODA Loop. Orient = analysis/synthesis, Decide = planning, Act = execution, Loop = verification + aggregate assessment. Root cause: Orient had been reduced from Boyd's cognitive engine to a planning activity, shifting every downstream phase forward by one position.
- 2026-03-19: Agents reduced from 5 to 4. Verifier + sentinel merged into assessor (dual-mode: verify per-task in act, assess aggregate in loop). Researcher expanded with analytical synthesis capability for orient.
- 2026-03-19: Scanning consolidated. Sync sheds convention scanning and proof auditing (now pure state reconciliation + staleness detection). Observe owns active-cycle scanning. Init dispatches researcher for bootstrap.
- 2026-03-19: Each phase skill anchored with Boyd-canonical one-liner referencing foundation/OODALOOP.md.

### I-1 (cycle log + state-hygiene validators)
- 2026-04-21: `loop/SKILL.md` Step 6 appends one line per verdict to `.oodaloop/CYCLES.log` (gitignored). Field semantics: depth=Parent chain hops, subloops=distinct Child-slug values, tasks=T<n> headings in Plan, refines/rescopes=prior verdict markers. `?` for any unrecoverable field.
- 2026-04-21: Pre-commit block #6 validates staged `tests/fixtures/state-hygiene/*.task.md`: Mode vocabulary (direct|delegated), Paused 8-field completeness, phase↔section pairing, Parent DAG/depth (>3 without Depth-consent: marker = violation). Depth threshold is `depth > 3` (i.e., 5+ file chains require consent).
- 2026-04-21: `tests/` directory added (never before committed). Commit must include `git add tests/`.
- 2026-04-21: `docs/` directory now tracked (IMPROVEMENTS.md). Commit must include `git add docs/`.
- 2026-04-21: Mechanism precedent established: binding contracts enforced by build (pre-commit), not agent prose. Future contract additions default to mechanism unless judgment-only.

## Deconfliction
- `superpowers`: disabled at workspace level
- `continual-learning`: enabled, deprioritized
- `create-plugin`: enabled (quality gates useful)
- `team-kit`: enabled (selective)
