# OODALOOP Architecture

## Purpose

OODALOOP orchestrates project delivery using an OODA-style loop: Observe, Orient, Decide, Act, Loop. It uses atomic tasking, context isolation, file-based state, and verification while dropping ceremony that does not improve outcomes.

---

## Design Transfer Analysis

### Transfers directly
- **Atomic task decomposition**: tasks are single-concern, dependency-ordered, with acceptance criteria.
- **Context isolation**: each agent (researcher, planner, executor, verifier, sentinel) operates within a focused scope.
- **File-based shared state**: `.oodaloop/` directory is the single source of truth for project state.
- **Verification before closure**: Act phase requires evidence-backed acceptance checks before progressing.

### Platform adaptations
- **Slash commands as entrypoints**: `commands/*.md` with frontmatter.
- **Planner/executor handoff via specialized agents**: role separation uses agent definitions with `readonly` constraints.
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
                              ↑               ↓
                   (resume)   |   CONTINUE → next task / resume parent
                              |   REFINE  → adjust plan, re-enter decide
                              |   RESCOPE → re-enter observe
                              |
               blocking discovery during decide:
               small  → /oodaloop-quick → resume inline
               complex → pause parent → observe child → ... → loop child
                                                                ↓
                                              CONTINUE → delete child, resume parent
```

The quick path (`/oodaloop-quick`) short-circuits this for low-risk, local changes: execute, summarize, update state. It also resolves small blocking discoveries during execution without pausing the parent task.

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

Project state lives in `.oodaloop/` within the target project. Three file types:

```
.oodaloop/
  CONTEXT.md             ← persistent: what IS (repo state, survives across tasks)
  BACKLOG.md             ← persistent: what SHOULD BE (future work, survives across conversations)
  <slug>.task.md          ← ephemeral: what's HAPPENING (one per active OODA cycle)
