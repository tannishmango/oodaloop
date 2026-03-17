# OODALOOP Principles

## Purpose

OODALOOP exists to make AI-assisted feature development **faster, safer, and more adaptive** under uncertainty, without collapsing into process theater.

---

## Core Principles (Extracted From Kickoff Intent)

1. **Compression over complexity**
   - Prefer minimal, high-signal process primitives.
   - If a framework needs too much explanation, it is not production-grade.

1. **Coverage of the full development loop**
   - The system must cover research, scoping, planning, execution, verification, and reassessment.
   - Any missing phase eventually becomes hidden risk.

1. **Adaptive rigor**
   - Process depth should match task complexity and risk.
   - Tiny tasks should not require heavyweight ceremony.

1. **Minimum effective process**
   - The best process is no process, except for the irreducible scaffold required to maintain orientation, coordination, verification, and recovery.
   - Every extra phase, file, handoff, or rule is guilty until it proves it increases learning rate or execution reliability.

1. **Progress tracking as infrastructure**
   - Progress tracking is not documentation polish; it is the control surface for coordination.
   - State must be simple enough to stay updated and rich enough to guide next actions.

1. **Feedback loops are non-optional**
   - Plans are hypotheses, not truths.
   - Execution discoveries must be able to change scope and sequencing.

1. **Parallelism with dependency awareness**
   - Parallelize independent work; serialize coupled work.
   - Naive parallelism creates merge debt and context collisions.

1. **Context hygiene beats context volume**
   - Shared context should be intentionally curated, not accumulated.
   - Stale and duplicated context is a primary failure mode.

1. **Single source of truth**
   - Each critical concept has exactly one canonical home.
   - Duplication is latency: it turns into contradiction over time.

1. **Instruction followability as a design constraint**
   - Workflow quality is measured by whether agents reliably follow it.
   - If agents routinely violate the harness, the harness is poorly designed.

1. **Orchestration should be robust to imperfect agents**
   - The system should degrade gracefully when outputs are partial or noisy.
   - Reliability comes from architecture, not idealized model behavior.

1. **Epistemic rigor over assertion**
   - The system should privilege evidence, falsifiability, and explicit uncertainty over fluent narrative.
   - For non-trivial claims, trust should come from tests, checks, examples, or reconciliations, not confident wording.

---

## First-Principles Extensions (Cross-Domain Synthesis)

- **12) Orientation quality is the strategic bottleneck** (Boyd + information theory)
  - Observe/Act speed is useless if Orient is low-quality.
  - Better heuristics and models improve loop outcomes more than raw loop frequency alone.

- **13) Late commitment, fast revision** (OODA + PDSA)
  - Decide as late as practical with best available evidence.
  - Re-open decisions when new evidence invalidates assumptions.

- **14) Study, do not just check** (Deming PDSA)
  - Verification should explain why outcomes occurred, not only pass/fail status.
  - Every cycle should improve the next cycle's decision quality.

- **15) Manage the bottleneck, not the busyness** (TOC)
  - System throughput is constrained by few limiting factors.
  - Prioritize removal or protection of current bottlenecks before local optimizations.

- **16) Amdahl realism for parallel work**
  - Overall acceleration is bounded by serial portions.
  - Optimize handoffs and blocking dependencies before adding more parallel agents.

- **17) Preoccupation with failure** (HRO)
  - Treat anomalies and near-misses as high-value signals.
  - Small inconsistencies often predict large failures later.

- **18) Reluctance to simplify interpretation** (HRO)
  - Avoid first-story bias.
  - Use multiple hypotheses when diagnosing failures or drift.

- **19) Sensitivity to operations** (HRO)
  - Keep a live view of current state, not just planned state.
  - Operational awareness must outrank stale plan assumptions.

- **20) Deference to expertise**
  - In critical moments, route decisions to the agent/process with the best local signal.
  - Hierarchy should not overrule evidence.

- **21) Commitment to resilience**
  - Build for detection, containment, and recovery.
  - Failure handling quality is as important as success-path quality.

- **22) Falsifiability beats plausibility** (scientific method + TDD)
  - Important claims should be expressed in a form reality can refute.
  - Tests, invariants, and reconciliations are stronger than persuasive explanations.

- **23) Counterfactual comparison hardens decisions** (inversion + Bayesian updating)
  - Strong reasoning compares the chosen path against the best alternative, not just the first coherent plan.
  - Counterfactuals and steelmanning matter most when uncertainty, risk, or irreversibility is high.

---

## Design Laws For OODALOOP

1. **Every artifact and ritual must earn its existence**
   - Keep only files that directly improve execution, coordination, or verification.

2. **Every loop must update state**
   - If a cycle does not update canonical state, it did not complete.

3. **Every phase must emit evidence**
   - Decisions require traceable evidence links (inputs, outputs, rationale, confidence).

4. **Every handoff must be explicit**
   - Define who owns next action, prerequisites, and completion criteria.

5. **Every plan must be executable**
   - Plans should be written so execution can start without reinterpretation.

6. **Every verification must be actionable**
   - Failures must generate concrete next steps, not generic warnings.

7. **Every scope change must be intentional**
   - Scope drift without explicit acknowledgment is a system defect.

8. **Every simplification must preserve control**
   - Remove ceremony aggressively, but never remove observability or recovery.

9. **The framework should collapse toward less process over time**
   - Better understanding should remove ceremony, interfaces, and approvals rather than accumulate them.

10. **Every high-stakes claim needs a proof path**
    - Use tests, runtime checks, exemplars, invariants, or reconciliations to turn assertions into evidence.

---

## Anti-Patterns To Reject

- Framework bloat disguised as rigor.
- Creating artifacts because frameworks are expected to have them.
- Over-serialization that ignores parallel opportunities.
- Naive parallelism that ignores coupling and integration cost.
- Progress tracking spread across many stale files.
- Execution that never loops back to reassess scope.
- "Pass/fail" verification with no learning or causal insight.
- Plausible explanations presented as verified truth.
- Data-producing systems with no validation or reconciliation story.
- Optimizing local tasks while global bottlenecks remain untouched.
- Automating or formalizing process that should have been deleted.

---

## Meta-Principle

**OODALOOP is a learning-rate engine.**  
Its advantage is not just writing code faster; it is improving the quality of decisions per cycle while preserving execution reliability under uncertainty.
