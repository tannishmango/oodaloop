# OODALOOP Adapters

OODALOOP's core semantics (routing, skills, task-tree/state model, doctrine) are host-agnostic. Adapters expose those semantics through whatever capabilities a host actually provides.

## Adapter surfaces

Each adapter may map six surfaces:

| Surface | What it does | Core requirement? |
|---|---|---|
| **Commands** | Places explicit OODALOOP entrypoints where the host discovers them | yes |
| **Skills** | Makes procedural skill files discoverable | yes |
| **Agents** | Translates researcher/planner/executor/reviewer definitions | when host supports custom agents |
| **Rules** | Carries lightweight invariants such as default-NORMAL routing and safety | yes |
| **Manifest** | Registers the package if the host requires one | host-specific |
| **Lifecycle hooks** | Deterministic must-happen checks/telemetry around tool/session/agent events | optional |

## What adapters must not redefine

- when OODALOOP semantically earns invocation,
- residual-decision-load / leaf-readiness semantics,
- surprise meaning,
- task parent/child semantics,
- persistent state meaning,
- doctrine.

Host capabilities implement the substrate; they do not redefine the task model.

## Lifecycle hooks

Modern hosts increasingly expose lifecycle hooks. Use them where they can enforce **facts** cheaply and outside the reasoning context.

Good candidates:
- intercept destructive/external-state operations,
- validate task-state schema,
- record changed-path / lifecycle telemetry,
- observe subagent completion/failure,
- capture proof command outcomes,
- restore narrowly scoped context after compaction when needed.

Bad candidates:
- decide whether an architecture is correct,
- decide whether surprise is consequential,
- choose REFINE vs RESCOPE,
- implement a semantic supervisor loop in shell callbacks.

When hooks are unavailable, portable prose/tooling fallbacks remain valid.

## Execution substrate

Adapters may also leverage host-native:
- subagents / nested agents,
- parallel execution,
- isolated worktrees,
- background execution,
- permissions,
- model routing.

These are selected per ready leaf based on independence, context, risk, and economics. OODALOOP no longer persists a global `direct`/`delegated` labor mode or `subagent`/`in-chat`/`new-chat` child strategy.

## Host capability matrix

Capabilities evolve quickly; treat this table as adapter-maintenance guidance rather than core doctrine.

| Capability | Cursor | Claude Code | OpenCode |
|---|---|---|---|
| Slash/explicit commands | adapter maps host entrypoint | adapter maps host entrypoint | adapter maps host entrypoint |
| Skills | supported | supported | supported/configurable |
| Specialized agents | supported | supported | configurable |
| Rules/instructions | supported | supported | configurable |
| Lifecycle hooks | use when available; capability may vary by version | use when available; capability may vary by version | optional/config-dependent |
| Manifest required | yes for plugin packaging | no core requirement | no core requirement |

Do not encode fast-moving host feature details into core skills. Keep exact paths/syntax in each `adapters/<host>/` implementation note and update them independently.

## Install flow

```text
clone repo → run install.sh → detect host → apply adapter → done
```

Installation should not cause agents to route normal work into OODALOOP. The always-on rule must preserve the NORMAL default.

## Adding a new host

1. Create `adapters/<host>/`.
2. Map commands, skills, agents, rules, and registration.
3. Map lifecycle hooks only for deterministic invariants that clearly benefit.
4. Document any host-native execution substrate the runtime can optionally use.
5. Keep routing/uncertainty/task-tree semantics unchanged.
