# OODALOOP Improvements

## Status

The August 2026 uncertainty-first redesign supersedes the April process-hardening tracker.

The previous tracker correctly identified several operational failures—subloops rarely firing, verdicts collapsing to CONTINUE, rich classification vocabularies without decision triggers, and prose contracts becoming template-filling—but many proposed fixes still added more gates to a framework that was already too expensive.

The current architecture takes the more fundamental route: remove framework gravity and fixed semantic-review cost first, then measure what is still missing.

Historical rationale remains available in git history.

---

## Working rule

Do not automatically run an OODALOOP cycle to improve OODALOOP.

Use the same routing invariant as any other repository work:
- ordinary changes → ordinary agent workflow,
- consequential uncertainty → OODALOOP only when it earns the cost.

Framework changes should prefer deletion/substitution over additive process.

---

## Next empirical work

### E-1: Measure whether OODALOOP stays out of the way

**Question:** after installation, do agents still self-select OODALOOP for ordinary planned work?

Collect examples across real repositories. Track:
- NORMAL vs OODALOOP route,
- why OODALOOP was selected,
- whether the user later judged the extra process worthwhile,
- cases that should retrospectively have stayed NORMAL.

**Success:** ordinary moderate work usually never creates OODALOOP state.

### E-2: Measure surprise detection quality

**Question:** do agents surface material map/territory mismatches before silently expanding scope?

Track:
- surprise count/type,
- evidence that triggered it,
- route chosen (quick / Decide / Observe-Orient / user),
- false positives where execution could safely have continued,
- missed surprises discovered by the user later.

Do not add more surprise categories until real trajectories show a decision need.

### E-3: Measure leaf readiness

**Question:** given a planned leaf, can an executor finish without inventing consequential intent?

Useful signals:
- post-plan task splits,
- new architectural choices during Act,
- unexpected subsystem/file-family expansion,
- user corrections during execution,
- proof failures caused by planning assumptions.

This is the main empirical proxy for residual decision load.

### E-4: Review economics

**Question:** when does the optional fresh-context reviewer improve outcomes enough to justify its cost?

Track reviewer trigger, conclusion, whether it changed the trajectory, and approximate cost where available.

If a trigger category almost never changes decisions, remove it.

### E-5: Host hooks

Implement host-specific deterministic hooks only after verifying the installed host API/version.

Priorities:
1. destructive/external-state interception,
2. state/schema validation,
3. changed-path / proof / lifecycle telemetry,
4. subagent completion/failure observation.

Do not implement semantic supervisor loops in hooks.

### E-6: Learned routing / model policy

Once enough trajectories exist, analyze which pre-implementation signals predict that a cheaper executor will finish without requiring new consequential judgment.

Possible features:
- novelty/domain familiarity,
- assumptions/open decisions,
- coupling/dependency structure,
- proof posture,
- historical surprise rates in the affected subsystem,
- user corrections,
- post-plan splits,
- task-tree depth,
- execution/review cost.

Do not create a hand-tuned numerical complexity score before this data exists.

### E-7: Repository cleanup

Continue deleting artifacts that only encoded the previous process model, including stale examples/visualizations/fixtures that imply:
- mandatory assessors,
- `direct/delegated` labor mode,
- three child execution strategies,
- depth-3 recursion consent,
- quick-task task-file ceremony.

Preserve only tests/examples that validate current factual state invariants.

---

## Evaluation principle

A future improvement is good when it increases information, safety, proof, coordination, or recovery **more than it increases framework cost**.

If better models or hosts make a mechanism unnecessary, delete it.
