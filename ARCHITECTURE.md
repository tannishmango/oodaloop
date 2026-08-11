# OODALOOP Architecture

## Purpose

OODALOOP is a host-agnostic escalation and recovery harness for agentic software work under consequential uncertainty.

It is **not** the default planning system. Ordinary agent planning/execution remains the default path.

OODALOOP is justified when uncertainty, novelty, coupling, blast radius, proof difficulty, coordination, or implementation surprise make the cost of a wrong trajectory meaningfully larger than the cost of extra orientation.

The architectural invariant is:

> Act from the best current map, detect when evidence contradicts it, and re-orient before drift compounds.

---

## 1. Entry routing

Routing happens **before** OODALOOP state, artifacts, or agents are invoked.

The preflight must be cheap enough that every task can implicitly afford it:

```text
Can current context support safe execution + verification
without unresolved consequential judgment?
        │
        ├─ yes → NORMAL
        │
        └─ no
             │
             ├─ can lightweight local planning resolve it?
             │       └─ yes → NORMAL + ordinary plan
             │
             └─ no → OODALOOP
```

### Routing signals

OODALOOP becomes more useful when work contains:
- unfamiliar/poorly understood territory,
- architecture or cross-system coupling,
- assumptions whose failure changes the approach,
- unclear interfaces/ownership/acceptance semantics,
- high-asymmetry risk or blast radius,
- difficult/missing proof paths,
- decomposition needed to prevent executors inventing consequential intent,
- evidence from implementation that the current map is wrong.

Task count, file count, and lines changed are weak signals and never sufficient alone.

### Routing outcomes

- **NORMAL**: no `.oodaloop/` initialization, sync, task file, or OODALOOP agent call. Continue with host-native agent behavior.
- **OODALOOP**: initialize/reconcile state only now, then enter at the lightest phase that can reduce the unresolved uncertainty.

---

## 2. Semantic loop

```text
observe → orient → decide → act → loop/reconcile
```

These names describe responsibilities, not mandatory ceremony for every node.

### Observe

Gather evidence that can change the approach. Perform a blind-spot pass when novelty/risk warrants it. Persist facts, important assumptions, invalidation conditions, and open consequential decisions.

Do not perform exhaustive repo/proof inventories by default.

### Orient

Interpret evidence and identify **residual consequential decision load**: what high-impact judgment an implementer would otherwise have to invent.

Narrow the option space while preserving implementation freedom not constrained by evidence.

### Decide

Resolve consequential choices and decompose into executable leaves.

Planning invariant:

> **Minimize residual consequential decisions while preserving maximum implementation optionality.**

A leaf is executable when a competent executor can complete it without inventing product intent, choosing architecture, discovering substantial new scope, or making another high-impact trade-off absent from the spec.

### Act

Execute decision-ready leaves using the cheapest adequate host substrate/model, run proportionate proof, and detect material surprise.

Routine leaves do not require semantic review.

### Loop / reconcile

At a meaningful boundary, compare evidence with objective/invariants and choose:
- `CONTINUE`,
- `REFINE` (return to Decide at the affected node),
- `RESCOPE` (targeted Observe/Orient).

Loop is lightweight when nothing changed. It is not a mandatory second audit of all leaves.

---

## 3. Task tree and recursion

Large work naturally forms a task tree:

```text
root objective
  ├─ branch
  │   ├─ leaf
  │   └─ leaf
  └─ leaf
```

OODALOOP does not impose a fixed swarm topology. The tree grows only as the problem requires.

### Leaf → branch promotion

A planned leaf may reveal during execution that it still contains consequential uncertainty. That is evidence the leaf was not actually executable.

The leaf can be promoted back into a branch:
- re-decompose at Decide,
- gather targeted evidence at Observe/Orient,
- or create a separately persisted child node when independence/restartability justify it.

### Child nodes

A child is not automatically a full OODA cycle.

