# Backlog

Items discovered during OODA cycles, user conversations, and execution. Curated by loop phase.

## Next
Prioritized, ready to cycle into.

- **subcycle-live-test**: Run a real OODALOOP cycle on a target project (e.g., extracting status command into a skill) to validate checkpoint assessor fires, discovery classification works, and sub-cycle trigger path is reachable. [2026-03-19]

## Later
Valuable, not urgent. Promote to Next when dependencies clear or priority shifts.

- **start-resumable-detection**: `/oodaloop-start` should detect `resumable` tasks (from sync) and offer to resume them directly, not just report them. Currently relies on sync surfacing the Ready to Resume section. [2026-03-19]
- **strategy-auto-selection**: Heuristics for automatically choosing between subagent/new-chat/in-chat based on blocker complexity, context window usage, and chain depth. Currently defaults to subagent with user confirmation. [2026-03-19]
- **multitask-coordination**: Priority and conflict resolution when multiple task files touch the same files or compete for resources. [2026-03-16]
- **agent-tuning**: Evidence-based model selection per agent after enough real cycles to generate data. [2026-03-16]

## Done
- **subcycle-redesign**: Mandatory per-task checkpoint with readonly assessor, three execution strategies (subagent/new-chat/in-chat), enhanced Paused section for cold-start, CODE-DESIGN.md for design review, 6 new recovery checks. 8 files, 1 new. [done 2026-03-19]
- **adaptive-principle-injection**: Implemented selective injection of compressed doctrine for non-trivial OODA commands via `foundation/PRINCIPLES-COMPRESSED.md`, with runtime smoke validation for `/oodaloop-observe` and `/oodaloop-quick`. [done 2026-03-18]
- **state-sync**: Added `/oodaloop-sync` + `sync` skill to reconcile state after interruptions. Includes targeted convention drift refresh, unambiguous task metadata repairs, and done/ready/blocked status reporting without deleting task files. [done 2026-03-18]
- **nested-sub-cycles**: Arbitrary-depth sub-cycles. Existing implementation was already generic; added depth check (>3 asks user), chain tree in status, cycle/depth detection in state-hygiene. 4 touchpoints. [done 2026-03-17]
- **proof-of-work**: Proof-of-work architecture. Evidence contract rewritten with 4-tier hierarchy, surface-to-user mandate, counterfactual reasoning, anti-cowardice, honesty mandate. 7 touchpoints: evidence-contract, executor, decide, act, orient, loop, sentinel. 7 independent catches. [done 2026-03-17]
- **test-rigor**: Defense-in-depth fix for test avoidance. 5 touchpoints updated: evidence-contract, executor, decide, orient, act. Triggered by real autotracing failure. [done 2026-03-17]
- **skill-followability-audit**: Audited all 7 skills. Fixed loop Step 4 (durable knowledge criteria) and act Step 2 (no-automated-checks fallback). [done 2026-03-17]
- **readme-update**: README updated with state model, self-bootstrapping, M3.5 milestone. [done 2026-03-17]
- **error-recovery**: Recovery section added to state-hygiene rule. Detection checks, reporting template, recovery options. [done 2026-03-17]
- **bootstrap-cleanup**: Files already deleted in prior session. No work needed. [done 2026-03-17]
- **convention-drift**: Observe Step 2 rewritten with sentinel file table and concrete detection logic. [done 2026-03-17]
- **end-to-end-validation**: Skipped -- user validated through real usage on autotracing. [done 2026-03-17]
- **recursive-tasks**: Pause/resume sub-cycles for blocking discoveries. Extended decide, observe, loop, state-hygiene. Zero new file types or skills. [done 2026-03-17]
- **state-arch-revision**: Replaced 5-file mixed model with CONTEXT.md + task files. [done 2026-03-16]
- **adapter-architecture**: Adapter layer for Cursor/Claude Code/OpenCode portability. [done 2026-03-17]
