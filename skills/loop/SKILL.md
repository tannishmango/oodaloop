---
name: loop
description: Assess aggregate outcomes, emit verdict, and manage task lifecycle.
---

> Boyd's Feedback: After acting, observe results and reorient. The loop is continuous — every action's outcome feeds the next cycle. (foundation/OODALOOP.md)

> **Plugin paths**: `foundation/` references in this skill are relative to the OODALOOP plugin root, not the workspace. Resolve from this skill file's installed path.

## Trigger

`/oodaloop-loop` or after Act phase completion.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with Execution Log section.
- `.oodaloop/CONTEXT.md` must exist.

## Workflow

### 1. Read state
Read the active task file (all sections). Read `.oodaloop/CONTEXT.md` for persistent context and active decisions.

For non-trivial rescoping and verdict decisions, also read `foundation/PRINCIPLES-COMPRESSED.md` and apply only relevant heuristics.

### 2. Assess
Dispatch **assessor agent in assess mode** (Type 2, readonly). The assessor receives:
- The assessor agent definition (`agents/assessor.md`) — this is the governing specification. Do NOT override the assessor's checks or scope in the dispatch prompt.
- The full task file (all sections)
- `.oodaloop/CONTEXT.md`

The assessor evaluates aggregate concerns per its Type 2 specification (coherence, cross-cutting consistency, cumulative drift, convention compliance, proof adequacy). It does NOT re-verify individual tasks — Type 1 checkpoints during act already handled per-task verification.

Also evaluate:
- Are original assumptions still valid?
- Has scope drifted from what was planned?
- Were there unexpected discoveries during execution?
- Have repo conventions changed during this cycle?

### 3. Emit verdict
Exactly one of:
- **CONTINUE**: all tasks passed, scope held. Proceed to next task or close.
- **REFINE**: some tasks need adjustment. Specify which tasks to re-plan or re-execute. Re-enter decide.
- **RESCOPE**: fundamental assumptions changed. Re-enter observe with new evidence.

Each verdict must include:
- **Proof references**: cite specific proof artifacts from the cycle (test output, diffs, verification results). Do not issue verdicts backed only by narrative summaries.
- **Proof adequacy**: state whether the executed proof matched each task's Proof Plan and repo proof posture, and whether any downgraded evidence was user-approved.
- **Rationale**: why this verdict and not the alternatives.
- **Falsifiability**: state what evidence would disprove this verdict. If you cannot articulate what would make the verdict wrong, the verdict is not rigorous enough.
- **Confidence level**: and what would increase it.
- **Next recommended command**.

### 4. Absorb learnings into CONTEXT.md
Extract knowledge from this cycle that future tasks would need. Update CONTEXT.md:
- **Decisions**: add if the cycle made a choice that constrains future work (e.g., "chose library X over Y", "adopted pattern Z"). Include date and one-line rationale.
- **Architecture**: update if the cycle revealed or changed structural patterns (e.g., new module boundary, changed entry point, discovered critical path).
- **Conventions**: update if the cycle added or changed a convention (e.g., new test pattern, new commit format rule).

**Do NOT absorb**: execution details (what files were changed, what commands were run), task-specific observations that only matter for this task, or anything already captured in CONTEXT.md.

**Test**: before adding a line, ask "would an agent working on a completely different task need this?" If no, don't add it.

Update the "Last refreshed" timestamp.

### 5. Update backlog
Read `.oodaloop/BACKLOG.md`. Update it:
- **Add**: any discoveries from this cycle that represent future work (non-blocking issues found, improvement ideas, deferred scope items).
- **Promote**: if this cycle's results make a Later item urgent, move it to Next.
- **Complete**: if this cycle finished a backlog item, move it to Done.
- **Prune**: if any item is now obsolete or absorbed, remove it.

When recommending next steps to the user, reference the top items from the Next section.

### 6. Handle task file lifecycle
- If verdict is **REFINE**: append verdict, keep task file, update phase to `decide`.
- If verdict is **RESCOPE**: append verdict, keep task file, update phase to `observe`.
- If verdict is **CONTINUE** and all work is complete: append the verdict to the task file. Then handle parent resumption:

  If this task has **no `Parent:` field**: delete the task file. Learnings now live in CONTEXT.md.

  If this task **has a `Parent:` field**: read the parent task file's Paused section `Strategy` field. Remove the Paused section and set parent phase to `act`. Then handle per strategy:

  - **`subagent`**: the parent agent is orchestrating this child through subagents and will read the verdict from the child task file. Do NOT delete the child task file -- the parent agent is responsible for cleanup after reading the verdict (decide skill Step 3, subagent strategy step 8).
  - **`new-chat`**: delete the child task file, then append a `## Ready to Resume` section to the parent task file:
    ```
    ## Ready to Resume
    Child-completed: <child-slug>
    Child-result: <one-line summary of what the child accomplished>
    Resume-at: <which plan task to resume, from the parent's Resume-instructions>
    Date: <date>
    ```
    This section is read by `/oodaloop-start` (via sync) when the user opens a new conversation. Recommend the user run `/oodaloop-start` to resume.
  - **`in-chat`**: delete the child task file and resume execution of the parent task inline.

### 7. Report
Report verdict, absorbed learnings, and next step to the user.

## Output

- Verdict appended to task file
- `.oodaloop/CONTEXT.md` updated with absorbed learnings
- `.oodaloop/BACKLOG.md` updated with discoveries, promotions, completions
- Task file deleted (CONTINUE) or phase updated (REFINE/RESCOPE)
- Verdict and next-step recommendation reported to user (referencing top backlog items)
