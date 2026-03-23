---
name: act
description: Execute plan tasks and verify each against acceptance criteria.
---

> Boyd's Act: Implement the decided course of action. The only stage where the environment changes. (foundation/OODALOOP.md)

> **Plugin paths**: `foundation/` references in this skill are relative to the OODALOOP plugin root, not the workspace. Resolve from this skill file's installed path.

## Trigger

`/oodaloop-act` or transitioning from Decide phase.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with a Plan section (from decide).
- `.oodaloop/CONTEXT.md` must exist.
- Task file phase should be `act`.

## Workflow

### 1. Read plan, context, and labor strategy
Read the active task file's Plan section, including the **Labor Strategy** subsection (written by the plan assessor during decide). Read `.oodaloop/CONTEXT.md` conventions — these are binding constraints on implementation (commit format, linter rules, test patterns, etc.).
Treat the `Proof Infrastructure` subsection as binding for verification selection:
- choose the strongest available proof command relevant to each task
- only use weaker evidence when stronger checks are unavailable or explicitly blocked

If no Labor Strategy subsection exists: count total tasks in the Plan section. If the plan has more than 6 tasks, STOP — report to the user that the plan exceeds the direct-mode threshold without a labor strategy and recommend re-running `/oodaloop-decide` Step 8 to generate one. For plans with ≤6 tasks, default to `direct` mode.

For non-trivial verification judgments and uncertainty handling, also read `foundation/PRINCIPLES-COMPRESSED.md` and apply only relevant heuristics.

### 2. Handle pre-scoping flags
If the Labor Strategy includes pre-scoping flags, resolve each before any execution begins. For each flagged task, spawn a child OODA cycle (following the blocking-complex procedure in Step 4) scoped to that task's specific ambiguity. The child's objective is to produce a well-scoped replacement. Incorporate the result back into the plan (replace or refine the flagged task) before proceeding.

If no pre-scoping flags, skip this step.

### 3. Execute, assess, repeat
Read the Labor Strategy mode (`direct` or `delegated`).

#### Direct mode
For each task in dependency order:

**a. Execute.** Dispatch executor agent. The executor follows the task specification and respects CONTEXT.md conventions:
- **Destructive operations gate (binding — from destructive-ops rule):** Before executing any command that mutates external state (databases, Docker volumes, deployed services, APIs, infrastructure, make targets/scripts with unverified side effects), the executor MUST stop and present the operation to the user for explicit yes/no confirmation. Present: what the command does, what state it destroys, whether it's recoverable. Each destructive operation is confirmed individually. Plan approval does not constitute confirmation of destructive commands. When uncertain whether a command is destructive, ask.
- Write and run tests during implementation, not deferred. Test type matches risk: code logic → unit tests, integration points → integration tests.
- Execute the task's **Proof Plan** (from decide). If a required hard check cannot be run, stop and ask before substituting weaker evidence.
- Before working around a missing precondition or unblocking execution through any means other than the planned task steps, evaluate risk: is the workaround reversible (undoable via revert), contained (limited to task-created artifacts), and confident (based on certain knowledge of current state)? If any dimension is unfavorable, stop and surface the blocker to the user. Urgency does not override risk.
- Surface raw evidence to the user as it is produced. Do not summarize into narrative.
- Output a structured discovery assessment after completing the task (see executor agent constraints).

**b–d.** Record, Assess, Route — same as below.

#### Delegated mode
The parent agent orchestrates without implementing tasks directly. For each batch in the dependency graph:

**a. Dispatch.** Spawn executor subagents for each task in the batch (parallel). Each subagent receives: the executor agent definition (`agents/executor.md`) as the governing constraint set, its task specification, acceptance criteria, proof plan, and CONTEXT.md. One subagent per task — consistent with the executor's single-task scope.

**b–d.** For each completed task in the batch (once its subagent returns): Record, Assess, Route — same as below.

All tasks in a batch must complete and pass assessment before the next batch begins.

#### Common steps (both modes)

**b. Record.** Write the execution log entry for this task (see Step 5 format).

**c. Assess.** Dispatch **assessor agent in verify mode** (Type 2) to evaluate the execution results. Mandatory after every task regardless of execution mode. The assessor receives:
- The assessor agent definition (`agents/assessor.md`) — this is the governing specification. Do NOT override the assessor's 6-point check or output vocabulary in the dispatch prompt.
- The task's acceptance criteria and proof plan (from the Plan section)
- The execution log entry just written (from Step b)
- The executor's discovery assessment
- Read access to the changed files, CONTEXT.md, and `foundation/CODE-DESIGN.md`

The assessor runs its 6-point check and returns one of: **proceed**, **blocker-detected**, or **quality-concern** with cited evidence.

Record the checkpoint in the execution log (see Step 5 format).

**d. Route.** Based on the checkpoint result:
- **Proceed**: no blockers, plan still valid. Continue to next task (or next batch in delegated mode).
- **Blocker detected**: checkpoint identified or reclassified a discovery as blocking. Halt execution and route to Step 4.
- **Quality concern**: execution passed but evidence is thin or a gap was flagged. Report to user and ask whether to continue or re-execute the task.
- **Plan drift**: the assessor's plan validity or goal alignment check indicates remaining tasks are no longer valid given accumulated changes. Halt execution, evaluate which completed tasks remain aligned with the objective, and route to Step 4 (drift handling).

Do not proceed to the next task until the checkpoint completes and returns `proceed`.

### 4. Handle blockers and drift
When Step 3d routes here:

