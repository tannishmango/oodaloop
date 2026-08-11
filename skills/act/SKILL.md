---
name: act
description: Execute decision-ready leaves, prove them proportionately, and interrupt only when evidence shows the map no longer fits the territory.
---

> Boyd's Act changes the environment. OODALOOP should protect Act from unresolved consequential judgment without surrounding every change with ceremony.

## Trigger

`/oodaloop-act` after Decide, or resumption of a paused leaf after targeted uncertainty is resolved.

## Preconditions

- Active task file contains a Plan with executable leaves.
- `.oodaloop/CONTEXT.md` exists.

## Workflow

### 1. Read only what execution needs

Read the active leaf, its dependencies/invariants, relevant repo conventions, and proof requirement.

Do not load BACKLOG, unrelated plan branches, or broad doctrine into every executor context.

### 2. Select the cheapest adequate execution substrate

For each ready leaf, choose execution mechanics based on current host capability and economics:
- inline execution is fine,
- independent leaves may use subagents/parallelism when it actually saves context or wall time,
- isolated worktrees may be used when the host supports them and collision risk warrants it,
- model choice should use the cheapest model adequate for the remaining judgment.

There is no permanent `direct`/`delegated` mode and no task-count threshold that forces delegation.

A leaf that is truly decision-ready should usually be cheap to execute regardless of how difficult its parent problem was.

### 3. Execute and prove

For each leaf:

1. Implement within the leaf's intent/invariants.
2. Respect repo-native conventions.
3. Run the strongest **proportionate** proof required to establish acceptance.
4. Record concise evidence in the task file.

Do not paste large raw outputs into state. Preserve the command/result and critical evidence needed for recovery or review.

### 4. Detect surprise continuously

A **surprise** is evidence that materially violates the current map of the leaf or parent task.

The executor must surface surprise, but detection must not rely only on the executor choosing an expensive classification. The orchestrating agent should also compare the actual trajectory with the plan.

Signals include:
- an assumption's invalidation condition fires,
- work requires an unanticipated subsystem or materially different file family,
- a consequential semantic/architectural choice appears that the leaf did not resolve,
- supposedly local work becomes cross-cutting,
- proof fails for reasons outside the planned model of the change,
- repeated attempts fail under the same interpretation,
- a workaround would touch shared/core/external state beyond the leaf's understood boundary,
- actual dependencies invalidate remaining plan ordering or intent,
- mutation scope expands materially beyond what acceptance implied.

A surprise is not automatically a failure and does not automatically launch a child OODA cycle. It is an interrupt: **do not silently turn new consequential information into implementation.**

### 5. Route surprise by the judgment it requires

Pause only the affected leaf, preserve completed evidence, and choose the lightest response:

- **Contained/mechanical** → `/oodaloop-quick`; fix and resume.
- **Leaf was under-decomposed / plan needs splitting** → return to Decide with the new evidence.
- **Map/assumption is wrong or missing evidence** → targeted Observe/Orient re-entry.
- **High-risk or preference-dependent decision** → ask the user for the specific judgment.

Create a child task node only when the discovered work has a genuinely independent objective/dependency boundary and separate persistence improves coordination or restartability. A child does **not** have to run all five OODA phases; enter at the phase its uncertainty actually requires.

Parent/child state should record only what a cold resumption needs: parent, child, blocked leaf, new evidence, and resume point. Do not choose among `subagent`/`in-chat`/`new-chat` as semantic task state; those are execution-substrate choices.

### 6. Review only when review is informative

There is **no mandatory semantic assessor after every leaf**.

Invoke an independent/fresh-context reviewer only when one of these makes a second judgment likely to add information:
- material surprise,
- high-blast-radius or security/safety-sensitive change,
- architectural commitment,
- integration boundary where individually correct leaves may conflict,
- proof gap or ambiguous evidence.

Ordinary leaves close on their acceptance evidence.

### 7. Destructive / external-state boundary

Before external-state mutations that are destructive, irreversible, uncontained, or uncertain, require the user approval specified by the safety rule.

Where the host supports deterministic pre-tool hooks or permissions, prefer mechanical enforcement. Prose remains the portable fallback.

### 8. Evidence format

Keep one compact log:

```markdown
## Execution

### T1: <title>
**Status**: done | paused
**Changes**: <paths/components>
**Proof**: <command/check + result + critical evidence>
**Surprise**: none | <new evidence and why it changes the map>
**Review**: none | <why review was triggered + conclusion>
```

Do not add fields that do not improve recovery, proof, or future routing data.

### 9. Transition

When all leaves required for the objective are complete, set phase to `loop` for lightweight boundary reconciliation.

## Output

Executed leaves with proportionate evidence, plus explicit interrupts where implementation discovered that the plan was no longer sufficient. Routine execution should not pay semantic-review tax.
