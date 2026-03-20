# OODALOOP

Most agent frameworks make the agent serve the framework. OODALOOP inverts that.

---

## The Loop

Boyd built OODA for combat under friction and incomplete information. Software delivery has the same shape.

```
observe → orient → decide → act → loop
```

**Introspective by default.** Every phase can interrupt itself. Mid-act, the loop may detect scope drift, halt, and re-orient — reassessing whether completed work still holds or needs refactoring before continuing. The question is never "did steps complete" but "is the trajectory still correct."

**Subloops.** Any phase can spawn a child loop — a blocker, a scope question, a refactor of prior work. Children resolve bottom-up before the parent resumes. Loops within loops, as deep as needed.

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
