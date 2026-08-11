# OODALOOP Principles

## Purpose

OODALOOP exists to improve AI-assisted software work **when uncertainty, consequence, coordination, or surprise make ordinary agent behavior insufficient**.

It is not the default planning framework. It should earn its invocation and collapse toward less process as agents, tools, and understanding improve.

The durable OODA invariant is not ceremony around five named phases. It is this:

> Act from the best current map, notice when evidence contradicts it, and re-orient before a bad trajectory compounds.

---

## Core principles

### 1. Ordinary agent behavior is the default

Needing a plan, touching multiple files, or being moderately complex does not justify OODALOOP.

Enter the framework only when meaningful residual consequential uncertainty remains after cheap local reasoning.

The routing judgment itself must be nearly free: no artifact, assessor, or workflow merely to decide whether a workflow is needed.

### 2. Complexity means remaining judgment, not amount of code

A useful conceptual variable is **residual consequential decision load**: how much high-impact judgment remains before an implementer can execute safely without inventing intent.

File count, task count, and lines changed are weak proxies. A mechanical 20-file edit may be cheap; a 15-line authorization change may deserve deep orientation.

Do not manufacture pseudo-precise entropy/complexity scores without calibrated evidence.

### 3. Spend intelligence where it collapses ambiguity

Reasoning is most valuable during discovery, architecture, decomposition, diagnosis, and rescoping—places where a good decision can make later execution mechanical.

Use the cheapest adequate intelligence once consequential choices have already been resolved.

Model/vendor names are execution policy, not architecture.

### 4. Plans should be high-information but weakly committed

Planning invariant:

> **Minimize residual consequential decisions while preserving maximum implementation optionality.**

Specify objective, behavior, invariants, constraints, interfaces when known, dependencies, acceptance, proof, and risk boundaries.

Do not prescribe incidental file organization, function shapes, control flow, or abstractions unless evidence actually constrains them.

This is the transferable design lesson behind the idea that explanations should be no more specific than necessary: commit strongly to what must be true, weakly to what need not be decided yet.

### 5. Decompose to executable leaves

A task is a node. A node is an executable **leaf** when a competent executor can complete it without inventing product intent, choosing architecture, discovering substantial new scope, or making another consequential trade-off absent from the spec.

Do not decompose to satisfy arbitrary file/task/modification quotas.

Mechanical multiplicity is not decision complexity.

### 6. Surprise is first-class evidence

No amount of planning eliminates unknown unknowns.

A **surprise** is observed evidence that materially violates the current map: contradicted assumptions, unexpected coupling, consequential choices absent from the plan, unexplained proof failure, material scope expansion, or dependencies that invalidate remaining work.

Do not require an executor to label an "unknown unknown." Require the system to stop silently absorbing evidence that changes the meaning of the work.

### 7. Re-enter only where the new judgment lives

A surprise does not imply a full recursive OODA ceremony.

Use the lightest response:
- local/mechanical fix,
- re-decompose at Decide,
- targeted Observe/Orient,
- or user judgment for high-risk/preference-dependent choices.

A supposed leaf can become a branch. Children resolve bottom-up. Not every child needs all phases.

### 8. Mechanize facts; leave semantic judgment to agents

Deterministic mechanisms are appropriate for facts such as schemas, state integrity, changed paths, test results, command status, destructive-operation interception, dependency conditions, and telemetry.

Agent judgment is appropriate for whether new evidence changes architecture, invalidates an assumption, warrants rescoping, or makes an alternative meaningfully better.

Do not mechanize judgment proxies merely to create the appearance of rigor.

### 9. Review must earn its cost

Independent/fresh-context review is valuable when a second lens can change a consequential decision: architecture, high blast radius, security/safety, material surprise, integration uncertainty, or ambiguous proof.

Routine leaves do not owe a second-model tax.

Never loop until a reviewer becomes stylistically satisfied.

### 10. Evidence over fluency

Claims should have proportionate proof paths. Hard relevant checks beat easy irrelevant checks.

Proof state should preserve what another agent needs to verify or resume, not giant raw transcripts.

### 11. Context is curated memory, not history

Persist knowledge when it materially shortens or improves a future trajectory—especially surprising repo behavior, non-obvious invariants, architectural constraints, reusable proof requirements, and causal lessons from failed approaches.

Do not accumulate ordinary execution history.

### 12. Restartability beats continuity assumptions

Long-running work should survive context loss and interruption through compact file-backed state.

State should describe the work—objective, assumptions, decisions, leaves, evidence, parent/child relationships—not the framework's ceremony.

### 13. Hosts provide substrate; OODALOOP provides semantics

Subagents, worktrees, parallelism, hooks, permissions, background execution, and model routers are host capabilities.

Use them through adapters when useful. Do not rebuild them in the core.

Hooks are especially useful for deterministic must-happen behavior; they should not become an architecture-judgment engine.

### 14. Instrument before theorizing routing

Collect cheap trajectory data—surprises, task splits, proof retries, user corrections, reorientation, review calls, children, and approximate costs where available.

Use observed outcomes later to learn better routing/model policies rather than inventing a complexity formula now.

---

## Design laws

1. **Every framework invocation must earn its cost.**
2. **Every artifact must improve execution, proof, coordination, recovery, or reusable learning.**
3. **Every plan must remove consequential reinterpretation, not local implementation freedom.**
4. **Every material surprise must be capable of interrupting the current trajectory.**
5. **Every re-entry should begin at the lightest phase that can resolve the new judgment.**
6. **Every deterministic fact that can be enforced cheaply should avoid semantic-agent theater.**
7. **Every safety boundary should prefer mechanical enforcement where the host exposes it.**
8. **Every simplification should preserve observability and restartability.**
9. **Every persistent learning should justify why a future unrelated task needs it.**
10. **The framework should get smaller as models and hosts get better.**

---

## Anti-patterns

Reject:
- framework gravity: agents choosing OODALOOP merely because work needs planning,
- process theater and mandatory ceremony for moderate work,
- second-model review after every leaf,
- arbitrary task/file-count complexity thresholds,
- rich classification vocabularies without decision value,
- full child cycles for local discoveries,
- giant execution/proof transcripts in persistent state,
- hardcoded current model names as architecture,
- custom swarm/concurrency infrastructure without an observed need,
- hooks used to make semantic architecture decisions,
- fake mathematical complexity scores,
- automating process that should have been deleted.

---

## Meta-principle

**OODALOOP is an escalation and recovery harness for maintaining orientation under uncertainty.**

Its success is measured partly by the hard work it handles well—and partly by how often it correctly stays out of the way.