```

### CONTEXT.md (persistent -- repo state)

One file holds everything that survives across tasks: project identity, repo conventions (6 categories: git, code quality, testing, CI/CD, dependencies, workspace tooling), architecture patterns, active decisions, and plugin deconfliction.

- Created by `/oodaloop-init` with automated convention scan.
- Enriched by observe (convention drift check) and loop (learning absorption).
- Updated incrementally -- sections change, file is never rewritten wholesale.
- "Last refreshed" timestamp enables targeted staleness detection.

### BACKLOG.md (persistent -- future work)

Tracks roadmap items, deferred work, discovered improvements, and ideas across conversations. Prevents roadmap loss when conversations end.

- Three tiers: **Next** (prioritized, ready), **Later** (valuable, not urgent), **Done** (completed, pruned periodically).
- Updated by loop (discoveries, promotions, completions) and decide (mid-execution notable discoveries).
- Read when choosing next work or when loop recommends next steps. NOT read during every phase -- stays out of hot context.
- Curated, not accumulated. Stale items pruned by loop.

### Task files (ephemeral)

Each OODA cycle creates one `<slug>.task.md` file. It contains the full lifecycle: phase tracking, objective, requirements, observations, scope, plan, execution log, verification, and verdict. All in one file per task.

- Created by observe, filled through orient/decide/act/loop.
- On CONTINUE verdict, learnings are absorbed into CONTEXT.md, backlog updated, and the task file is **deleted**. If the completed task has a `Parent:` field, its parent task is un-paused and resumes at decide.
- Multiple task files can coexist for concurrent work. Each is independent.
- A task can be `paused` when a blocking discovery requires a sub-cycle. The parent task file records what it's waiting for. The child task file references its parent. This enables recursive depth without new file types or skills.

### Design rationale
- **Three types, clean separation**: CONTEXT.md = what IS, BACKLOG.md = what SHOULD BE, task files = what's HAPPENING. Each concept has one home.
- **Flat structure**: everything lives at `.oodaloop/` root. No nested directories.
- **Multi-task ready**: task files are per-cycle, not singleton. `ls .oodaloop/*.task.md` shows all active work.
- **Anti-stale by design**: CONTEXT.md uses targeted refresh. Task files are ephemeral. BACKLOG.md curated by loop.
- **Context hygiene**: BACKLOG.md is NOT part of hot context. Only CONTEXT.md is read every phase. Backlog is referenced on-demand.

---

## Bootstrap Artifact Lifecycle

Legacy bootstrap artifacts were fully absorbed into durable skills, rules, and architecture docs, then deleted.

---

## Deconfliction Status

### Active decisions (milestone 1)

| Plugin | Decision | Rationale |
|--------|----------|-----------|
| `superpowers` | Disabled at workspace level | Session hook was injecting mandatory context. Removed to eliminate interference. |
| `continual-learning` | Keep enabled, deprioritized | Low interference for structural work. |
| `create-plugin` | Keep enabled | `plugin-quality-gates` rule directly supports correctness. |
| `team-kit` | Keep enabled (selective) | Code-quality rules are non-conflicting. |
| `database-skills` | Ignore during plugin work | Domain-specific, no interference. |

### Precedence rule

When behavior conflicts occur between OODALOOP and external plugins, **OODALOOP contracts win** within the plugin scope. External plugin behaviors are treated as advisory, not mandatory.

### Absorbed patterns

From external plugins, these patterns are absorbed into OODALOOP (without runtime dependency):
- Debugging discipline and verification-before-completion checks (from `superpowers`)
- Parallel task decomposition heuristics (from `superpowers`)
- Manifest/path/frontmatter quality gates (from `create-plugin`)
- Smoke-test and compiler-check workflows (from `team-kit`)

---

## Cross-Environment Portability

OODALOOP is host-agnostic. The core (skills, doctrine, state model, templates) works identically everywhere. Thin adapter layers map OODALOOP's components to each host's discovery paths.

### Portable layer (unchanged across hosts)
- **Skills** (`skills/*/SKILL.md`): Agent Skills open standard, supported by 27+ tools.
- **State** (`.oodaloop/`): CONTEXT.md + task files. Pure markdown, no host dependencies.
- **Doctrine** (`foundation/`): Principles and systems reference.
- **Templates** (`templates/`): State templates for target projects.

### Adapter layer (thin, per-host)
Each adapter maps five surfaces: commands (install path), skills (discovery path), agents (definition format), rules (file format), and manifest (if required). See `adapters/README.md` for the full capability matrix.

### Install
`install.sh` detects the host environment and applies the matching adapter. Manual setup is documented in `adapters/<host>/install.md`.

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
| M2: Working Observe/Orient | Functional research + planning pipeline, skill enrichment, local testing | Complete |
| M2.5: State Architecture | Persistent/ephemeral separation, CONTEXT.md + task files, multi-task design, convention memory | Complete |
| M3: Full Loop | End-to-end OODA cycle with sentinel verdicts and adaptive rigor in practice | Current |
| M3.1: Adapter Architecture | Cross-environment portability, install script, host detection, adapter layer | Current |

---

## Plugin Structure

```
oodaloop/
  .cursor-plugin/plugin.json    ← Cursor manifest (host-specific)
  .oodaloop/                    ← self-tracking state (committed)
  adapters/                     ← per-host install instructions and mappings
    cursor/
    claude-code/
    opencode/
  foundation/                   ← permanent doctrine
    PRINCIPLES.md
    SYSTEMS-REFERENCE.md
  commands/                     ← 8 thin command invocations (portable)
  skills/                       ← 7 procedural skills (portable, Agent Skills standard)
  agents/                       ← 5 specialized agents
  rules/                        ← 3 boundary rules
  templates/oodaloop/           ← 1 state template (CONTEXT.md)
  install.sh                    ← host-detecting install script
  ARCHITECTURE.md               ← this document
  README.md
  LICENSE
```

Commands are thin wrappers that invoke skills. Skills contain the actual procedure. The install script detects the host environment and places components where the host can discover them.
