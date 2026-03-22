# OODALOOP Principles (Compressed)

Derived from `foundation/PRINCIPLES.md`. Use this as a high-signal orientation aid, not a replacement for canonical doctrine.

## Operating intent

- Optimize for faster, safer delivery under uncertainty.
- Prefer compression: minimal process primitives, maximum signal.
- Keep the full loop intact: observe, orient, decide, act, loop.

## Decision heuristics

1. **Adaptive rigor**: match process depth to risk and complexity.
2. **Minimum effective process**: keep only scaffolding that improves coordination, verification, or recovery.
3. **Orientation first**: better models/heuristics beat raw loop speed.
4. **Late commitment, fast revision**: decide with best current evidence and re-open when assumptions break.
5. **Bottleneck focus**: optimize system constraints before local throughput.
6. **Dependency-aware parallelism**: parallelize independent work, serialize coupled work.
7. **Context hygiene**: curated shared context beats high context volume.
8. **Single source of truth**: each critical concept has one canonical home.
9. **Robustness to imperfect agents**: architecture should degrade gracefully.
10. **Restartability beats continuity assumptions**: design steps to fail cleanly, retry safely, and resume from known state.
11. **Evidence over fluency**: confidence comes from proof paths, not narrative tone.
12. **Risk gates autonomy**: autonomous action is bounded by three dimensions — reversibility (can undo via revert), containment (effect limited to task-created state), and confidence (certain about current state and expected outcome). Any unfavorable dimension requires human approval regardless of urgency or scope.

## Execution laws

- Every artifact must earn its existence.
- Every loop must update canonical state.
- Every phase must emit evidence.
- Every handoff must be explicit.
- Every plan must be executable without reinterpretation.
- Every verification must produce actionable next steps.
- Every scope change must be explicit and intentional.
- Every simplification must preserve observability and recovery.
- High-stakes claims require a falsifiable proof path.

## Failure-detection prompts

- What would disprove this conclusion?
- What is the strongest alternative explanation?
- What is the likely failure mode and earliest signal?
- What uncertainty remains and what evidence would reduce it?
- Has this component accumulated a second job?
- Could this complexity move into structured data instead of branching logic?
- Is this step serving the task, or preserving the framework?
- Is this action reversible, contained to task-created state, and based on certain knowledge? If any answer is no, who approved it?

## Anti-patterns to reject

- Process theater and framework bloat.
- Monolithic orchestration fused with task-specific judgment.
- Context accumulation without curation.
- Duplicate state tracking that drifts.
- Easy tests substituted for hard but relevant tests.
- Pass/fail checks with no causal learning.
- Local optimization while system bottlenecks remain.
- High-risk workarounds (irreversible, uncontained, or uncertain) taken to maintain execution velocity.

## Usage constraints

- Apply selectively for non-trivial decisions and uncertain trade-offs.
- Skip for trivial quick-path work where this would add overhead.
- If guidance conflicts with canonical doctrine, `PRINCIPLES.md` wins.
