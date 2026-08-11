# Uncertainty-first redesign — August 2026

## Why this redesign exists

OODALOOP was originally intended to distill durable invariants for coding agents under uncertainty: orientation before action, explicit scope, restartable state, evidence, and the ability to stop/replan before a bad trajectory compounds.

In real use, the framework drifted away from that intent.

Agents gravitated toward OODALOOP whenever work appeared to need a plan. The routing rules made almost every multi-file/moderate task enter Observe → Orient → Decide → Act, and hard work entered an even more expensive full cycle. Once inside, plan assessors, per-task assessors, aggregate assessors, fixed classifications, proof narration, labor-strategy gates, and recursive child-cycle machinery made completion slow and expensive.

The framework was stopped in practice because its process cost often exceeded the uncertainty it reduced.

The key lesson is not "make the process more efficient." It is:

> **OODALOOP should not own work unless the work actually needs OODALOOP.**

This redesign therefore starts with subtraction.

---

## Source synthesis

### 1. Anthropic — *A field guide to Claude Fable 5: Finding your unknowns*

Source: https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns

The useful framing is the gap between the **map** (prompt/spec/context) and **territory** (the actual codebase/environment). The post divides unknowns into known knowns, known unknowns, unknown knowns, and unknown unknowns, and emphasizes techniques such as blind-spot passes, prototypes, references, implementation plans, and implementation notes.

Most important for OODALOOP: planning ahead helps but is not sufficient. Unknowns can emerge deep in implementation and may reveal that the problem itself should be solved differently.

Transfer:
- use blind-spot discovery adaptively for novel/high-consequence work,
- represent important assumptions and what would invalidate them,
- preserve the ability for implementation evidence to change the map.

Non-transfer:
- do not turn the four quadrants into a mandatory worksheet. Unknown unknowns cannot be exhaustively enumerated by definition.

### 2. Cursor — *Agent swarms and the new model economics*

Source: https://cursor.com/blog/agent-swarm-model-economics

Cursor's SQLite experiments support several durable ideas:
- large work naturally forms a tree,
- planners and workers benefit from different context responsibilities,
- context isolation may be more important than parallelism itself,
- expensive reasoning is especially valuable when it collapses ambiguity into explicit work,
- cheap workers can carry most execution tokens once consequential decisions are resolved,
- decorrelated review lenses can improve sustained quality,
- agents can preserve surprising reusable knowledge for successors (Field Guide).

Transfer:
- task tree is the invariant,
- planner intelligence should be concentrated on consequential decomposition/decisions,
- executors should consume decision-ready leaves,
- fresh-context review is valuable at meaningful risk/integration boundaries,
- persist surprising reusable knowledge that shortens future trajectories.

Non-transfer:
- OODALOOP does not need a swarm runtime, custom VCS, fixed planner/worker topology, or massive parallelism. Those are execution substrates for environments that need them.

### 3. Cursor — *How Cursor Router chooses the right model for the task*

Source: https://cursor.com/blog/how-cursor-router-works

Cursor Router uses production outcome data rather than an opinionated first-principles complexity formula. Its Compass component predicts whether a cheaper path will satisfy the user; more demanding work is then routed by learned task/domain/model strengths and cost-performance constraints.

Transfer:
- do not invent a fake scalar task-entropy score,
- collect trajectory/outcome data first,
- eventually learn which pre-implementation signals predict that a cheap executor can complete work without new consequential judgment,
- treat model selection as policy/economics rather than architecture.

### 4. Michael Timothy Bennett — *The Optimal Choice of Hypothesis Is the Weakest, Not the Shortest*

Source: arXiv:2301.12987v4

The paper argues, within a specific formalism of enactive cognition and assumptions including uniformly distributed tasks, that maximizing the **weakness** (extension) of a valid hypothesis maximizes its probability of generalizing, while minimum description length is neither necessary nor sufficient in that formal setting. It summarizes the epistemological implication as:

> Explanations should be no more specific than necessary.

Important caveat: this is not treated here as a proof about LLM coding agents or as a general law of software planning. The theorem depends on Bennett's formal task representation and assumptions; the empirical examples are toy binary arithmetic tasks.

Transfer:
- a plan can be high-information without being over-specified,
- resolve what execution must know while preserving possibilities not ruled out by evidence.

OODALOOP formulation:

> **Minimize residual consequential decisions while preserving maximum implementation optionality.**

---

## The new conceptual model

### Residual consequential decision load

Instead of equating complexity with code size, use a qualitative question:

> How much consequential judgment remains before an implementer can execute without having to reinterpret intent?

Sources include:
- unresolved requirements,
- known unknowns,
- assumptions whose failure changes the approach,
- novel/unfamiliar territory,
- architecture/cross-system coupling,
- unclear interfaces or ownership,
- missing/difficult proof paths,
- risk/blast-radius decisions,
- dependencies that materially affect decomposition.

