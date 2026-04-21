# OODALOOP Improvements

## Purpose

Master tracker for framework-level improvements identified during the adversarial review on 2026-04-20 plus subsequent operational observations from real usage. Source of rich context (problem, evidence, recommendation, acceptance) for each item. Survives across sessions.

This doc is the canonical tracker. `.oodaloop/BACKLOG.md` is intentionally **not** used for these items — entries here are too long-form for that format, and BACKLOG is a target-project primitive, not a framework-self-improvement primitive.

## Working protocol

When an item moves to **Active** and an implementing agent begins work, the agent must:

1. Read the entry in full.
2. Walk the user through the **Problem** and **Evidence** sections in conversation. Confirm shared understanding before proceeding.
3. Walk the user through the **Recommendation** and **Acceptance** criteria. Surface assumptions, alternative approaches, and tradeoffs that aren't obvious from the entry.
4. Ask for explicit feedback and approval before any implementation step.
5. Only after explicit user approval, begin implementation. Standard OODALOOP cycle (`/oodaloop-observe` → `/oodaloop-orient` → ... → `/oodaloop-loop`) applies from this point.

The walkthrough is not ceremony. Every item carries non-trivial design decisions that were debated. The walkthrough exposes those debates so the user can adjust scope or approach before mechanical work begins. This protocol is itself a small example of the mechanism-vs-process distinction below: the contract is "agent must walk through and obtain approval," and the mechanism is the user's ability to refuse or redirect.

## Status legend

- **Active** — currently being worked on. Keep to one or two items maximum to prevent thrash.
- **Next** — scoped, ready to start when current Active finishes. Order within Next is roughly priority but can be reordered.

When an item is completed: append a summary to `CHANGELOG.md` under `[Unreleased]`, then delete the entry from this doc.

---

## Cross-cutting context

Two observations from the review unify many of the individual items below. Reading these gives the "why" behind the prioritization.

### A. Mechanism vs process

The framework's existing risk is **not** primarily over-process — it's performative gates (steelman, pre-mortem, falsifiability statements, multi-way classifications) that degrade into template-filling under load. The fix is **not** more such gates.

- **Mechanize when the contract is a fact** (vocabulary, schema, integrity, presence). These are cheap to check, invisible when correct, loud when violated. They don't add ceremony to the happy path.
- **Leave as prose when the contract is judgment** (was the steelman strong? did the heuristic apply? is this discovery notable?). Mechanizing judgment produces theater.
- **Delete when the prose contract is a judgment proxy that has degraded into template-filling.** If the steelmans in actual transcripts are mostly one-liners, the gate is theater that survived.

