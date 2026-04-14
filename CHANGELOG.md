# Changelog

All notable changes to OODALOOP are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [M4.7] - 2026-04-14

### Fixed
- Dotdir detection: skills and state-hygiene rule now instruct agents to read `.oodaloop/CONTEXT.md` directly instead of globbing `.oodaloop/**` (glob silently skips hidden directories, causing false "not found" in other projects)

## [M4.6] - 2026-03-24

### Changed
- `walkthrough.html`: mobile-friendly layout via extra breakpoints (wrapped sticky controls, wider diagram nodes and taller frames on small screens, touch-sized buttons, tighter section padding) while preserving desktop presentation

## [M4.5] - 2026-03-24

### Added
- `walkthrough.html`: interactive field-manual walkthrough for Observe→Loop — animated phase boards, SVG connector wires, sticky phase controls, Decide-phase atomic task DAG, Observe user-prompt scope strip, and copy tying labor strategy to reasoning-orchestrator versus fast subagent execution on atomic leaves (hero line from README scope-control doctrine)

## [M4.4] - 2026-03-23

### Changed
- Consolidated commit/push project skill guidance into `.cursor/skills/oodaloop-commit-push/` and removed the duplicate `commit-push` skill path.
- Renumbered assessor modes to reflect canonical decide→act→loop order: Type 1 = Plan Mode (Decide), Type 2 = Verify Mode (Act), Type 3 = Assess Mode (Loop); reordered sections in `agents/assessor.md` and updated all references in skills and changelog.

## [M4.3] - 2026-03-22

### Added
- `.cursor/skills/`: project-scoped skills (commit-push, release-cut, principles-curator) now tracked in repo; excluded from plugin install via `install.sh` allowlist

## [M4.2] - 2026-03-22

### Changed
- Agent dispatch governance: all assessor dispatches (decide Type 1, act Type 2, loop Type 3) and executor dispatch (act delegated) now pass the agent definition as governing specification with explicit prohibition on overriding spec vocabulary in dispatch prompts
- Assessor Plan Mode check 1: expanded from basic executability to scope quality evaluation — flags multiplicative work, deferred enumeration, combined concerns, and multi-file judgment as blocking plan quality issues
- Decide Step 3: added scope stress test (modification count per task, concrete enumeration of vague quantifiers, concern separation)
- Decide Step 7: added scope quality and enumeration checks to review gate; gate is now blocking — known defects must be fixed before proceeding to Step 8
- Decide Step 8: added mode vocabulary validation (reject non-`direct`/`delegated` values), re-dispatch loop on scope issues, assessor agent def passthrough; unresolved scope issues require task splits and re-dispatch before phase transition
- Act Step 1: missing labor strategy on >6-task plans now halts instead of silently defaulting to direct mode
- Act Step 3c: Type 2 assessor dispatch names valid output vocabulary (`proceed`/`blocker-detected`/`quality-concern`)
- Loop Step 2: replaced duplicated inline check descriptions with reference to assessor Type 3 spec (single source of truth)
- `rules/state-hygiene.mdc`: document that `.oodaloop/` lives at the workspace root; `rules/adaptive-rigor.mdc`: follow precondition-failure paths without improvising; `skills/orient/SKILL.md`: explicit STOP when no task file exists

## [M4.1] - 2026-03-22