Children begin at the lightest phase their uncertainty requires and resolve bottom-up. Parent reconciliation uses only the returned result/evidence that can affect parent assumptions/invariants.

Separate child persistence is justified only when it materially improves coordination or restartability.

No arbitrary recursion-depth cap is part of the semantic model. If recursion grows without reducing uncertainty, the correct response is to rescope/simplify—not to add more procedural depth.

---

## 4. Surprise model

Planning cannot enumerate unknown unknowns. Runtime detection focuses on observable surprise.

**Surprise** = evidence that materially violates the current map.

Signals include:
- assumption invalidation,
- unexpected subsystem/dependency,
- consequential choice absent from the leaf,
- local work becoming cross-cutting,
- proof failure outside the planned model,
- repeated failure under the same interpretation,
- workaround requiring shared/core/external mutation beyond understood scope,
- dependency/order invalidation,
- material mutation-scope expansion.

### Surprise routing

```text
surprise
  ├─ contained/mechanical → quick local fix
  ├─ under-decomposed     → Decide
  ├─ map/evidence wrong   → Observe / Orient
  └─ high-risk/preference → user judgment
```

The invariant is not frequent escalation. It is that consequential new evidence cannot be silently absorbed into implementation.

---

## 5. Review architecture

The previous architecture used a mandatory tri-mode assessor:
- plan assessment,
- per-leaf verification,
- aggregate assessment.

That created large fixed semantic-review cost and encouraged process completion rather than information gain.

The new architecture uses an optional `reviewer`.

### Reviewer triggers

Use a fresh independent lens when review can plausibly change a consequential decision:
- architectural commitment,
- security/safety/high blast radius,
- material surprise,
- integration uncertainty,
- ambiguous/incomplete proof,
- planner/executor anchoring with meaningful downside.

Routine leaves close on deterministic/proportionate acceptance evidence.

### Review principle

Prefer fresh context over the implementer's full reasoning transcript. Review the claim/evidence/decision, not the process story.

Never loop until a reviewer becomes stylistically satisfied.

---

## 6. Agent roles

| Agent | Writes | Role |
|---|---:|---|
| researcher | no | targeted evidence, codebase discovery, blind-spot pass |
| planner | no | consequential decisions, weakest-sufficient plan, leaf readiness |
| executor | yes | one decision-ready leaf + proof + surprise surfacing |
| reviewer | no | optional independent semantic lens when triggered |

No core role hardcodes a specific current model tier/name.

### Model economics policy

- spend stronger reasoning where it collapses ambiguity or changes architecture,
- use the cheapest adequate model for decision-ready execution,
- select reviewer intelligence proportional to the judgment being audited.

Host/router implementations may learn this policy empirically over time.

---

## 7. State model

Project state lives in `.oodaloop/` only after work actually enters OODALOOP.

```text
.oodaloop/
  CONTEXT.md       persistent curated reusable knowledge
  BACKLOG.md       persistent real future work
  <slug>.task.md   ephemeral active task/node
  CYCLES.log       optional cheap trajectory telemetry
```

### CONTEXT.md

Persist only knowledge that materially improves a future unrelated trajectory:
- surprising repo behavior,
- non-obvious invariants,
- architecture constraints/decisions,
- reusable proof requirements,
- causal lessons from failed approaches.

Do not accumulate execution history.

### Task files

Task files contain only what execution/recovery needs:
- objective and why OODALOOP was warranted,
- observations/requirements/assumptions when relevant,
- assessment and consequential decisions,
- task tree/leaves,
- compact execution/proof evidence,
- surprise/review results,
- parent/child waiting/resume facts when needed.

Valid phases remain `observe`, `orient`, `decide`, `act`, `loop`, but backward re-entry is allowed. Phase denotes the next consequential judgment, not a ritual completion history.

### Parent/child state

Minimal waiting record:

```text
Child
Blocked leaf
New evidence
Resume at
```