This is a conceptual lens, not a numeric score.

### Cheap routing before framework state

```text
Can this be safely executed and verified
without unresolved consequential judgment?
        │
        ├─ yes → ordinary execution
        │
        └─ no
             │
             ├─ can lightweight local planning resolve it?
             │       └─ yes → ordinary plan → execute
             │
             └─ no → OODALOOP
```

The routing decision creates no artifact, calls no assessor, and need not initialize `.oodaloop/`.

### Plans lower intent into executable leaves

A leaf is ready when an executor does not need to invent product intent, architecture, substantial scope, or another high-impact trade-off absent from the spec.

Do not split by arbitrary file/task counts. Mechanical multiplicity is not decision complexity.

### Surprise is the runtime signal for unknown unknowns

A model cannot reliably announce "I found an unknown unknown." It can observe evidence that violates its prior map.

Surprise examples:
- assumption invalidation,
- unanticipated subsystem/dependency,
- consequential choice absent from the plan,
- local work becoming cross-cutting,
- proof failure outside the current model,
- repeated failure under the same interpretation,
- mutation scope expanding materially,
- remaining dependencies/plan becoming invalid.

The invariant is:

> Do not silently convert consequential new information into implementation.

### Targeted re-entry, not recursive ceremony

A supposed leaf can become a branch.

Route the new judgment to the lightest place it belongs:
- contained/mechanical → local quick fix,
- under-decomposed → Decide,
- map/evidence wrong → Observe/Orient,
- high-risk/preference → user judgment.

Persist a child only when the new work has a genuinely independent boundary and separate state helps coordination/restartability. A child does not automatically run all phases.

### Review is conditional

The old tri-mode assessor charged semantic review three times: plan, every leaf, aggregate.

The redesign keeps the useful invariant—independent/fresh-context lenses can catch different failures—but makes review event/boundary-triggered:
- architecture,
- material surprise,
- security/safety/high blast radius,
- integration uncertainty,
- ambiguous proof.

Routine leaves close on proportionate evidence.

### Deterministic facts vs semantic judgment

Mechanize cheap facts when hosts expose the surface:
- state schema,
- changed paths,
- test/command status,
- parent cycles,
- destructive-operation interception,
- lifecycle telemetry.

Leave semantic questions to agents:
- did this surprise invalidate architecture?
- should the objective change?
- REFINE or RESCOPE?
- is the alternative actually better?

### Host capabilities are substrate

Subagents, nested agents, worktrees, parallel execution, background agents, hooks, permissions, and model routers are rapidly improving host capabilities.

OODALOOP should consume them through adapters where useful, not recreate them in the core.

Lifecycle hooks become an optional adapter surface for deterministic must-happen behavior. They do not become a semantic supervisor.

---

## What this redesign intentionally removes

- OODALOOP as the default for "anything non-trivial",
- multi-file = complex routing,
- mandatory plan assessor,
- mandatory per-leaf assessor,
- mandatory aggregate assessor,
- `direct/delegated` labor strategy,
- task-count delegation threshold,
- arbitrary modification/file-count atomicity thresholds,
- mandatory pre-mortem/steelman/falsifiability prose,
- four-way discovery classification as runtime contract,
- automatic full child OODA cycles,
- `subagent/in-chat/new-chat` as semantic state,
- eight-field Paused schema,
- depth >3 consent as recursion design,
- quick-task create/delete task-file ceremony,
- CHANGELOG-required-on-every-commit hook,
- hardcoded `model: fast` role assumptions.

---

## What remains invariant

- orientation matters when uncertainty matters,
- plans are hypotheses and must be revisable,
- dependencies matter for decomposition/parallelism,
- executors should receive bounded intent,
- evidence beats fluent assertion,
- high-asymmetry external-state operations require safety boundaries,
- state must support restartability,
- persistent context must be curated,
- surprising reusable knowledge should improve successors,
- scope/trajectory must be able to change when evidence changes.

---

## What we deliberately do not know yet

This redesign does not claim to have solved task complexity measurement.

The next step is empirical. Useful trajectory signals include:
- NORMAL vs OODALOOP route,
- post-plan splits,
- surprises,
- unexpected mutation scope,
- proof retries,
- user corrections,
- REFINE/RESCOPE,
- optional reviewer calls and whether they changed decisions,
- child nodes,
- approximate model/tool cost where available.

Future question:

> Given what was known at planning time, what predicts that a cheaper executor can finish without requiring new consequential judgment?

That may eventually support learned adaptive routing. Until then, the architecture should remain qualitative, weakly committed, and cheap.

---

## Success test

OODALOOP should improve difficult work **and** disappear from ordinary work.

The framework is failing if its own process becomes a larger source of complexity than the task it is meant to orient.
