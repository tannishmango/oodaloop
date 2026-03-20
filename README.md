# OODALOOP

Most agent frameworks make the agent serve the framework. OODALOOP inverts that.
Its core differentiator is scope control: the loop can stop itself before a bad plan compounds, re-evaluate with new evidence, and route blockers into targeted subloops.

---

## The Loop

Boyd built OODA for combat under friction and incomplete information. Software delivery has the same shape.

```
observe → orient → decide → act → loop
```

**Introspective by default.** Every phase can interrupt itself. Mid-act, the loop may detect scope drift, halt, and re-orient — reassessing whether completed work still holds or needs refactoring before continuing. The question is never "did steps complete" but "is the trajectory still correct."

**Scope guardrails over momentum.** The system is allowed to stop. If the current plan is underspecified or drifting, OODALOOP explicitly pauses execution, reevaluates scope, and updates trajectory before more code is written.

**Subloops and quick loops.** Any phase can spawn a child loop — a blocker, a scope question, a refactor of prior work. Lightweight quick loops handle trivial blockers fast; full subagent loops handle deeper uncertainty. Children resolve bottom-up before the parent resumes. Loops within loops, as deep as needed.

**Verdicts drive flow.** Each cycle ends: `CONTINUE`, `REFINE`, or `RESCOPE`. `REFINE` sends the loop back to re-examine specific tasks. `RESCOPE` rewinds to observe/orient with everything learned so far. Nothing is sunk cost.

**Adaptive rigor.** Trivial tasks skip ceremony. Complex tasks get full-cycle scrutiny. The loop scales itself.

Drop mid-cycle. Pick up anywhere. `/oodaloop-sync` reconciles state and tells you exactly where you left off.

---

## Roles

```
Observe    →  researcher    gather facts
Orient     →  researcher    synthesize into problem, risks, scope
Decide     →  planner       break into atomic, well-scoped tasks
Act        →  executor      build it
Loop       →  assessor      judge outcomes — including prior work coherence
```

---

## State

```
.oodaloop/
  CONTEXT.md        what IS
  BACKLOG.md        what SHOULD BE
  <slug>.task.md    what's HAPPENING — ephemeral, deleted on completion
```

---

## Install

```bash
git clone <repo-url>
cd oodaloop && ./install.sh
```

Then inside any target project: `/oodaloop-start`

Targets: **Cursor**, **Claude Code**, **OpenCode** — see [ARCHITECTURE.md](ARCHITECTURE.md).

---

UNLICENSED
