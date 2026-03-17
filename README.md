# OODALOOP

OODA-loop orchestration for adaptive project delivery.

Private/internal plugin. This repository is intended for local use or private GitHub only, and is not for marketplace publication.

## What it does

OODALOOP structures project/feature work into an adaptive cycle:

- **Observe** -- research and gather requirements
- **Orient** -- decompose into an executable plan
- **Decide** -- implement atomic tasks
- **Act** -- verify outcomes against acceptance criteria
- **Loop** -- reassess scope based on execution evidence

Process depth scales with task complexity. Trivial tasks get a fast path; complex work gets full OODA with sentinel reassessment.

## Commands

| Command | Purpose |
|---------|---------|
| `/oodaloop-init` | Initialize `.oodaloop/` state in a project |
| `/oodaloop-observe` | Research and requirements gathering |
| `/oodaloop-orient` | Plan decomposition and task sequencing |
| `/oodaloop-decide` | Execute plan tasks |
| `/oodaloop-act` | Verify execution outcomes |
| `/oodaloop-loop` | Sentinel scope reassessment |
| `/oodaloop-status` | Report current state |
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

## Structure

```
plugin.json                  manifest
foundation/                  permanent doctrine
commands/                    8 entry-point commands
skills/                      7 procedural skills
agents/                      5 specialized agents
rules/                       3 boundary rules (always active)
templates/oodaloop/          state templates for target projects
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for design details and deconfliction status.

## Status

**Milestone 2** (current): functional init/observe/orient commands with enriched skills. Commands are thin invocations; skills contain executable procedures. Symlinked for local testing.

## License

UNLICENSED (internal use only)
