# OODALOOP Architecture

## Purpose

OODALOOP orchestrates project delivery in Cursor using an OODA-style loop: Observe, Orient, Decide, Act, Loop. It preserves what works from GSD (atomic tasks, context isolation, file-based state, verification) while adapting to Cursor's plugin primitives and dropping ceremony that doesn't improve outcomes.

---

## GSD Transfer Analysis

### Transfers directly
- **Atomic task decomposition**: tasks are single-concern, dependency-ordered, with acceptance criteria.
- **Context isolation**: each agent (researcher, planner, executor, verifier, sentinel) operates within a focused scope.
- **File-based shared state**: `.oodaloop/` directory is the single source of truth for project state.
- **Verification before closure**: Act phase requires evidence-backed acceptance checks before progressing.

### Adapts for Cursor
- **Slash commands → Cursor commands**: GSD's terminal commands become `commands/*.md` with frontmatter.
- **Planner/executor handoff → Cursor agents**: role separation uses Cursor's agent definitions with `readonly` constraints.
- **Skills as procedural layer**: deeper "how" logic lives in `skills/*/SKILL.md`, referenced by commands.
- **Rules as boundary layer**: `rules/*.mdc` with `alwaysApply: true` enforce lightweight invariants.

### Drops
- **Terminal-centric internals**: no shell scripts, no `tmux` session management, no process supervision.
- **Unconditional heavyweight ceremony**: no mandatory design-approval gates for trivial tasks.
- **Rigid sequential flow**: adaptive rigor selects process depth based on task complexity.

---

## OODA Phase Design

| Phase | Command | Agent | Skill | Purpose |
|-------|---------|-------|-------|---------|
| Observe | `/oodaloop-observe` | researcher | observe | Research, requirements gathering |
| Orient | `/oodaloop-orient` | planner | orient | Plan decomposition, task sequencing |
| Decide | `/oodaloop-decide` | executor | decide | Implementation of atomic tasks |
| Act | `/oodaloop-act` | verifier | act | Acceptance checks, gap reporting |
| Loop | `/oodaloop-loop` | sentinel | loop | Scope reassessment, drift detection |

Supporting commands:
- `/oodaloop-init`: bootstrap `.oodaloop/` state in a target project.
- `/oodaloop-status`: read-only state report.
- `/oodaloop-quick`: fast path for trivial tasks, bypassing full ceremony.

### Phase flow

```
init → observe → orient → decide → act → loop
                                          ↓
                              CONTINUE → next task batch
                              REFINE  → adjust plan, re-enter decide
                              RESCOPE → re-enter observe
```

The quick path (`/oodaloop-quick`) short-circuits this for low-risk, local changes: execute, summarize, update state.

---

## Adaptive Rigor Model

Process depth is not uniform. It scales with task complexity and risk:

| Complexity | Flow | Ceremony |
|------------|------|----------|
| Trivial | `/oodaloop-quick` | Execute → summary → state update |
| Medium | Observe → Orient → Decide → Act | Plan + verify, no loop |
| Complex | Full OODA with Loop | Plan + verify + sentinel reassessment |

If a task escalates mid-execution (trivial becomes complex), the executor pauses and upgrades the process level. If process feels like overhead, reduce it. The rule `adaptive-rigor.mdc` enforces this.

---

## Agent Architecture

Four of five agents are `readonly: true`. Only the executor writes.

| Agent | Readonly | Model | Role |
|-------|----------|-------|------|
| researcher | true | fast | Codebase exploration, requirements discovery |
| planner | true | fast | Task decomposition, dependency analysis |
| executor | false | fast | Implementation of atomic tasks |
| verifier | true | fast | Acceptance checks, evidence collection |
| sentinel | true | fast | Scope reassessment, loop verdicts |

This enforces separation of concerns: read-heavy analysis is isolated from write operations. The executor is the only mutation surface, bounded to single-task scope.

---

## State Management

Project state lives in `.oodaloop/` within the target project:

```
.oodaloop/
  STATE.md          ← phase tracking, decisions, verdicts
  PROJECT.md        ← requirements, scope, constraints
  PLAN.md           ← created by orient skill
  SUMMARY.md        ← created by decide skill
  VERIFICATION.md   ← created by act skill
```

