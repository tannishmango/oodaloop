# Changelog

All notable changes to OODALOOP are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `foundation/CODE-DESIGN.md`: concrete, assessable code design principles for the assess checkpoint
- Mandatory readonly checkpoint subagent after every task in decide (execute-assess-repeat loop)
- Three sub-cycle execution strategies: `subagent` (default), `new-chat`, `in-chat`
- Subagent orchestration pattern for child OODA cycles via Cursor Task tool
- Enhanced Paused section format with 8 fields for cold-start resumption
- `Ready to Resume` section for cross-conversation parent resumption
- 6 new state-hygiene recovery checks for sub-cycle failure modes
- `resumable` task status in sync for completed child cycles
- README rewrite with recursive sub-cycles and sentinel rescoping sections

### Changed
- Decide skill rewritten: per-task checkpoints replace per-batch pauses, design review in assessments
- Executor agent gains structured discovery output (4-category classification)
- Observe skill reads parent Paused section for child task cold-start bootstrapping
- Loop skill handles per-strategy parent resumption (subagent retains file, new-chat writes Ready to Resume)
- Sync skill detects Ready to Resume sections and reports resumable tasks

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
