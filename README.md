# OODALOOP

OODA-loop orchestration for adaptive project delivery.

Private/internal plugin. This repository is intended for local use or private GitHub only, and is not for marketplace publication.

## What it does

OODALOOP structures project/feature work into an adaptive cycle:

- **Observe** -- research, gather requirements, detect convention drift
- **Orient** -- decompose into an executable plan
- **Decide** -- implement atomic tasks, triage mid-execution discoveries
- **Act** -- verify outcomes against acceptance criteria
- **Loop** -- reassess scope, absorb learnings, curate backlog

Process depth scales with task complexity. Trivial tasks get a fast path; complex work gets full OODA with sentinel reassessment. Blocking discoveries during execution can spawn recursive sub-cycles that pause the parent task and resume after resolution.

## Commands

| Command | Purpose |
|---------|---------|
| `/oodaloop-begin` | Start here: bootstrap/check state and kick off the right flow |
| `/oodaloop-init` | Initialize `.oodaloop/` state in a project |
| `/oodaloop-observe` | Research and requirements gathering |
| `/oodaloop-orient` | Plan decomposition and task sequencing |
| `/oodaloop-decide` | Execute plan tasks |
| `/oodaloop-act` | Verify execution outcomes |
| `/oodaloop-loop` | Sentinel scope reassessment |
| `/oodaloop-status` | Report current state |
| `/oodaloop-sync` | Reconcile state after interruptions/refreshes |
| `/oodaloop-quick` | Fast path for trivial tasks |

## Agents

| Agent | Role | Access |
|-------|------|--------|
| researcher | Codebase exploration, discovery | readonly |
| planner | Task decomposition, sequencing | readonly |
| executor | Implementation | read/write |
| verifier | Acceptance checks, gap reporting | readonly |
| sentinel | Drift detection, loop verdicts | readonly |

## Key principles

- **Adaptive rigor**: process depth matches task complexity and risk.
- **Evidence over assertion**: non-trivial claims require proof paths.
- **Single source of truth**: one canonical home per concept.
- **Compression**: minimal, high-signal process primitives.
- **Every artifact earns its existence**: if it doesn't improve outcomes, delete it.

## State model

Project state lives in `.oodaloop/` within the target project:

| File | Lifecycle | Purpose |
|------|-----------|---------|
| `CONTEXT.md` | Persistent | Repo identity, conventions, architecture, decisions |
| `BACKLOG.md` | Persistent | Future work, deferred items, roadmap |
| `<slug>.task.md` | Ephemeral | One per active OODA cycle -- created at observe, deleted at loop |

CONTEXT.md is updated incrementally (convention drift, learning absorption). Task files capture the full lifecycle of a single piece of work and are deleted when complete. Multiple task files can coexist for concurrent work.

## Self-bootstrapping

OODALOOP builds itself. Each milestone uses the tooling produced by prior milestones. The plugin's own `.oodaloop/` directory tracks its development state, and every change to the plugin follows its own OODA cycle.

## Install

```bash
git clone <repo-url> && cd oodaloop
./install.sh
```

The install script detects your environment (Cursor, Claude Code, OpenCode) and places components where the host can discover them. To specify a host explicitly:

```bash
./install.sh cursor
./install.sh claude-code
./install.sh opencode
```

Then in any project: run `/oodaloop-begin` to start.

`/oodaloop-begin` is the default kickoff command. It initializes state if needed, asks a short guided intake if your objective is unclear, then routes you to `/oodaloop-quick` or `/oodaloop-observe`.

For Cursor local development, sync updates into Cursor's local plugin directory with:

```bash
./sync.sh
```

Do this after any edits to the plugin. Then reload Cursor window.

For manual setup or other hosts, see `adapters/<host>/install.md`.

## Structure

```
.cursor-plugin/plugin.json   Cursor manifest
adapters/                    per-host install instructions
foundation/                  permanent doctrine
commands/                    10 entry-point commands
skills/                      9 procedural skills (Agent Skills standard)
agents/                      5 specialized agents
rules/                       3 boundary rules (always active)
templates/oodaloop/          CONTEXT.md template for target projects
install.sh                   host-detecting installer
sync.sh                      sync to Cursor local plugin directory
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for design details, portability model, and deconfliction status.

## Status

**Milestone 3.4** (current): recursive sub-cycles, concrete convention drift detection, error recovery, backlog management. All milestones were self-bootstrapped -- built using OODALOOP itself.

## License

UNLICENSED (internal use only)
