# OODALOOP

**A lightweight, composable OODA harness for AI-assisted software delivery.**

Boyd built OODA for environments defined by friction, incomplete information, and changing conditions. Software delivery has the same shape.

OODALOOP is built to stay lightweight on simple tasks while remaining flexible, composable, and scalable when the work has to pause, rescope, or split into child loops.

Most agent harnesses optimize for forward motion. OODALOOP optimizes for maintaining orientation while the situation changes.

## Operating Premise

- Plans are provisional.
- Execution produces new intelligence.
- Progress without reassessment is drift.
- Task success does not guarantee objective success.
- The procedure must know how to pause, branch, and re-enter cleanly.

## The Procedure

```text
observe -> orient -> decide -> act -> loop
```

- `Observe` - reconnaissance. Gather facts, constraints, and signs of drift.
- `Orient` - situational assessment. Turn raw findings into a usable picture of the problem.
- `Decide` - course of action. Break the work into ordered tasks with clear acceptance.
- `Act` - execution. Carry out one task at a time.
- `Loop` - after-action assessment. Judge results and choose where to re-enter.

After `loop`, OODALOOP takes one of three actions:

- `CONTINUE` - the objective still holds and the results are sufficient.
- `REFINE` - the objective holds, but the plan must change.
- `RESCOPE` - the assumptions changed; return to observation.

The advantage is practical: the system does not just notice that reality changed. It knows where to re-enter the procedure.

## Recursive Shape

OODALOOP uses one loop shape everywhere.

- Run the full loop to complete an operation.
- Step back to `decide` or `observe` when new information invalidates the current course of action.
- Pause a parent task and open a child loop when a blocker becomes its own operation.

Child loops use the same shape and can recurse again if needed. That composability is what makes the system scalable: reassessment, reset, resume, and sub-operations all use the same procedure and state model.

## Closed-Loop Execution

This is the part most agent harnesses do not have.

Execution does not run open-loop. After each task, the assessor checks whether the step actually met its acceptance, whether it stayed aligned with design and intent, and whether anything discovered during execution changes the remaining plan.

Only then does the next task begin.

At the end of the cycle, the work is judged again at a different level: not "did each step complete," but "did the whole body of work solve the objective."

That distinction matters. Local success can still produce overall drift.

## Friction and Branching

The procedure assumes friction rather than treating it as an exception.

A small blocker can be handled inline. A larger blocker pauses the parent task and opens a child loop. When the child completes, control returns to the parent at the correct re-entry point with state intact.

```text
Task A: ship auth flow
  discovers missing migration
  pauses

Task B: create migration
  discovers schema conflict
  pauses

Task C: resolve schema conflict
  completes -> Task B resumes -> Task A resumes
```

This keeps the work legible. The blocker becomes structured work instead of dissolving into chat context and improvisation.

## Adaptive Rigor

OODALOOP does not force the same ceremony on every task.

- Low-risk local work can go through `/oodaloop-quick`.
- Normal scoped work runs through observe, orient, decide, and act.
- Higher-risk or unstable work gets the full loop, including after-action reassessment.

If the situation changes mid-execution, the procedure deepens with it. Rigor tracks risk.

## Roles

OODALOOP uses four narrow roles:

- `researcher` - reconnaissance and discovery
- `planner` - course-of-action design
- `executor` - implementation
- `assessor` - step authorization and after-action judgment

Three are readonly. Only the executor writes.

That separation is deliberate. Discovery, planning, execution, and assessment are different jobs. Keeping them distinct reduces self-justifying behavior and makes the procedure easier to trust.

## State

State lives in `.oodaloop/` inside the target project:

- `CONTEXT.md` - the current operating picture: conventions, architecture, decisions
- `BACKLOG.md` - deferred and follow-on work
- `<slug>.task.md` - the live record of a single OODA cycle

This gives the workflow durable memory inside the repo. It also makes pause/resume, rescope, and parent/child task chains explicit rather than conversational. Each loop keeps its own record, so recursion stays clean.

## Portability

OODALOOP is host-agnostic at the core. Skills, agents, rules, doctrine, and state stay the same. Thin adapters map those pieces to each host's discovery and install model.

Current targets include Cursor, Claude Code, and OpenCode.

## Install

```bash
git clone <repo-url>
cd oodaloop
./install.sh
```

Target a specific host if needed:

```bash
./install.sh cursor
./install.sh claude-code
./install.sh opencode
```

Then, inside any target project:

```text
/oodaloop-start
```

For local development of this repo:

```bash
./sync.sh
```

If a local Cursor install exists, the pre-commit hook runs that sync automatically.

## Commands

Entry and control:

- `/oodaloop-start` - initialize, resync state if needed, and route to the right flow
- `/oodaloop-quick` - fast path for trivial work
- `/oodaloop-status` - inspect active task state and parent/child chains
- `/oodaloop-sync` - reconcile state after interruption
- `/oodaloop-init` - create `.oodaloop/` state in a target project

Phase commands:

- `/oodaloop-observe` - gather facts and current constraints
- `/oodaloop-orient` - produce a situational assessment
- `/oodaloop-decide` - produce an ordered plan
- `/oodaloop-act` - execute task by task
- `/oodaloop-loop` - reassess and choose continue, refine, or rescope

## Project Shape

```text
.cursor-plugin/plugin.json   Cursor manifest
adapters/                    host-specific install mappings
foundation/                  doctrine and systems reference
commands/                    entrypoints
skills/                      procedures
agents/                      specialized roles
rules/                       always-on guardrails
templates/oodaloop/          project state template
install.sh                   installer
sync.sh                      local development sync
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full design, state model, and portability details.

## Principles

- Adaptive rigor over fixed ceremony.
- Evidence over assertion.
- Single source of truth for state.
- Verification before closure.
- Explicit handoffs over implicit drift.
- Less process over time, not more.

## License

UNLICENSED (internal use)
