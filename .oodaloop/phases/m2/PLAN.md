# M2 Plan: Working Observe/Orient

## Tasks

### T1: Standardize file paths to flat structure
**Depends on**: none
**Acceptance**: All commands, skills, and ARCHITECTURE.md reference `.oodaloop/PLAN.md`, `.oodaloop/SUMMARY.md`, `.oodaloop/VERIFICATION.md` (flat). No `phases/<phase>/` references remain. ARCHITECTURE.md State Management section updated.

### T2: Slim commands to thin skill invocations
**Depends on**: none
**Acceptance**: Each command file contains only frontmatter + a one-line skill invocation (or self-contained logic for `status`). No workflow/inputs/outputs sections duplicating skill content. `init` and `quick` commands also slimmed.

### T3: Enrich init skill
**Depends on**: T1
**Acceptance**: Init skill has precise, numbered steps that an AI agent can follow without ambiguity. Covers: check for existing `.oodaloop/`, create directory, write STATE.md with project name and current date substituted, write PROJECT.md with project name substituted, confirm. Specifies that template content is written inline (no file copy from plugin directory needed).

### T4: Enrich observe skill
**Depends on**: T1, T3
**Acceptance**: Observe skill has a structured research procedure with: (a) what to look for (codebase structure, existing docs, dependencies, patterns, risks), (b) how to organize findings (requirements, constraints, observations sections in PROJECT.md), (c) when observations are sufficient (all scope questions answered or explicitly marked uncertain), (d) how to update STATE.md. An AI agent following the skill against a real project produces a populated PROJECT.md.

### T5: Enrich orient skill
**Depends on**: T1, T4
**Acceptance**: Orient skill specifies the exact PLAN.md format: task ID, description, dependencies, acceptance criteria, parallelism annotations. Describes the decomposition procedure: read PROJECT.md, identify work streams, break into atomic tasks, sequence by dependency, annotate parallelism. An AI agent following the skill produces a structured PLAN.md.

### T6: Enrich status command
**Depends on**: T1
**Acceptance**: Status command is self-contained (no skill reference) and has enough procedural detail to read `.oodaloop/` files and emit a structured report: current phase, task counts, recent decisions, blockers.

### T7: Update ARCHITECTURE.md
**Depends on**: T1, T2
**Acceptance**: Bootstrap lifecycle table updated (START.md deleted). Deconfliction table updated (superpowers disabled). M1 status marked complete. State Management section reflects flat paths. Plugin Structure section reflects current file tree.

### T8: Symlink and integration test
**Depends on**: T3, T4, T5, T6, T7
**Acceptance**: Plugin symlinked to `~/.cursor/plugins/local/oodaloop/`. Commands appear in Cursor. `/oodaloop-init` creates `.oodaloop/` successfully on a test target. Structural validation passes (all manifest paths resolve, frontmatter present).

## Dependency Graph

```
T1 ──┬── T2 ──── T7 ──┐
     ├── T3 ── T4 ── T5 ──┤── T8
     └── T6 ──────────────┘
```

## Parallelism

- **Parallel batch 1**: T1, T2 (independent)
- **Sequential after T1**: T3 → T4 → T5 (each builds on prior)
- **Parallel with T3-T5**: T6 (independent after T1)
- **Sequential after T2+T1**: T7
- **Final**: T8 (depends on all)

## Execution Strategy

Batch 1: T1 + T2 (parallel)
Batch 2: T3 + T6 + T7 (T3 sequential from T1, T6/T7 parallel)
Batch 3: T4
Batch 4: T5
Batch 5: T8 (integration test)
