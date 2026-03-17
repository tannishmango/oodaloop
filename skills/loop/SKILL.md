---
name: loop
description: Sentinel reassessment, learning absorption, and task lifecycle management.
---

## Trigger

`/oodaloop-loop` or after Act phase completion.

## Preconditions

- An active task file (`.oodaloop/<slug>.task.md`) must exist with Verification section.
- `.oodaloop/CONTEXT.md` must exist.

## Workflow

### 1. Read state
Read the active task file (all sections). Read `.oodaloop/CONTEXT.md` for persistent context and active decisions.

### 2. Assess
Dispatch sentinel agent (readonly). Evaluate:
- Are original assumptions still valid?
- Has scope drifted from what was planned?
- Were there unexpected discoveries during execution?
- Are verification results acceptable?
- Have repo conventions changed during this cycle?

### 3. Emit verdict
Exactly one of:
- **CONTINUE**: all tasks passed, scope held. Proceed to next task or close.
- **REFINE**: some tasks need adjustment. Specify which tasks to re-plan or re-execute. Re-enter decide.
- **RESCOPE**: fundamental assumptions changed. Re-enter observe with new evidence.

Each verdict must include: evidence, rationale, confidence level, and next recommended command.

### 4. Absorb learnings into CONTEXT.md
Extract durable knowledge from this task cycle and update CONTEXT.md:
- **Decisions**: add new decisions with date and rationale to the Decisions section.
- **Architecture**: update if structural patterns were discovered or changed.
- **Conventions**: update if conventions changed during this cycle.
- Do NOT add task-specific details. Only absorb what future tasks need to know.

Update the "Last refreshed" timestamp.

### 5. Update backlog
Read `.oodaloop/BACKLOG.md`. Update it:
- **Add**: any discoveries from this cycle that represent future work (non-blocking issues found, improvement ideas, deferred scope items).
- **Promote**: if this cycle's results make a Later item urgent, move it to Next.
- **Complete**: if this cycle finished a backlog item, move it to Done.
- **Prune**: if any item is now obsolete or absorbed, remove it.

When recommending next steps to the user, reference the top items from the Next section.

### 6. Handle task file lifecycle
- If verdict is **CONTINUE** and all work is complete: append the verdict to the task file, then **delete the task file**. The learnings now live in CONTEXT.md.
- If verdict is **REFINE**: append verdict, keep task file, update phase to `decide`.
- If verdict is **RESCOPE**: append verdict, keep task file, update phase to `observe`.

### 7. Report
Report verdict, absorbed learnings, and next step to the user.

## Output

- Verdict appended to task file
- `.oodaloop/CONTEXT.md` updated with absorbed learnings
- `.oodaloop/BACKLOG.md` updated with discoveries, promotions, completions
- Task file deleted (CONTINUE) or phase updated (REFINE/RESCOPE)
- Verdict and next-step recommendation reported to user (referencing top backlog items)