Design choices:
- **Flat structure**: all state files live at `.oodaloop/` root. No nested `phases/` directories. Simpler to reference, harder to go stale.
- **Two templates, five dynamic**: STATE.md and PROJECT.md are initialized by `/oodaloop-init`. PLAN.md, SUMMARY.md, and VERIFICATION.md are created by skills during execution.
- **Decisions log is a section in STATE.md**, not a separate file.

---

## Bootstrap Artifact Lifecycle

These files exist at the repo root during initial development:

| File | Status | Lifecycle |
|------|--------|-----------|
| `PROMPT.md` | Bootstrap | Hard input for plugin design. Archive or delete after v1 stable. |
| ~~`START.md`~~ | Deleted | Absorbed after M1. |
| `PLUGIN-AUDIT.md` | Bootstrap | Plugin interference findings. Collapse into this document's Deconfliction section after v1. |
| `DECONFLICTION-CHECKLIST.md` | Bootstrap | Build gates. Collapse into this document after v1. |

**Rule**: if a bootstrap file's content has been fully absorbed into a durable artifact, delete the bootstrap file.

---

## Deconfliction Status

### Active decisions (milestone 1)

| Plugin | Decision | Rationale |
|--------|----------|-----------|
| `superpowers` | Disabled at workspace level | Session hook was injecting mandatory context. Removed to eliminate interference. |
| `continual-learning` | Keep enabled, deprioritized | Low interference for structural work. |
| `create-plugin` | Keep enabled | `plugin-quality-gates` rule directly supports correctness. |
| `cursor-team-kit` | Keep enabled (selective) | Code-quality rules are non-conflicting. |
| `database-skills` | Ignore during plugin work | Domain-specific, no interference. |

### Precedence rule

When behavior conflicts occur between OODALOOP and external plugins, **OODALOOP contracts win** within the plugin scope. External plugin behaviors are treated as advisory, not mandatory.

### Absorbed patterns

From external plugins, these patterns are absorbed into OODALOOP (without runtime dependency):
- Debugging discipline and verification-before-completion checks (from `superpowers`)
- Parallel task decomposition heuristics (from `superpowers`)
- Manifest/path/frontmatter quality gates (from `create-plugin`)
- Smoke-test and compiler-check workflows (from `cursor-team-kit`)

---

## Anti-Patterns

Reject these explicitly:

1. **Process theater**: creating artifacts because frameworks expect them, not because they improve outcomes.
2. **Context bloat**: accumulating stale context instead of curating it.
3. **Duplicate state**: multiple files tracking the same information, drifting apart.
4. **Ceremony for ceremony's sake**: forcing heavyweight flow on trivial tasks.
5. **Overfitting to model weaknesses**: building mechanisms that will become redundant as models improve.
6. **Pass/fail verification with no learning**: "it passed" tells you nothing about why or what to improve.
7. **Optimizing busyness over bottlenecks**: local task speedups while global constraints remain.
8. **Automating bad process**: encoding ceremony that should have been deleted.

---

## Milestone Roadmap

| Milestone | Scope | Status |
|-----------|-------|--------|
| M1: Ground Breaking | Plugin scaffold, component skeletons, architecture baseline, doctrine home | Complete |
| M2: Working Observe/Orient | Functional research + planning pipeline with real agent orchestration | Current |
| M3: Full Loop | End-to-end OODA cycle with sentinel verdicts and adaptive rigor in practice | Future |

### M1 non-goals
- Full OODA orchestration logic
- Hook scripts or MCP servers
- Symlink to `~/.cursor/plugins/local/`
- Publishing or marketplace submission
- Sentinel loop verdict engine implementation
- Dynamic phase file creation (described in skills, not yet executable)

---

## Plugin Structure

```
oodaloop/
  .cursor-plugin/plugin.json    ← manifest
  .oodaloop/                    ← self-tracking state (committed)
  foundation/                   ← permanent doctrine
    PRINCIPLES.md
    SYSTEMS-REFERENCE.md
  commands/                     ← 8 thin command invocations
  skills/                       ← 7 procedural skills (the real substance)
  agents/                       ← 5 specialized agents
  rules/                        ← 3 boundary rules
  templates/oodaloop/           ← 2 state templates (reference only)
  ARCHITECTURE.md               ← this document
  README.md
  LICENSE
```

Commands are thin wrappers that invoke skills. Skills contain the actual procedure. This mirrors the pattern used by reference plugins (cursor-team-kit, superpowers).

All component paths in `plugin.json` are relative and resolve to existing directories.
