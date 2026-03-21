# Changelog

All notable changes to OODALOOP are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed
- Foundation doctrine loading (`PRINCIPLES-COMPRESSED.md`, `CODE-DESIGN.md`) moved from commands to skills — commands used bare `foundation/` paths that resolved against workspace root instead of plugin directory, causing agents in other repos to fail finding the files
- Added `Plugin paths` resolution note to all 5 phase skills and assessor agent so agents can derive plugin root from skill `fullPath`

### Added
- `agents/assessor.md`: dual-mode assessment agent (verify per-task in act, assess aggregate in loop), merged from verifier + sentinel
- Boyd-canonical one-liner anchoring in all 5 phase skills, referencing `foundation/OODALOOP.md`
- Interactive engagement checkpoints in observe skill (3 structural pause points with adaptive compression)
- Full proof audit procedure absorbed into observe from sync
- `foundation/CODE-DESIGN.md`: concrete, assessable code design principles for the assess checkpoint
- Mandatory readonly checkpoint subagent after every task in decide (execute-assess-repeat loop)
- Three sub-cycle execution strategies: `subagent` (default), `new-chat`, `in-chat`
- Subagent orchestration pattern for child OODA cycles via Cursor Task tool
- Enhanced Paused section format with 8 fields for cold-start resumption
- `Ready to Resume` section for cross-conversation parent resumption
- 6 new state-hygiene recovery checks for sub-cycle failure modes
- `resumable` task status in sync for completed child cycles
- Explicit orient precondition recovery when observe output was not persisted to a task file

### Changed
- README tightened around composable recursive OODA framing
- Phase alignment corrected to Boyd's canonical OODA Loop: Orient = analysis/synthesis, Decide = planning, Act = execution, Loop = verification + aggregate assessment
- Orient skill rewritten as cognitive engine — analysis, synthesis, situational assessment (was: planning)
- Decide skill rewritten as planning phase — absorbs decomposition logic from old orient (was: execution)
- Act skill rewritten as execution + Type 1 checkpoint — absorbs execution loop, blocker handling, sub-cycle management from old decide (was: verification)
- Loop skill dispatches assessor in assess mode (was: sentinel), adds aggregate verification scope
- Observe skill gains facts-only framing, phase transition to orient, proof audit ownership
- Sync skill simplified to pure state reconciliation + staleness detection (sheds scanning and proof audit)
- Init skill reframes convention scanning as researcher dispatch
- Researcher agent expanded with analytical synthesis capability for orient phase
- 5 command descriptions updated to match new phase definitions
- Rules updated: evidence-contract phase names, state-hygiene phase-section mapping and parent resumption references
- ARCHITECTURE.md and README.md updated: phase tables, agent tables, counts, all descriptions aligned
- Observe now persists task state earlier and incrementally (skeleton at step 4, then requirements/observations/scope updates before checkpoints)
- Install and sync scripts now reassert `core.hooksPath=.githooks` so pre-commit enforcement (including changelog and sync checks) self-heals on local drift

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
