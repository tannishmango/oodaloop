---
name: decide
description: Execute plan tasks through the executor agent.
---

## Trigger

`/oodaloop-decide` or transitioning from Orient.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with a Plan section.
- `.oodaloop/CONTEXT.md` must exist.
- Task file phase should be `decide`.

## Workflow

### 1. Read plan and context
Read the active task file's Plan section. Read `.oodaloop/CONTEXT.md` conventions -- these are binding constraints on implementation (commit format, linter rules, test patterns, etc.).
Treat the `Proof Infrastructure` subsection as binding for verification selection:
- choose the strongest available proof command relevant to each task
- only use weaker evidence when stronger checks are unavailable or explicitly blocked

### 2. Execute, assess, repeat
For each task in dependency order:

**a. Execute.** Dispatch executor agent. The executor follows the task specification and respects CONTEXT.md conventions:
- Write and run tests during implementation, not deferred to act. Test type matches risk: code logic → unit tests, integration points → integration tests.
- Execute the task's **Proof Plan** (from orient). If a required hard check cannot be run, stop and ask before substituting weaker evidence.
- Surface raw evidence to the user as it is produced. Do not summarize into narrative.
- Output a structured discovery assessment after completing the task (see executor agent constraints).

**b. Record.** Write the execution log entry for this task (see Step 4 format).

**c. Assess.** Dispatch a readonly subagent to evaluate the execution results. This is mandatory after every task -- it is the mechanism that catches blockers the executor missed or underclassified. The subagent receives:
- The task's acceptance criteria and proof plan (from the Plan section)
- The execution log entry just written (from Step b)
- The executor's discovery assessment
- Read access to the changed files, CONTEXT.md, and `foundation/CODE-DESIGN.md`

The subagent must:
1. **Acceptance check.** Verify the executor's claimed changes against the acceptance criteria.
2. **Discovery review.** Review the executor's discovery assessment -- confirm or reclassify each finding.
3. **Plan validity.** Check whether the remaining plan tasks are still valid given what just changed.
4. **Design review.** Evaluate the implementation against `foundation/CODE-DESIGN.md`:
   - Check structural limits on changed files (file length, function length, nesting depth, parameter count). Flag files crossing thresholds.
   - Assess whether the task's changes fit the codebase's existing patterns or introduce inconsistency. Does the implementation follow the standards visible in surrounding code?
   - Evaluate composition: did the implementation grow an existing component when it should have introduced a new one? Is a refactor of the surrounding code warranted to achieve a more composable design -- even if no pattern existed before?
   - Check for red flags: God objects, copy-paste variants, shotgun surgery, leaky abstractions, dead code.
5. **Goal alignment.** Step back from the task and assess: does this task still make sense in the context of the overall objective? Could the goal be better served by a different approach given what the codebase actually looks like?
6. **Evidence.** Reference specific file paths, line ranges, output, and concrete observations. Generic assessments ("looks good", "no issues") are insufficient -- the assessor must cite what was checked and what was found.

Record the checkpoint in the execution log (see Step 4 format).

**d. Route.** Based on the checkpoint result:
- **Proceed**: no blockers, plan still valid. Continue to next task.
- **Blocker detected**: checkpoint identified or reclassified a discovery as blocking. Halt execution and route to Step 3.
- **Quality concern**: execution passed but evidence is thin or a gap was flagged. Report to user and ask whether to continue or re-execute the task.

Do not proceed to the next task until the checkpoint completes and returns `proceed`.

### 3. Handle blockers
When the checkpoint (Step 2d) routes here, or the executor surfaces a blocking discovery:

**Trivial** (one-line fix, handled inline): already resolved by executor. Note in execution log, continue.

**Notable but non-blocking**: add to `.oodaloop/BACKLOG.md` Next or Later section. Continue.

**Blocking-small** (clear fix, single concern, low risk): resolve with `/oodaloop-quick`, then resume the current task. No pause needed.

**Blocking-complex** (unclear scope, multi-file, or architectural): pause the current task and spawn a child OODA cycle. Proceed as follows:

**Depth check**: follow `Parent:` references from the current task file back to root. If chain depth ≥ 3, report the full chain to the user and ask before going deeper.

**Select execution strategy** (default: `subagent`; confirm with user or override if a disqualifier applies):

#### Strategy: subagent
The parent agent orchestrates the child OODA cycle by dispatching subagents for each phase, using the task file as the coordination layer.

1. Write the Paused section to the parent task file (format defined in state-hygiene rule). Set `Strategy: subagent`.
2. Spawn a subagent (readonly) for **observe**: provide the observe skill path, `.oodaloop/CONTEXT.md`, the parent's Paused section context (blocker description, child objective), and `Parent: <current-task-slug>`. The subagent creates the child task file.
3. Check the child task file exists and has Requirements + Observations. If malformed, report and ask user.
4. Spawn a subagent (readonly) for **orient**: provide the orient skill path and the child task file. The subagent appends the Plan section.
5. Spawn a subagent (read/write) for **decide**: provide the decide skill path, the child task file, and CONTEXT.md. The subagent executes the plan (including its own checkpoints).
6. Spawn a subagent (readonly) for **act**: provide the act skill path and the child task file. The subagent appends Verification.
7. Spawn a subagent (readonly) for **loop**: provide the loop skill path, the child task file, and CONTEXT.md. The subagent emits a verdict.
8. Read the verdict from the child task file:
   - **CONTINUE**: child resolved the blocker. Delete the child task file (loop left it for us to read). Remove parent's Paused section, set parent phase to `decide`, resume execution at the task that was blocked.
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
3. On child CONTINUE: remove parent's Paused section, set parent phase to `decide`, resume execution.
4. On child REFINE/RESCOPE: continue the child cycle until it reaches CONTINUE, or escalate to `new-chat` if context is running low.

### 4. Execution log format
After each task (Step 2b), append to the task file. After each checkpoint (Step 2c), append the checkpoint block to the same task entry.

```markdown
## Execution Log

### T1: <title>
**Status**: done | blocked | escalated
**Changes**: <files modified, created, deleted>
**Proof Plan Compliance**: full | partial | blocked (<reason>)
**Proof**: <raw output -- paste actual test results, command output, diffs. Not descriptions of them. If output is long, paste the critical portion and state what was truncated.>
**Gaps**: <anything skipped, untested, uncertain, or where a lower evidence tier was used and why>
**Discoveries**: <executor's structured discovery assessment -- classification, evidence, rationale per finding. "No discoveries" if none.>
**Backlog additions**: <items added to BACKLOG.md, if any>

**Checkpoint**: proceed | blocker-detected | quality-concern
**Checkpoint evidence**: <what the assessor verified -- specific file paths, line ranges, output checked, criteria compared. Not "looks good.">
**Checkpoint reclassifications**: <any executor discoveries the assessor reclassified, with rationale. "None" if all confirmed.>
**Design review**: <structural limit flags (file sizes, function lengths), composition concerns, red flags, refactor opportunities. "Clean" only if limits were checked and nothing flagged.>
**Plan validity**: <are remaining tasks still valid? Does the goal still make sense given what the codebase actually looks like?>

### T2: ...
```

### 5. Update task file phase
After all batches complete, set task file phase to `act`. Update timestamp.

## Output

- Execution log appended to task file with evidence per task
- Task file phase advanced to `act`
- Summary reported with recommendation to proceed to `/oodaloop-act`