### Added
- Risk gate in act phase blocker handling — three-dimensional evaluation (reversibility, containment, confidence) as prerequisite before scope classification
- Risk-gates-autonomy heuristic (#12) in PRINCIPLES-COMPRESSED.md
- Risk-aware failure-detection prompt and anti-pattern
- `rules/destructive-ops.mdc`: hard safety boundary requiring explicit user confirmation before any external state mutation (databases, Docker volumes, deployments, services). Always-apply, cannot be overridden by any skill or process level.
- Destructive operations gate in act skill Step 2a — executor must stop and confirm before running commands that mutate external state
- Destructive flag requirement in decide skill task decomposition — plans must tag tasks that touch external state with `**Destructive**: yes`
- Destructive operations check in quick skill — fast path still requires confirmation for external state mutations
- Executor agent safety constraint (first and highest-priority) — hard stop before database ops, Docker mutations, deployments, service calls

### Changed
- README: verdicts section clarifies handling sunk-cost situations vs claiming "nothing is sunk cost"
- Blocker scope classifications (trivial, blocking-small) now require low-risk qualification, not just low scope
- Executor constraint: workarounds to missing preconditions must pass risk evaluation before autonomous action
- `install.sh` now uses allowlist of plugin dirs, nukes target before reinstall, and bumps version for cache invalidation
- Pre-commit hook calls `./install.sh cursor` instead of removed `sync.sh`

### Fixed
- Foundation doctrine loading (`PRINCIPLES-COMPRESSED.md`, `CODE-DESIGN.md`) moved from commands to skills — commands used bare `foundation/` paths that resolved against workspace root instead of plugin directory, causing agents in other repos to fail finding the files
- Added `Plugin paths` resolution note to all 5 phase skills and assessor agent so agents can derive plugin root from skill `fullPath`

### Removed
- `sync.sh` — consolidated into `install.sh`; single script handles full reinstall with cache busting

## [M4.0] - 2026-03-21

### Added
- `agents/assessor.md`: tri-mode assessment agent (Type 1 plan evaluation in decide, Type 2 verify per-task in act, Type 3 assess aggregate in loop), merged from verifier + sentinel
- Assessor Type 1 (plan mode) — dispatched by decide after plan is written; evaluates executability, recommends labor strategy (direct vs delegated), flags under-scoped tasks for pre-scoping
- Plan assessor dispatch step in decide skill (Step 8) — writes Labor Strategy subsection into plan before phase transition
- Delegated execution mode in act skill — parent orchestrates parallel executor subagents per batch instead of sequential single-agent execution
- Pre-scoping flag handling in act skill (Step 2) — resolves under-scoped tasks via child OODA before execution begins
- Plan drift routing in act skill — new checkpoint outcome that halts execution, evaluates completed work, and loops back to decide for replanning
- Boyd-canonical one-liner anchoring in all 5 phase skills, referencing `foundation/OODALOOP.md`
- Interactive engagement checkpoints in observe skill (3 structural pause points with adaptive compression)
- Full proof audit procedure absorbed into observe from sync
- `foundation/CODE-DESIGN.md`: concrete, assessable code design principles for the assess checkpoint
- Three sub-cycle execution strategies: `subagent` (default), `new-chat`, `in-chat`
- Subagent orchestration pattern for child OODA cycles via Cursor Task tool
- Enhanced Paused section format with 8 fields for cold-start resumption
- `Ready to Resume` section for cross-conversation parent resumption
- 6 new state-hygiene recovery checks for sub-cycle failure modes
- `resumable` task status in sync for completed child cycles
- Explicit orient precondition recovery when observe output was not persisted to a task file

### Changed
- Phase alignment corrected to Boyd's canonical OODA Loop: Orient = analysis/synthesis, Decide = planning, Act = execution, Loop = verification + aggregate assessment
- Orient skill rewritten as cognitive engine — analysis, synthesis, situational assessment (was: planning)
- Decide skill rewritten as planning phase — absorbs decomposition logic from old orient (was: execution)
- Act skill rewritten as execution + Type 2 checkpoint — absorbs execution loop, blocker handling, sub-cycle management from old decide (was: verification)
- Loop skill dispatches assessor in assess mode (was: sentinel), adds aggregate verification scope
- Observe skill gains facts-only framing, phase transition to orient, proof audit ownership
- Sync skill simplified to pure state reconciliation + staleness detection (sheds scanning and proof audit)
- Init skill reframes convention scanning as researcher dispatch
- Researcher agent expanded with analytical synthesis capability for orient phase
- README tightened around composable recursive OODA framing
- 5 command descriptions updated to match new phase definitions
- Rules updated: evidence-contract phase names, state-hygiene phase-section mapping and parent resumption references
- ARCHITECTURE.md and README.md updated: phase tables, agent tables, counts, all descriptions aligned
- Observe now persists task state earlier and incrementally (skeleton at step 4, then requirements/observations/scope updates before checkpoints)
- Install and sync scripts now reassert `core.hooksPath=.githooks` so pre-commit enforcement self-heals on local drift

### Removed
- `agents/verifier.md` (absorbed into assessor)
- `agents/sentinel.md` (absorbed into assessor)

## [M3.13] - 2026-03-19

### Added
- Mandatory proof audit during sync
- Project skills and sandbox harness scanning in sync flow
- Bumped synced plugin version on sync to force Cursor cache invalidation

### Changed
- Strengthened proof posture and restartability doctrine
- Curated Unix/Systemantics principle additions to foundation

## [M3.11] - 2026-03-18

### Added
- Selective doctrine injection into target projects
- State sync flow (`/oodaloop-sync`) and startup refinements

### Changed
- Standardized `/oodaloop-start` kickoff naming across all surfaces
- Enforced pre-commit sync for local Cursor installs
- Updated branding assets

## [M3.9] - 2026-03-17

### Added
- Arbitrary-depth nested sub-cycles
- Proof-of-work architecture: demonstrate, don't describe
- Defense-in-depth for test avoidance (5 independent catches)
- Recursive sub-cycles with convention drift detection and error recovery
- BACKLOG.md for persistent roadmap tracking and mid-execution discovery triage

### Changed
- Improved followability of agent output

## [M3.1] - 2026-03-17

### Added
- Cross-environment adapter architecture with `install.sh`
- README install documentation
- Recursive impossible diamond logo (Escher-Bach geometry)

### Changed
- Generalized documentation and state language for platform-agnostic use

## [M2] - 2026-03-16

### Added
- Functional init, observe, and orient skills
- Plugin deconfliction scan in init skill
- `.oodaloop/` self-tracking bootstrap
- CONTEXT.md + task file state architecture

### Changed
- Replaced 5-file mixed state model with cleaner CONTEXT.md approach
- Renamed command files to match Cursor command names
- Refined plugin description with recursive OODA framing

### Fixed
- Author attribution in plugin metadata

## [M1] - 2026-03-16

### Added
- OODALOOP plugin scaffold and architecture baseline
- Initial skill, command, agent, rule, and template directory structure