This drives I-1 (mechanize what's already specified), I-12 (audit performative gates after the cycle log gives data), and the general restraint applied throughout this doc against adding new prose contracts.

### B. Rich classification vocabulary, no decision rules

OODALOOP has rich slot vocabulary (CONTINUE/REFINE/RESCOPE; trivial/notable/blocking-small/blocking-complex; direct/delegated; subagent/in-chat/new-chat; unit/integration/e2e) but no triggers that distinguish slots. Under cost asymmetry, agents collapse to the cheapest slot every time:

- Discovery → always `trivial`
- Verdict → always `CONTINUE`
- Strategy → always default
- Test type → always `unit` (M3.7 was the fix for the test-type version of this exact pattern)

The fix is not more vocabulary. It's **positive triggers attached to existing categories** — checkable signals that say "consider this category seriously." Decision still belongs to the agent. This drives I-3, I-4, I-5.

---

## Active

### I-2: Subagent strategy disqualification for safety-critical chains

**Source.** Adversarial review F4. User confirmed: "framework tends to send agents hard into dangerous things without any second thought. This occurs more frequently with this framework than with just regular agent prompting."
**Confidence.** high.

**Problem.** Both the depth-3 consent gate and the destructive-ops confirmation are specified to "ask the user," but in the default `subagent` execution strategy, the asking agent has no human interlocutor — and the skill doesn't define how the request bubbles up. Behavior is undefined and host-dependent at the most safety-critical moment. The framework's user-observed tendency to push agents into dangerous actions is amplified by subagent strategy, where each level down the chain has weaker judgment context than its parent.

**Evidence.**
- `skills/act/SKILL.md` lines 113–114 (depth check requires asking the user)
- `skills/act/SKILL.md` lines 117–131 (subagent strategy steps; no consent-bubble protocol defined)
- `rules/destructive-ops.mdc` lines 26–35 (explicit user ask required for any external-state mutation)
- User-reported pattern: framework biases harder than baseline prompting toward dangerous actions

**Recommendation.** Hard-disqualify the `subagent` strategy when **either** condition holds:
- Chain depth at dispatch is already ≥ 1 (i.e., we're already inside a child cycle), OR
- Active plan contains any task with `**Destructive**: yes` flag

When disqualified, `act/SKILL.md` Step 4 must select between `in-chat` and `new-chat`. The user-facing agent always remains the orchestrator for safety-critical surfaces. Update the strategy-selection text at `act/SKILL.md` line 115 to enumerate the disqualifier explicitly.

**Acceptance.**
- `act/SKILL.md` Strategy: subagent section documents the disqualifier and the reasoning.
- A test scenario (manually constructed) where a chain would cross the disqualifier produces an `in-chat` or `new-chat` strategy selection, not `subagent`.
- The 8-field Paused section format is reviewed for whether all 8 fields remain necessary when subagent strategy is restricted to depth-0 cycles. Likely deletion candidate during I-13.

**Notes.**
- Reduces parallelism in deep chains. User has confirmed deep chains never fire in practice (see I-3), so the cost is hypothetical.
- Cycle log (I-1) will reveal whether subagent strategy ever fires; if not, the entire strategy is a deletion candidate during I-13.
- Connects to I-13 bloat audit: subagent strategy machinery (Paused section, three execution strategies, sub-cycle dispatch) may be largely deletable.

---

## Next

Listed in roughly recommended order, but not strictly sequenced. Each item is independently scoped.

### I-3: Subloops actually fire — external triggers in assessor Type 2

**Source.** New operational failure observed in real usage. User reported: "oodaloop basically never starts subloops. It just doesn't work and is not easily tracked at all. This could benefit from recursive mechanical procedures enforcement I think. But that alone likely isn't full solution."
**Confidence.** high (operational observation).

**Problem.** Cost asymmetry on the executor's escalation decision drives the four-way classification (`trivial / notable / blocking-small / blocking-complex`) to collapse to `trivial` in practice. The path of least resistance is "patch inline + dump to BACKLOG." Spawning a child cycle costs many turns: pause the parent, write the 8-field Paused section, spawn observe → orient → decide → act → loop subagents in sequence, read each result, resume the parent. Honest classification as `blocking-complex` is punished by ceremony.

Compounding: classification is **self-reported by the agent that benefits from cheaper classification**. The assessor in Type 2 reviews the classification (`agents/assessor.md` line 52: "confirm or reclassify each finding") but reviews don't generate escalations — they confirm or downgrade them.

**Evidence.**
- `agents/executor.md` discovery output structure lines 25–30: no positive criteria pushing toward escalation, only definitions of categories
- `agents/assessor.md` Type 2 check 2 (line 52): only "confirm or reclassify" — no positive trigger to upgrade
- User-reported operational pattern: subloops never fire across many cycles
- Once cycle log (I-1) lands, this becomes empirically measurable rather than gut-felt

**Recommendation.** Add **external triggers** to the assessor's Type 2 checkpoint, separate from the executor's self-report. When any trigger fires, the assessor must consciously decide *not* to escalate, with stated reasoning recorded in the checkpoint output.

Concrete triggers (all mechanical, all checkable by the assessor):
- **Scope expansion**: changed files set ⊋ files anticipated in acceptance criteria
- **Cross-cutting language**: executor's discovery prose matches `"throughout the codebase"`, `"many places"`, `"across the repo"`, `"architectural"`, `"system-wide"`, or similar patterns
- **BACKLOG growth**: task added > 2 items to BACKLOG mid-execution
- **Multi-file mutation**: in a task scoped to single file in the plan, the executor modified > 1 file

The triggers identify candidates for escalation. Final classification still requires judgment. The trigger forbids unconscious downgrading.

**Acceptance.**
- `agents/assessor.md` Verify Mode (Type 2) section includes the external triggers either as part of the 6-point check or as a 7th point ("Discovery escalation triggers").
- `act/SKILL.md` Step 3c references the trigger requirement when describing assessor dispatch.
- After 10+ real cycles with cycle log enabled (I-1), subloop firing rate is measurable. Tune trigger thresholds against observed data.

**Notes.**
- Depends on I-1 (cycle log) for empirical validation. Trigger thresholds may need tuning.
- The four-way discovery classification may simplify to two-way (`continue` / `escalate`) once data shows whether intermediate classifications add value. Defer that decision to I-13 (bloat audit).
- Not process tyranny: triggers are facts (file counts, prose patterns) attached to existing slots. No new ceremony, no agent action required unless trigger fires.
- User noted "that alone likely isn't full solution" — agreed. The deeper issue is incentive asymmetry, which triggers can mitigate but not fully eliminate. Empirical data will reveal whether triggers are sufficient or whether deeper redesign (e.g., separating decision authority from execution authority on escalation) is needed.

---

### I-4: Verdict actually distinguishes — invert prompt + mechanical triggers in loop

**Source.** New operational failure observed in real usage. User reported: "oodaloop does not ever really circle back to replan after implementing. it never suggests it. so clearly that isn't working."
**Confidence.** high (operational observation).

**Problem.** Same shape as I-3. The verdict mechanism has slots (CONTINUE/REFINE/RESCOPE) but no positive triggers for non-CONTINUE. CONTINUE closes the cycle; REFINE re-enters decide; RESCOPE re-enters observe. Each non-CONTINUE outcome is more turns of work for the same human-perceived progress. The Type 3 assess mode (`agents/assessor.md` lines 65–73) lists 5 checks all framed as "look for issues" — no positive heuristic that says "if you observe X, the answer is REFINE." Result: always CONTINUE.

**Evidence.**
- `agents/assessor.md` Type 3 Assess Mode lines 65–73 (5 checks, no positive triggers for non-CONTINUE)
- `skills/loop/SKILL.md` Step 3 (verdict required, no positive bias)
- User-reported operational pattern: verdict always CONTINUE
- Boyd's actual model (per user clarification) explicitly supports stopping and jumping back at any point if current path is deemed to fail. The framework's mechanism encodes this but never invokes it.

**Recommendation.** Two changes.

1. **Invert the verdict prompt** in `loop/SKILL.md` Step 2. Don't ask the assessor "what's the verdict?" Ask:
   > Steelman the case for REFINE. Steelman the case for RESCOPE. If neither steelman exceeds one paragraph of substantive argument, the verdict is CONTINUE.

   This applies the framework's own steelman discipline to its own verdict mechanism. Reverses the burden: REFINE/RESCOPE are the considered outcomes, CONTINUE is the residual.

2. **Add mechanical triggers** for REFINE/RESCOPE candidates in the assessor Type 3 spec:
   - Final commit set ⊋ files anticipated in plan → REFINE candidate
   - Tests required > 1 retry to pass → REFINE candidate
   - BACKLOG gained > 3 items during cycle → RESCOPE candidate
   - User response during cycle contained substantive correction (negation words, scope changes, "actually" / "instead" / "no, do X" patterns) → RESCOPE candidate

   Triggers identify candidates; agent still writes the steelman; verdict still requires judgment.

**Acceptance.**
- `loop/SKILL.md` Step 2 prompt is inverted as specified.
- `agents/assessor.md` Type 3 includes the four mechanical triggers.
- After 10+ real cycles with cycle log enabled (I-1), REFINE/RESCOPE rates are measurable. If still ≈ 0, the triggers are too weak and need tuning, OR the verdict mechanism is genuinely vestigial and should be considered for simplification under I-13.

**Notes.**
- Depends on I-1 (cycle log) for empirical validation.
- Risk: over-triggering REFINE creates churn. The steelman threshold (one substantive paragraph) is the moderating gate.
- Boyd context: user explicitly noted Boyd "considered at any point stopping and jumping back if current path is deemed to fail." This fix operationalizes that. The previous review's framing critique of Boyd-fidelity is retracted; the substance of jump-back is captured here.

---

### I-5: Proof-first — test must exist and fail before implementation when proof plan names a test

**Source.** New operational failure observed in real usage. User reported: "oodaloop doesn't really ever yield proof. it doesn't do any TDD. It doesn't try to write code for expected outputs or tests prior to implementation. Though, it does include documented expected results/outputs."
**Confidence.** high (operational observation).

**Problem.** The framework documents expected outputs in two places — task acceptance criteria and proof plans — but neither becomes code before implementation. The executor reads the proof plan, writes the implementation, then runs the proof. The proof plan is a verification step, not a specification primitive that constrains implementation order.

Combined with the executor's bias toward "make the test pass" rather than "make the implementation true," this produces the well-known anti-pattern: implementation passes the test that was selected to pass it, rather than implementation that satisfies a test written from the spec.

The framework already has the mechanism (proof plan with named test commands). It just doesn't sequence it correctly. M3.7's test-rigor work added "match test type to risk" — useful, but it's about *what kind* of test, not *when* the test exists.

**Evidence.**
- `skills/act/SKILL.md` Step 3a executor flow: "Execute the task's Proof Plan (from decide). If a required hard check cannot be run, stop and ask before substituting weaker evidence." No order constraint.
- `agents/executor.md` constraints: confront hardest test, match rigor to risk — no constraint on order
- `skills/decide/SKILL.md` Step 3: Proof Plan defined as "commands + expected evidence tier + any gating prerequisites" — no order requirement
- User-reported operational pattern: tests written after implementation, or pre-existing tests confirmed without new fixtures

**Recommendation.** Add one constraint to the executor in `agents/executor.md` and reference it from `skills/act/SKILL.md` Step 3a:

> If the task's Proof Plan names an automated test command (pytest, jest, mocha, cargo test, go test, etc.), the test fixture must exist and **fail** before any implementation code is written. Then implement. Then verify the test now passes. Tasks whose proof is non-test (read-only inspection, config validation, file existence checks, manual verification) are exempt.

Mechanizable check in the assessor's Type 2 verification: confirm via git history that the test commit precedes the implementation commit. If both were added in the same commit, the proof plan was satisfied as paperwork, not as proof.

**Acceptance.**
- `agents/executor.md` includes the proof-first constraint as one of its bulleted constraints.
- `skills/act/SKILL.md` Step 3a references the constraint.
- `agents/assessor.md` Type 2 includes the git-history check as part of evidence quality verification (point 6).
- After 5+ cycles with this in place, proof-first compliance is observable in commit history of executed tasks.

**Notes.**
- Not blanket TDD. The constraint applies only when the proof plan names a test command. Refactors and tasks with non-test proof are exempt.
- Risk: creates friction on tasks where the test fixture is itself substantial work. Mitigate by allowing a "scaffold the test, get it failing, then implement" loop — the constraint requires the test to exist and fail, not to be in final form.
- Connects to the broader "yield proof" gap: the framework records expected outputs as English (acceptance criteria) but doesn't operationalize them. This fix operationalizes one slice (test commands). A future improvement may extend to non-test proof plans (e.g., "expected output shape" as a JSON schema enforced by a checker).
- This is the operational-failure version of the mechanism-vs-process pattern: the mechanism exists (proof plan) but isn't used to constrain order. Adding the order constraint is mechanism, not new process.

---

### I-6: Concurrency — claim correction + advisory lockfile

**Source.** Adversarial review F3. User confirmed: "we have not properly added either lockfile handling or git branching (branching tends to get complicated but I know frameworks are developing solid git branching strategies)."
**Confidence.** high (claim correction); medium (lockfile design — needs more thought during walkthrough).

**Problem.** Two simultaneous OODA cycles racing on `BACKLOG.md` or `CONTEXT.md` will silently corrupt one of the writes. Nothing in the framework guards this, and `ARCHITECTURE.md` line 142 markets the substrate as "Multi-task ready." The two scenarios that break this are routine: two terminal tabs on the same project, or one terminal running a delegated batch where two parallel executors both surface a notable discovery. State-hygiene (`rules/state-hygiene.mdc` lines 53–74) lists 17 detection checks; none target concurrent-write conflicts.

**Evidence.**
- `ARCHITECTURE.md` line 142 ("Multi-task ready" claim)
- `skills/loop/SKILL.md` Steps 4 & 5 (read-then-write of CONTEXT.md and BACKLOG.md)
- `skills/act/SKILL.md` Step 4 (BACKLOG.md mid-execution writes from multiple tasks)
- `rules/state-hygiene.mdc` lines 53–74 (no concurrency checks)

**Recommendation.** Two changes.

1. **Replace the marketing claim.** Edit `ARCHITECTURE.md` line 142 to read: *"Designed for single active cycle today; concurrent-cycle safety on shared persistent state (BACKLOG.md, CONTEXT.md) is open work."* Add a corresponding "Known Scope" mention in `README.md`.

2. **Add advisory lockfile.** Cheapest first move:
   - On any read-modify-write of `BACKLOG.md` or `CONTEXT.md`, the writing skill creates `.oodaloop/.lock` containing PID, timestamp, slug, and target file. Releases on completion.
   - On entry, any skill that intends to write shared state checks for `.oodaloop/.lock` with TTL (e.g., 30 minutes). If present and not expired, prompts: *"Another OODALOOP cycle (slug=X, started Y ago) is updating shared state. Wait, abort, or override (with risk acknowledgment)?"*
   - State-hygiene rule gains a check: stale lockfile (TTL exceeded) is reported and the user can release manually.

**Acceptance.**
- `ARCHITECTURE.md` and `README.md` claim corrections shipped.
- Lockfile mechanism implemented in `skills/loop/SKILL.md` Steps 4 & 5 and `skills/act/SKILL.md` Step 4 (mid-execution BACKLOG writes).
- `rules/state-hygiene.mdc` includes stale-lockfile detection (and the mechanical validator from I-1 enforces it).
- A manual test: two simultaneous loop verdicts produce a clear interaction prompt rather than silent last-writer-wins.

**Notes.**
- Git branching is the bigger concurrency story and is explicitly deferred. User noted it tends to get complicated; treat as separate future work, not part of this item.
- Lockfile design is intentionally simple (advisory, TTL, prompts the user). Distributed locking, file-based atomic operations, or version-stamped CRDTs are over-engineering for this use case.
- Connects to I-1: the state-hygiene mechanical validator should include stale-lockfile detection once this lands.

---

### I-7: Move SYSTEMS-REFERENCE.md out of foundation/

**Source.** Adversarial review F2. User clarified: "intended to be a broader index we add things to to occasionally reference when making updates to the oodaloop framework itself. We can move it to a dedicated directory for such files and document that. It's related to principles-curator skill."
**Confidence.** high.

**Problem.** `foundation/SYSTEMS-REFERENCE.md` (193 lines) is loaded by zero runtime skills, agents, or rules. Mentions are limited to file listings and the principles-curator's editing reference. Its presence in `foundation/` (alongside load-bearing PRINCIPLES.md, PRINCIPLES-COMPRESSED.md, CODE-DESIGN.md) makes the doctrine layer's coherence fake — half is loaded, half is reading material.

**Evidence.**
- Grep for `SYSTEMS-REFERENCE` shows hits in: `ARCHITECTURE.md` (file listing), `.oodaloop/CONTEXT.md` (architectural prose), `.cursor/skills/principles-curator/SKILL.md` (editing reference). No phase skill, no agent, no rule.
- Compare PRINCIPLES-COMPRESSED.md (loaded by all 5 phase skills) and CODE-DESIGN.md (loaded by act + assessor).

**Recommendation.** Create `reference/` directory at repo root (sibling of `foundation/`). Move `SYSTEMS-REFERENCE.md` there. Update its header to state:

> **Curator workspace.** Index of cross-domain thinkers, concepts, and frameworks consulted when updating OODALOOP itself. Not loaded by any runtime skill. See `principles-curator` skill for editing protocol.

Update references:
- `ARCHITECTURE.md` "Plugin Structure" section (move from `foundation/` to `reference/`)
- `.oodaloop/CONTEXT.md` Architecture section (remove SYSTEMS-REFERENCE.md from the doctrine list)
- `.cursor/skills/principles-curator/SKILL.md` Step 0 path

**Acceptance.**
- File moved to `reference/SYSTEMS-REFERENCE.md`.
- All references updated.
- Header documents its role and excludes it from "loaded by skills" claims.
- Principles-curator skill still works against the new path.

**Notes.**
- Preserves the curator workflow (which the user values) while removing the "doctrine but unread" smell.
- Establishes the pattern: `foundation/` is loaded by skills; `reference/` is consulted by humans/curators. Future similar files (e.g., research notes, weekly reviews, design exploration) go in `reference/`.

---

### I-8: Rename "convention drift" → "config drift"

**Source.** Adversarial review F6. User agreed.
**Confidence.** high.

**Problem.** `skills/observe/SKILL.md` Step 2 detects only changes to config files (sentinel-file presence). Behavioral conventions (test policy, PR norms, code-review practice agreed in Slack) silently desync. Section is named "Check for convention drift" — promises more than it delivers.

**Evidence.** `skills/observe/SKILL.md` Step 2 lines 28–46 (sentinel files only). CONTEXT.md `Conventions` section header in templates and current state.

**Recommendation.** Rename:
- `skills/observe/SKILL.md` Step 2 header from "Check for convention drift" to "Check for config drift."
- Detection logic and sentinel-file tables remain unchanged (they're correct for what they do).

Optionally: add a sync-time prompt asking the user "any team conventions changed in the last week that aren't in CONTEXT.md?" This is the only honest behavioral-drift detector — the user. Discuss during walkthrough whether to include this prompt or skip it (avoiding new friction on every sync).

**Acceptance.**
- Section renamed.
- Optional: sync skill includes the behavioral-drift prompt as part of staleness check, gated by whether it adds value vs friction.

**Notes.**
- Pure naming fix (or naming fix + small optional addition). Cheapest item in this list.

---

### I-9: Split assessor into three single-purpose agents

**Source.** Adversarial review open question OQ1. User said: "performs okay merged but happy to split as I don't think that should add overhead and we don't know for sure."
**Confidence.** medium.

**Problem.** `agents/assessor.md` defines three modes (Plan/Verify/Assess) with substantively different scopes, inputs, outputs, and consumers. Each mode is independently dispatched by a different skill (decide/act/loop). Merging them into one agent file requires every dispatch site to inject mode-vocabulary instructions ("do not override the assessor's checks or scope") to prevent the dispatcher from pulling the wrong section — defensive instructions repeated three times is a smell that the agent definition is doing more than one job.

**Evidence.**
- `agents/assessor.md` lines 14–74 (three modes, semi-independent specs)
- `skills/decide/SKILL.md` Step 8 line 116: "Do NOT override the assessor's checks, mode vocabulary, or output format in the dispatch prompt."
- `skills/act/SKILL.md` Step 3c line 67: same defensive instruction
- `skills/loop/SKILL.md` Step 2 line 28: same defensive instruction

**Recommendation.** Split into three files:
- `agents/plan-assessor.md` (current Type 1 / Plan Mode — dispatched by decide)
- `agents/task-verifier.md` (current Type 2 / Verify Mode — dispatched by act)
- `agents/cycle-assessor.md` (current Type 3 / Assess Mode — dispatched by loop)

Each file has only its mode's spec. Shared constraints (readonly, evidence-contract, falsifiability) repeat as a short common preamble in each. Three identical short preambles is honest and less smelly than one file with mode dispatch.

Update dispatch sites in `decide/SKILL.md` Step 8, `act/SKILL.md` Step 3c, `loop/SKILL.md` Step 2 to reference the specific agent file. Remove the defensive "do not override" instructions — no longer needed when each agent has only one mode.

**Acceptance.**
- Three new agent files exist; old `agents/assessor.md` deleted.
- Dispatch sites updated to use the right agent per phase.
- Defensive "do not override" instructions removed from dispatch sites.
- A test cycle confirms each phase still gets the correct assessment behavior.

**Notes.**
- Risk: splitting may fragment the shared preamble across three files. Acceptable for now; if it becomes annoying, extract to a rule later.
- Net change in line count: roughly neutral. The win is single-purpose specs and cleaner dispatch sites.
- After this lands, future assessment additions (e.g., a fourth mode) become "add a new agent" not "add a fourth section to the god-object."

---

### I-10: Consolidate "Plugin paths" prologue across phase skills + assessor

**Source.** Review consolidation #13.
**Confidence.** medium.

**Problem.** Five identical "Plugin paths" prologues across phase skills (`act/SKILL.md` line 8, `decide/SKILL.md` line 8, `observe/SKILL.md` line 8, `orient/SKILL.md` line 8, `loop/SKILL.md` line 8) plus `agents/assessor.md` line 12. Each says: *"`foundation/` references in this skill are relative to the OODALOOP plugin root, not the workspace. Resolve from this skill file's installed path."*

The repetition is a smell that this contract belongs in one place.

**Evidence.** Six files with near-identical prologue blocks, all added together in M3.11 per CHANGELOG.

**Recommendation.** Create `rules/plugin-paths.mdc` with `alwaysApply: true` containing the resolution instruction. Remove the prologue from each of the six files.

**Acceptance.**
- New `rules/plugin-paths.mdc` exists and is always-apply.
- Six prologue blocks removed.
- A test cycle in a target project (not OODALOOP itself) confirms agents still resolve `foundation/` paths correctly.

**Notes.**
- After this change, future skills automatically inherit the path resolution guidance without needing a prologue.
- Pairs with I-11 (same pattern, different content). Consider doing them together as one cycle.

---

### I-11: Consolidate doctrine-injection clauses across phase skills

**Source.** Review consolidation #14.
**Confidence.** medium.

**Problem.** Five identical "For non-trivial X, also read `foundation/PRINCIPLES-COMPRESSED.md` and apply only relevant heuristics" clauses across `observe/SKILL.md` line 23, `orient/SKILL.md` line 32, `decide/SKILL.md` line 30, `act/SKILL.md` line 30, `loop/SKILL.md` line 24. Same pattern as I-10 — duplicated soft contract.

Compounding: this is exactly the "verbal contract not mechanically enforced" pattern from F1. There's no way to verify the model loaded the file or applied the heuristic. Either commit to mechanism or accept it's optional and label it as such.

**Evidence.** Five files with near-identical clauses.

**Recommendation.** Decide between two options during walkthrough:

**Option A:** Move into `rules/doctrine-injection.mdc` (or fold into the rule from I-10) as a single always-apply rule. Remove from each skill body.

**Option B:** Soften the language from "must read" to "consider reading" since enforcement is impossible. State explicitly that doctrine application is judgment, not requirement.

Option A keeps the contract but consolidates. Option B is more honest about what the framework can verify. The two are not mutually exclusive — could do A with the softer wording.

**Acceptance.** Per chosen option.

**Notes.**
- This is the second test case for the mechanism-vs-process distinction (after I-1). If I-1's pre-commit checks succeed, the framework gains a track record of mechanizing facts — and the soft-contract pattern here can either be mechanized (if checkable) or honestly relaxed.
- Pairs with I-10. Consider doing them together.

---

### I-12: Performative-gate audit (depends on cycle log data from I-1)

**Source.** Mechanism-vs-process discussion. User concerns about process tyranny while acknowledging some enforcement is needed.
**Confidence.** speculative until cycle log produces data.

**Problem.** Several gates in the framework demand the agent perform an action regardless of state: pre-mortem (`decide/SKILL.md` Step 6), steelman (`decide/SKILL.md` Step 6 + `evidence-contract.mdc`), falsifiability statement (`loop/SKILL.md` Step 3 + `evidence-contract.mdc`), 4-way discovery classification (`agents/executor.md`). These are stated as binding but enforced only by agent self-report.

The risk under the mechanism/process framing: these are performative rather than substantive. They get satisfied with template-filling in practice. If true, deletion improves outcomes (less ceremony, less template-filling, no loss of substantive rigor). The user explicitly endorsed this approach: "must follow points made on Q1 in this prompt about avoiding process tyranny."

**Evidence.** Will be produced by I-1 (cycle log) over time. Until then, the audit is speculative.

**Recommendation.** After I-1 has accumulated 20+ real cycles, sample task files for:

- **Pre-mortem section**: how often does it identify a failure mode that actually occurred during execution? Target: substantial fraction. If near zero, the gate is theater.
- **Steelman section**: how often does it identify the alternative that a future REFINE/RESCOPE adopts? Same logic.
- **Falsifiability statement**: how often is the verdict actually disproven by subsequent evidence? Same logic.
- **Discovery classification**: distribution across the four categories. If always `trivial` (per I-3 prediction), the four-way structure is wasted vocabulary.

For any gate with low utility ratio, propose deletion or simplification in a separate cycle. For gates with high utility ratio, keep as-is and document why.

**Acceptance.**
- After 20+ cycles, sample report produced and shared.
- Deletion proposals (or "keep, here's why") for each audited gate.
- Subsequent cycles implement the deletions.

**Notes.**
- Cannot start until I-1 produces data. Tracked here so the dependency is explicit and the work isn't forgotten.
- Deletion candidates so far (from review): the 8-field Paused section (if subagent strategy is restricted per I-2), the four-way discovery classification (if always trivial per I-3), the three-way verdict (if always CONTINUE despite I-4 triggers).
- This is how bloat reduction happens responsibly: measure, then delete. Not "delete because it feels bloated."

---

### I-13: Bloat audit (depends on cycle log data from I-1 + I-3 + I-4)

**Source.** Open question OQ3. User said: "definitely there is bloat. We don't know how to remove or compress right now. I am sure there are some mechanical process things we could do to enforce behaviors or structures that we could trade off for bloated docs, but must follow points made on Q1 in this prompt about avoiding process tyranny."
**Confidence.** speculative until data accumulates.

**Problem.** ~2000 lines of process specification across `skills/`, `agents/`, `rules/`, `foundation/`, and `ARCHITECTURE.md` to orchestrate a 5-phase loop. Some of this is necessary. Some has accumulated through additive cycles (CHANGELOG shows mostly additions, occasional consolidations). Without data on what fires vs what doesn't, deletion is guesswork that could cause regressions.

User's intuition (which I share): some bloat could be traded off for mechanical enforcement of the same structure. But this requires knowing what's bloated vs. what's actually load-bearing.

**Evidence.** Total spec line count. CHANGELOG additive bias (M3.7 added 5 touchpoints, M3.8 added 7 touchpoints, M4.0 added significant scope, M4.1 added risk gate + destructive ops, M4.2 added more validators).

**Recommendation.** After I-1 + I-3 + I-4 have produced cycle data (target: 20+ real cycles), audit:

- **Sub-cycle strategies (subagent/in-chat/new-chat)**: if cycle log shows zero subloops fire (per I-3 prediction), the entire sub-cycle machinery is currently dead and can be aggressively simplified. Specific candidates: 8-field Paused section format, three-strategy selection logic, Ready-to-Resume section.
- **Verdict slots (CONTINUE/REFINE/RESCOPE)**: if always CONTINUE despite I-4 triggers, the three-way verdict can collapse to two-way (continue / re-enter) or even one-way with explicit "loop again" only when needed.
- **Adapter layer for hosts that aren't being used**: if Claude Code / OpenCode aren't in active use, keep adapters but mark as untested and stop maintaining adapter-specific quirks proactively.
- **Deconfliction section in CONTEXT.md template**: if no plugin conflicts have been encountered in N init runs, simplify or remove.
- **The duplicate prologues already addressed in I-10 and I-11.**

Propose specific deletions in subsequent cycles, not in this one. The audit is the first half; deletion cycles are the second half.

**Acceptance.**
- Deletion candidate list with empirical justification per item.
- One or more subsequent cycles implementing deletions.

**Notes.**
- Strict ordering: I-1 (cycle log) → I-3 + I-4 (triggers fire, give us data on slot collapse) → 20+ cycles → bloat audit. This is the "measure, then delete" approach.
- The risk of premature deletion is the same as the risk of premature abstraction. Wait for data.
- The user's tradeoff intuition is correct: mechanical enforcement of structure (e.g., a validator that requires phase metadata to match sections) makes documentation of the same structure redundant. Once mechanism enforces the fact, the prose explaining the fact becomes deletable. I-1's mechanical validators are the first such trade.

---

## Considered and not added

These were considered during the review and dropped for stated reasons. Captured here so they don't get re-litigated in future reviews.

- **`/oodaloop-quick` exists but is rarely the right call.** No observation data; the design rationale (avoid heavyweight ceremony for trivial work) is sound. Revisit if cycle log shows quick is never used or always inappropriate.
- **`/oodaloop-status` should be a skill, not an inline command.** Style preference; current design is fine. The status command is read-only, has no shared logic worth extracting, and inlining the steps reduces a hop.
- **`principles-curator` skill in `.cursor/skills/` is confused architecture.** Intentional design — project-scoped Cursor skill for editing the plugin, not a runtime component of the plugin. Marked as understood.
- **Boyd-fidelity framing critique.** Retracted after user clarified that jump-back-at-any-point is encoded in the verdict mechanism. The substantive critique (verdict never fires) is captured in I-4.
- **"Assessor god object" framing.** Reframed as I-9 (split decision). The split is happening; the "god object" framing was over-pitched.

---

## Workflow notes

- When an Active item completes: append summary to `CHANGELOG.md` under `[Unreleased]`, then delete the entry from this doc. Do not move to a "Done" section here — CHANGELOG is the canonical history.
- When a Next item moves to Active: copy unchanged to the Active section. Do not edit during the move.
- When discovering a new framework-level improvement during ordinary work: add it to Next here, not to `.oodaloop/BACKLOG.md`. Use the same entry format as the items above.
- This doc itself is subject to future review. If it accumulates more than ~15 entries, consider whether the framework needs a different tracking primitive (it currently doesn't have one — see "OODALOOP has no primitive for multi-issue improvement initiatives" in cross-cutting context).