Execution substrate is not state. Do not store `subagent`/`in-chat`/`new-chat` or `direct`/`delegated` as semantic task fields.

---

## 8. Deterministic mechanisms vs semantic policy

### Mechanize facts

When cheap/available, deterministic mechanisms should enforce or capture:
- task-state schema and phase/evidence pairing,
- parent-cycle / missing-child integrity,
- tests/type/lint command outcomes,
- changed paths / mutation scope,
- destructive-operation interception,
- dependency conditions,
- lifecycle telemetry.

### Keep judgment semantic

Agents decide:
- whether surprise is consequential,
- whether architecture/assumptions are invalidated,
- whether the objective should change,
- whether an alternative is meaningfully better,
- whether new evidence warrants REFINE/RESCOPE.

Do not automate shallow proxies for these judgments.

---

## 9. Adaptive proof

Proof must be strong enough to establish the acceptance claim and proportionate to risk.

Examples:
- pure logic → unit tests may suffice,
- integration behavior → integration proof when available/required,
- configuration/schema → relevant validators/build checks,
- external-state behavior → sandbox/real-system proof according to risk and user permission.

Hard relevant proof beats easy irrelevant proof.

Do not create blanket TDD or maximal-proof ceremony for every leaf. Proof ordering may be chosen to increase confidence where failure is expensive, but process is not an invariant.

---

## 10. Host adapter architecture

Core semantics remain host-agnostic.

Adapters map host capabilities:

1. commands / entrypoints,
2. skills,
3. agent definitions,
4. rules / persistent instruction surfaces,
5. manifest / registration where required,
6. **optional lifecycle hooks / deterministic event handlers**.

### Hooks

Use hooks for must-happen deterministic behavior when the host supports them, such as:
- destructive-operation interception,
- cheap state validation,
- changed-path telemetry,
- proof/lifecycle capture,
- subagent completion/failure observation.

Do not make hooks decide architecture or rescoping.

### Other native substrate

Subagents, nested agents, parallelism, worktrees, background execution, and model routing are adapter/execution-policy capabilities. The core task tree does not depend on any one implementation.

---

## 11. Telemetry and future routing

Do not invent a mathematical task-entropy score in the current system.

Collect cheap trajectory data first:
- OODALOOP invoked vs NORMAL,
- leaf count,
- surprise count/types,
- post-plan splits,
- proof retries/gaps,
- user corrections,
- REFINE/RESCOPE,
- reviewer calls,
- child nodes,
- approximate cost where the host exposes it.

The future empirical routing question is:

> Given what was known before implementation, what predicts that a cheaper executor can finish without requiring new consequential judgment?

Learn from real trajectories before hardcoding complexity theory.

---

## 12. Anti-patterns

Reject explicitly:

1. **Framework gravity** — invoking OODALOOP because work merely needs a plan.
2. **Process theater** — fixed artifacts/checklists that do not change decisions.
3. **Mandatory semantic review** — second-model tax on routine leaves.
4. **Arbitrary complexity thresholds** — task/file counts treated as reasoning complexity.
5. **Classification bloat** — vocabularies that do not change routing.
6. **Recursive ceremony** — full five-phase child cycles for local discoveries.
7. **Context bloat** — transcripts and task history in persistent state.
8. **Host reimplementation** — building custom swarm/worktree/router machinery already provided by hosts.
9. **Hardcoded model frontier** — vendor/model names embedded as architectural truth.
10. **Fake precision** — invented entropy/complexity scores without calibrated data.
11. **Automation of bad process** — mechanizing rituals that should have been deleted.

---

## Success condition

OODALOOP succeeds when:
- hard, uncertain work gets better orientation and recovery,
- surprise cannot silently become scope drift,
- plans reduce consequential ambiguity without strangling implementation,
- review and state are proportional,
- host capabilities are leveraged without contaminating core semantics,
- and ordinary software work usually never enters the framework at all.
