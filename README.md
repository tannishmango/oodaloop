# OODALOOP

**An OODA loop that observes itself observing.**

Orient, decide, act, and reorient -- recursively. OODALOOP orchestrates AI-assisted project delivery as a living cycle that adapts mid-flight, recurses when it hits blockers, and collapses ceremony when the task doesn't warrant it.

Most workflow frameworks bolt process onto work. They're rigid pipelines that force heavyweight ceremony on trivial tasks and have no answer when assumptions change mid-execution. OODALOOP inverts this: process depth is a function of task complexity, the cycle can nest inside itself, and a verification loop watches for the moment your plan stops matching reality.

---

## The Cycle

```
observe → orient → decide → act → loop
   ↑                                 │
   │         CONTINUE ───→ done      │
   │         REFINE  ───→ decide     │
   └──────── RESCOPE ───→ observe ───┘
```

| Phase | What happens |
|-------|--------------|
| **Observe** | Research the codebase, detect convention drift, gather requirements |
| **Orient** | Analyze observations, synthesize a situational assessment |
| **Decide** | Decompose into a dependency-ordered plan with acceptance criteria |
| **Act** | Execute atomic tasks, verify each with per-task checkpoint |
| **Loop** | Assess aggregate outcomes: continue, refine the plan, or rescope entirely |

Trivial work skips the ceremony. A one-line fix doesn't need a plan phase -- `/oodaloop-quick` handles it directly. Medium tasks run observe through act without a loop. Complex work gets the full cycle with aggregate reassessment. If a task escalates mid-execution, the process level upgrades with it.

---

## Recursive Sub-Cycles

This is where OODALOOP diverges from linear workflows.

During execution, you will discover things -- a dependency that's broken, an assumption that's wrong, a prerequisite that doesn't exist yet. Most frameworks tell you to file a ticket and keep going. OODALOOP handles it structurally:

**Small blocker?** Resolve it inline with `/oodaloop-quick`. No pause, no context switch.

**Complex blocker?** The parent task *pauses* and spawns a child OODA cycle. The child runs its own full observe → orient → decide → act → loop. When it completes, the parent automatically resumes where it left off.

```
Task A (building auth)
  └─ discovers missing DB migration
     └─ Task A pauses
        └─ Task B spawns (fix migration)
           └─ discovers schema conflict
              └─ Task B pauses
                 └─ Task C spawns (resolve schema)
                    └─ C completes → B resumes → B completes → A resumes
```

Chains resolve bottom-up. Each child references its parent. Depth beyond 3 levels requires explicit user consent. `/oodaloop-status` renders the full chain as a tree.

The recursion is the point. Work doesn't proceed in straight lines. The system that orchestrates it shouldn't pretend otherwise.

---

## Scope Reassessment

The loop phase isn't a rubber stamp. The assessor agent compares what actually happened against what was assumed and emits a verdict:

| Verdict | Meaning | What happens next |
|---------|---------|-------------------|
| **CONTINUE** | Scope held. Outcomes match criteria. | Absorb learnings, close the task, move on. |
| **REFINE** | Some tasks need adjustment, but the objective is sound. | Keep the task open, re-enter decide with an updated plan. |
| **RESCOPE** | Core assumptions changed. The plan is wrong. | Re-enter observe. Research again with new information. |

Every verdict includes proof references, rationale, confidence level, and a falsifiability statement -- not just a label. The assessor is readonly; it can only recommend, never modify.

This means OODALOOP doesn't just detect that something went wrong. It knows *where to re-enter the cycle* based on how wrong things went. A bad task gets refined. A bad premise gets rescoped from scratch.

Convention drift detection works the same way: observe and sync phases compare what's actually on disk against what CONTEXT.md claims across six categories (git, code quality, testing, CI/CD, dependencies, workspace tooling). Only drifted categories get rescanned.

---

## Commands

| Command | Purpose |
|---------|---------|
| `/oodaloop-start` | Entry point. Bootstraps state, syncs if needed, routes to the right flow. |
| `/oodaloop-quick` | Fast path for trivial tasks. No plan phase, no loop. |
| `/oodaloop-observe` | Research and requirements gathering |
| `/oodaloop-orient` | Analyze observations, form situational assessment |
| `/oodaloop-decide` | Plan decomposition and task sequencing |
| `/oodaloop-act` | Execute plan tasks, verify each with checkpoint |
| `/oodaloop-loop` | Assess aggregate outcomes, reassess scope |
| `/oodaloop-sync` | Reconcile state after interruptions or context resets |
| `/oodaloop-status` | Read-only state report with task tree |
| `/oodaloop-init` | Initialize `.oodaloop/` state in a target project |

Start with `/oodaloop-start`. It handles everything else.

---

## Agents

Four specialized agents, three of them readonly. Only the executor writes.

| Agent | Role | Writes? |
|-------|------|---------|
| **researcher** | Codebase exploration, requirements discovery, situational assessment | No |
| **planner** | Task decomposition, dependency analysis, pre-mortem | No |
| **executor** | Implementation of atomic tasks | Yes |
| **assessor** | Per-task verification, aggregate assessment, loop verdicts | No |

---

## State

All project state lives in `.oodaloop/` within the target project. Three file types, clean separation:

| File | What it tracks | Lifecycle |
|------|----------------|-----------|
| `CONTEXT.md` | What **is** -- repo identity, conventions, architecture, decisions | Persistent, incrementally updated |
| `BACKLOG.md` | What **should be** -- future work, deferred items, roadmap | Persistent, curated by loop |
| `<slug>.task.md` | What's **happening** -- one per active OODA cycle | Ephemeral, deleted on completion |

Multiple task files coexist for concurrent work. Paused parents and active children are separate files linked by a `Parent:` field. CONTEXT.md is the only file read every phase; BACKLOG.md stays out of hot context until explicitly needed.

---

## Install

```bash
git clone <repo-url> && cd oodaloop
./install.sh
```

The install script detects your environment and places components where the host can discover them:

```bash
./install.sh cursor       # Cursor IDE
./install.sh claude-code  # Claude Code
./install.sh opencode     # OpenCode
```

Then in any project: `/oodaloop-start`.

For local development, sync edits into Cursor's plugin directory:

```bash
./sync.sh
```

The pre-commit hook runs this automatically when a local Cursor install exists.

---

## Structure

```
.cursor-plugin/plugin.json   Cursor manifest
adapters/                    Per-host install mappings
foundation/                  Permanent doctrine (principles, systems reference)
commands/                    10 entry-point commands
skills/                      9 procedural skills (Agent Skills standard)
agents/                      4 specialized agents
rules/                       3 always-active boundary rules
templates/oodaloop/          CONTEXT.md template for target projects
install.sh                   Host-detecting installer
sync.sh                      Dev sync to Cursor local plugin directory
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for design details, portability model, and the full phase flow.

---

## Principles

OODALOOP is a learning-rate engine. Its advantage isn't writing code faster -- it's improving the quality of decisions per cycle while preserving reliability under uncertainty.

- **Adaptive rigor** -- process depth matches task complexity. No unconditional ceremony.
- **Compression over complexity** -- minimal, high-signal primitives. If it needs too much explanation, it's not production-grade.
- **Evidence over assertion** -- non-trivial claims require proof paths, not confident wording.
- **Every artifact earns its existence** -- if it doesn't improve outcomes, delete it.
- **The framework should shrink over time** -- better understanding removes ceremony, not accumulates it.

---

## Status

**Milestone 3.4**: recursive sub-cycles, convention drift detection, error recovery, backlog management. All milestones self-bootstrapped -- built using OODALOOP itself.

## License

UNLICENSED (internal use)
