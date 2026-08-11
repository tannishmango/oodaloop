# OODALOOP

Most software work should **not** use OODALOOP.

OODALOOP is an escalation and recovery harness for agentic coding when uncertainty, consequence, coordination, or implementation surprise make ordinary planning insufficient.

Its core job is simple:

> Act from the best current map, notice when the territory contradicts it, and re-orient before a bad trajectory compounds.

---

## Stay out by default

Needing a plan is not enough reason to enter OODALOOP.

Neither is touching multiple files, having several steps, or being "moderately complex."

Before entering, use a nearly-free preflight:

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

A mechanical 20-file edit may stay ordinary. A 15-line authorization or migration change may deserve deep orientation.

`/oodaloop-start` can explicitly return **NORMAL** and create no framework state at all.

---

## The loop

For work that earns the extra reasoning:

```text
observe → orient → decide → act → reconcile
```

These are semantic responsibilities, not ceremony every node must repeat.

**Observe** gathers evidence that can change the approach, including blind spots in unfamiliar territory.

**Orient** turns evidence into meaning and exposes the consequential decisions an executor would otherwise have to invent.

**Decide** resolves those choices and decomposes only until work becomes executable leaves.

**Act** executes leaves and proves them proportionately.

**Reconcile (Loop)** checks whether action changed the map enough to require refinement or rescoping.

---

## High-information, weakly committed plans

A good plan removes consequential ambiguity without prescribing implementation detail that evidence does not justify.

The planning invariant is:

> **Minimize residual consequential decisions while preserving maximum implementation optionality.**

Plans should be strong about behavior, invariants, constraints, dependencies, acceptance, proof, and safety boundaries—and intentionally weak about incidental local implementation choices.

A leaf is ready when an executor can complete it without inventing product intent, choosing architecture, discovering substantial new scope, or making another high-impact trade-off absent from the spec.

---

## Surprise is the runtime interrupt

Planning cannot enumerate unknown unknowns.

OODALOOP instead looks for their observable consequence: **surprise**—evidence that materially violates the current map.

Examples:
- an assumption is contradicted,
- an unexpected subsystem becomes necessary,
- a consequential choice appears that the leaf never resolved,
- local work becomes cross-cutting,
- proof fails for reasons outside the planned model,
- repeated attempts fail under the same interpretation,
- remaining plan dependencies no longer make sense.

Surprise does not automatically launch a full child OODA cycle. Route to the lightest place the new judgment lives:

```text
contained/mechanical → quick local fix
under-decomposed     → Decide
map/evidence wrong   → Observe / Orient
high-risk/preference → user judgment
```

A supposed leaf may become a branch. Children resolve bottom-up, but they enter only the phase they actually need.

---

## Review only when it can change something

Routine leaves close on proportionate proof.

There is no mandatory second-model assessor after every task and no mandatory plan-assessor loop.

A fresh-context `reviewer` is optional for consequential architecture, material surprise, security/safety risk, integration uncertainty, or ambiguous proof.

Deterministic facts should be checked deterministically. Semantic judgment should not be turned into checklist theater.

---

## Roles

```text
researcher → targeted evidence + blind-spot discovery
planner    → consequential decisions + executable leaves
executor   → implement one decision-ready leaf
reviewer   → optional independent lens when review earns its cost
```

Model choice is execution policy, not architecture. Spend stronger reasoning where it collapses ambiguity; use the cheapest adequate intelligence for already-resolved execution.

---

## State

```text
.oodaloop/
  CONTEXT.md        curated reusable knowledge
  BACKLOG.md        real future work
  <slug>.task.md    ephemeral active task/node
  CYCLES.log        optional cheap trajectory telemetry
```

State exists for restartability, not process bookkeeping.

Persist surprising/non-obvious knowledge that materially improves future trajectories. Do not turn CONTEXT into a transcript.

Parent/child state records only what cold resumption needs: parent, child, blocked leaf, new evidence, and resume point.

---

## Host capabilities

The core is host-agnostic. Adapters may use native capabilities such as:
- subagents,
- worktrees,
- parallel execution,
- permissions,
- lifecycle hooks,
- model routing.

These are execution substrates, not OODALOOP semantics.

Hooks are especially useful for deterministic must-happen behavior such as destructive-operation interception, state validation, or cheap telemetry. Architectural judgment remains with agents.

Targets currently include **Cursor**, **Claude Code**, and **OpenCode**. See [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Install

```bash
git clone <repo-url>
cd oodaloop && ./install.sh
```

Inside a target project, invoke `/oodaloop-start` only when you want to evaluate/enter the escalation path. Ordinary agent work does not need to pass through it.

---

## Design test

OODALOOP is working when it handles genuinely uncertain work better **and** correctly stays out of the way for ordinary work.

The framework should get smaller as agents and hosts get better.

---

UNLICENSED
