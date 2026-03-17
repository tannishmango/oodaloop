# Backlog

Items discovered during OODA cycles, user conversations, and execution. Curated by loop phase.

## Next
Prioritized, ready to cycle into.

- **recursive-tasks**: Mid-execution discovery handling -- when execution reveals blocking issues or improvement opportunities, assess inline (trivial), defer to backlog (notable), or spawn a sub-cycle (blocking). Needs decide skill changes, task file parent/child references, loop resumption logic. Subagents as execution mechanism. [2026-03-17]
- **end-to-end-validation**: Run full OODA cycle on autotracing with a real task. First complete validation of all phases working together. [2026-03-16]
- **convention-drift**: Make observe skill's drift detection concrete -- specify mechanism (git status, file existence, timestamp comparison) so agents follow it reliably. [2026-03-16]

## Later
Valuable, not urgent. Promote to Next when dependencies clear or priority shifts.

- **bootstrap-cleanup**: Absorb PROMPT.md, PLUGIN-AUDIT.md, DECONFLICTION-CHECKLIST.md into durable artifacts, delete originals. [2026-03-16]
- **error-recovery**: Define failure mode handling for each phase -- what happens when observe fails mid-way, task files corrupt, CONTEXT.md contradicts disk state. [2026-03-16]
- **multitask-coordination**: Priority and conflict resolution when multiple task files touch the same files or compete for resources. [2026-03-16]
- **auto-refresh**: Signal-based CONTEXT.md refresh heuristics beyond manual drift check in observe. [2026-03-16]
- **readme-update**: Update README for new state model and self-bootstrapping story. [2026-03-16]
- **agent-tuning**: Evidence-based model selection per agent after enough real cycles to generate data. [2026-03-16]

## Done
- **state-arch-revision**: Replaced 5-file mixed model with CONTEXT.md + task files. [done 2026-03-16]
- **adapter-architecture**: Adapter layer for Cursor/Claude Code/OpenCode portability. [done 2026-03-17]
