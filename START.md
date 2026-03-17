Read these files first:

- `PRINCIPLES.md`
- `SYSTEMS-REFERENCE.md`
- `PLUGIN-AUDIT.md`
- `DECONFLICTION-CHECKLIST.md`
- `PROMPT.md`

Do not edit anything yet.

Your job is to produce a compressed implementation plan for **milestone 1 only**.

You must determine:

1. Which files are permanent doctrine and what permanent repo home they should have.
2. Which files are bootstrap artifacts and what their lifecycle should be after OODALOOP is established.
3. The minimal initial repo structure for this plugin.
4. The minimal valid plugin scaffold to create in this repo.
5. Which parts of the current build prompt belong in milestone 1 versus later milestones.
6. Any blockers, risks, or ambiguities that should be resolved before implementation.

Constraints:

- Optimize for minimum effective process.
- Avoid process theater.
- Keep one canonical copy of each doctrine file.
- Preserve adaptive rigor and fast-path behavior.
- Treat evidence, proof paths, and explicit uncertainty as first-class for non-trivial work.
- Do not overfit to temporary model weaknesses if the mechanism would likely become redundant later.
- Prefer deletable structure over ambitious overbuild.

Return:

1. `Permanent vs Bootstrap Classification`
2. `Proposed Repo Structure`
3. `Bootstrap Artifact Lifecycle`
4. `Milestone 1 Scope`
5. `Non-Goals`
6. `Risks / Open Questions`
7. `Step-by-Step Execution Plan`

Do not scaffold or move files yet. Plan only.

The next agent should have enough context and direction to follow a prompt similar to:

```
Execute the approved milestone 1 plan.

Keep the repo canonical.
Create the permanent doctrine home.
Establish the valid plugin scaffold in this repo.
Create only the minimal coherent component skeletons needed for milestone 1.
Update architecture/docs accordingly.
Do not overbuild.
```