**If plan drift**: The assessor flagged that remaining tasks are invalid given what changed. Before classifying scope:
1. List completed tasks and their outputs.
2. Evaluate each against the *current* state of the objective — which are still aligned, which are now incompatible?
3. Report to the user: what drifted, which completed tasks are affected, and whether affected tasks should be kept, reverted, or amended.
4. After user decision on completed work: loop back to decide (re-dispatch the planner with the drift context and retained task outputs as constraints) for a revised plan. The revised plan goes through the plan assessor (Type 1) before act resumes.

**If blocker** (not drift): evaluate the proposed resolution through the risk gate before classifying scope.

**Risk gate**: Assess on three dimensions:
- **Reversible?** Can the action be fully undone by reverting the task's own changes?
- **Contained?** Is the effect limited to artifacts the task is creating, or does it touch pre-existing, shared, or external state?
- **Confident?** Is the agent certain about the current state being modified and the expected outcome?

If any dimension is unfavorable, the resolution requires user approval regardless of scope. Surface the blocker, the proposed fix, and which risk dimensions are unfavorable. Do not proceed autonomously.

After the risk gate clears, classify by scope:

**Trivial** (one-line fix, low-risk, handled inline): already resolved by executor. Note in execution log, continue.

**Notable but non-blocking**: add to `.oodaloop/BACKLOG.md` Next or Later section. Continue.

**Blocking-small** (clear fix, single concern, low-risk): resolve with `/oodaloop-quick`, then resume the current task. No pause needed.

**Blocking-complex** (unclear scope, multi-file, or architectural): pause the current task and spawn a child OODA cycle. Proceed as follows:

**Depth check**: follow `Parent:` references from the current task file back to root. If chain depth ≥ 3, report the full chain to the user and ask before going deeper.

**Select execution strategy** (default: `subagent`; confirm with user or override if a disqualifier applies):

#### Strategy: subagent
The parent agent orchestrates the child OODA cycle by dispatching subagents for each phase, using the task file as the coordination layer.

1. Write the Paused section to the parent task file (format defined in state-hygiene rule). Set `Strategy: subagent`.
2. Spawn a subagent (readonly) for **observe**: provide the observe skill path, `.oodaloop/CONTEXT.md`, the parent's Paused section context (blocker description, child objective), and `Parent: <current-task-slug>`. The subagent creates the child task file.
3. Check the child task file exists and has Requirements + Observations. If malformed, report and ask user.
4. Spawn a subagent (readonly) for **orient**: provide the orient skill path and the child task file. The subagent appends the Assessment section.
5. Spawn a subagent (readonly) for **decide**: provide the decide skill path and the child task file. The subagent appends the Plan section.
6. Spawn a subagent (read/write) for **act**: provide the act skill path, the child task file, and CONTEXT.md. The subagent executes the plan (including its own checkpoints).
7. Spawn a subagent (readonly) for **loop**: provide the loop skill path, the child task file, and CONTEXT.md. The subagent emits a verdict.
8. Read the verdict from the child task file:
   - **CONTINUE**: child resolved the blocker. Delete the child task file (loop left it for us to read). Remove parent's Paused section, set parent phase to `act`, resume execution at the task that was blocked.
   - **REFINE/RESCOPE**: child needs more work. Report to user with the verdict and ask how to proceed.

Between each subagent dispatch, read the child task file to verify the expected section was written. If a subagent fails or produces malformed output, report the failure to the user rather than retrying silently.

#### Strategy: new-chat
For complex blockers requiring fresh context or significant user judgment.

1. Write the Paused section to the parent task file (format defined in state-hygiene rule). Set `Strategy: new-chat`.
2. Report to the user: what was discovered, why it blocks, the child objective, and instruct them to start a new conversation and run `/oodaloop-start` (which will detect the paused parent and pending child via sync).
3. Stop execution. The parent resumes when the child completes and loop un-pauses it.

#### Strategy: in-chat
For moderate blockers where context isn't exhausted and the child cycle is expected to be short.

1. Write the Paused section to the parent task file. Set `Strategy: in-chat`.
2. Run the child OODA cycle directly in the current conversation: observe → orient → decide → act → loop.
3. On child CONTINUE: remove parent's Paused section, set parent phase to `act`, resume execution.
4. On child REFINE/RESCOPE: continue the child cycle until it reaches CONTINUE, or escalate to `new-chat` if context is running low.

### 5. Execution log format
After each task (Step 3b), append to the task file. After each checkpoint (Step 3c), append the checkpoint block to the same task entry.

```markdown
## Execution Log

### T1: <title>
**Status**: done | blocked | escalated
**Changes**: <files modified, created, deleted>
**Proof Plan Compliance**: full | partial | blocked (<reason>)
**Proof**: <raw output — paste actual test results, command output, diffs. Not descriptions of them. If output is long, paste the critical portion and state what was truncated.>
**Gaps**: <anything skipped, untested, uncertain, or where a lower evidence tier was used and why>
**Discoveries**: <executor's structured discovery assessment — classification, evidence, rationale per finding. "No discoveries" if none.>
**Backlog additions**: <items added to BACKLOG.md, if any>

**Checkpoint**: proceed | blocker-detected | quality-concern
**Checkpoint evidence**: <what the assessor verified — specific file paths, line ranges, output checked, criteria compared. Not "looks good.">
**Checkpoint reclassifications**: <any executor discoveries the assessor reclassified, with rationale. "None" if all confirmed.>
**Design review**: <structural limit flags (file sizes, function lengths), composition concerns, red flags, refactor opportunities. "Clean" only if limits were checked and nothing flagged.>
**Plan validity**: <are remaining tasks still valid? Does the goal still make sense given what the codebase actually looks like?>

### T2: ...
```

### 6. Update task file phase
After all tasks complete, set task file phase to `loop`. Update timestamp.

## Output

- Execution log appended to task file with evidence per task
- Task file phase advanced to `loop`
- Summary reported with recommendation to proceed to `/oodaloop-loop`
