# OODALOOP Plugin Build Prompt (Cursor-Native, GSD-Aligned)

## Mission

Design and scaffold **OODALOOP**, a Cursor plugin that orchestrates project/feature delivery using an OODA-style loop:

- **Observe** (research + requirements)
- **Orient** (plan + decompose)
- **Decide** (execute)
- **Act** (verify)
- **Loop** (reassess scope based on execution evidence)

The plugin should preserve what works in GSD (tight scope, context isolation, atomic tasking, file-based state), while avoiding ceremony and incorrect assumptions about Cursor internals.

---

## Step 0: Plugin Ecosystem Deconfliction

Before building OODALOOP components, audit installed plugins for overlap and interference.

Rules:

1. Assume marketplace plugins are immutable (do not hand-edit in cache).
2. Classify each plugin capability as `keep external`, `disable`, or `absorb pattern`.
3. Prioritize removal of workflow bloat and rigid global mandates.
4. OODALOOP takes precedence when behavior conflicts occur.
5. Preserve only high-signal capabilities that improve reliability or throughput.

Expected output:

- `PLUGIN-AUDIT.md` with:
  - interference findings
  - keep/disable/absorb matrix
  - concrete deconfliction plan
- `DECONFLICTION-CHECKLIST.md` with explicit `Now / During Build / Before v1` gates

Hard gate:

- Do **not** proceed to implementation until all "Now (Blockers)" items in `DECONFLICTION-CHECKLIST.md` are completed.

---

## First: Assess Before Building

Before implementation, perform a brief assessment and write it to `ARCHITECTURE.md`:

1. Which GSD patterns transfer directly to Cursor.
2. Which patterns need adaptation due to Cursor differences.
3. Which patterns should be dropped (too heavy, redundant, or brittle).
4. Risks if we over-fit to process theater.

If uncertainty exists, prefer simpler mechanisms over speculative complexity.

---

## Non-Negotiable Guardrails

1. **Cursor-native over Claude-native.** Do not copy terminal-centric behavior blindly.
2. **Single source of truth.** Avoid duplicated instructions/state.
3. **Adaptive rigor.** Small asks get lightweight flow; larger asks use full OODA loop.
4. **Evidence-driven looping.** Reassessment uses execution summaries and verification outcomes.
5. **Epistemic discipline over fluent guessing.** Non-trivial claims require evidence, explicit confidence, and surfaced uncertainty.
6. **Plugin validity always.** Manifest, metadata, and component paths must remain valid.

---

## Epistemic Contract

For non-trivial work:

- Prefer executable evidence over narrative assurance: tests, reproductions, runtime checks, invariants, exemplars, or reconciliations.
- When ambiguity, risk, or irreversibility is high, compare at least two plausible options or hypotheses and state why one wins.
- Use TDD or equivalent proof-first loops when behavioral correctness or data trust is central.
- Treat generated data as untrusted until validated against constraints, samples, or reconciliation logic.
- Communicate evidence, confidence, and open uncertainty succinctly in summaries, verification artifacts, and loop verdicts.

---

## Skills / Rules: What To Use

### Required

- `create-plugin-scaffold` skill (scaffold + valid base structure)
- `plugin-quality-gates` rule (manifest/path/frontmatter correctness)

### Useful (use when relevant)

- `review-plugin-submission` skill (marketplace readiness check)
- `check-compiler-errors` skill (if plugin includes TS/JS executable pieces)

### Not required for this build task

- Heavy process-design skills that force long pre-design loops for simple edits.
- CI/PR automation skills unless we are explicitly opening a PR.

---

## Target Output Location

Default plugin location:

`~/.cursor/plugins/local/oodaloop/`

Only use a different location if the user explicitly requests it.

---

## Plugin Scope (v1)

Build a focused plugin with these components:

1. **Commands** (entry points)
   - `/oodaloop-init`
   - `/oodaloop-observe`
   - `/oodaloop-orient`
   - `/oodaloop-decide`
   - `/oodaloop-act`
   - `/oodaloop-loop`
   - `/oodaloop-status`
   - `/oodaloop-quick`

2. **Skills** (procedural knowledge)
   - Init workflow
   - Observe workflow
   - Orient workflow
   - Decide workflow
   - Act workflow
   - Loop reassessment workflow
   - Quick-task workflow

3. **Agents/Subagents** (specialized responsibilities)
   - Researcher (read-heavy discovery)
   - Planner (decomposition + plan creation)
   - Executor (implementation per atomic task)
   - Verifier (acceptance checks + gap reporting)
   - Sentinel (scope reassessment from artifacts/summaries)

4. **Rules**
   - Keep OODALOOP artifacts consistent and minimal.
   - Enforce concise execution summaries with evidence, confidence, and unresolved uncertainty.
   - Enforce traceability from requirement -> plan -> execution -> verification.
   - Require proof paths for behavioral and data-quality claims when the work is non-trivial.

5. **Templates**
   - `.oodaloop/STATE.md`
   - `.oodaloop/PROJECT.md`
   - `.oodaloop/REQUIREMENTS.md`
   - `.oodaloop/ROADMAP.md`
   - `.oodaloop/DECISIONS.md`
   - `.oodaloop/phases/<phase>/PLAN.md`
   - `.oodaloop/phases/<phase>/SUMMARY.md`
   - `.oodaloop/phases/<phase>/VERIFICATION.md`

---

## OODALOOP Runtime Contract

The orchestrator must infer workflow depth from task complexity and existing artifacts:

- If request is trivial and local: run quick flow (minimal ceremony, clear summary).
- If request is multi-step or high-risk: require Observe -> Orient -> Decide -> Act.
- After major phase completion: run Loop reassessment.

The user should not need to manually choose a mode; the plugin adapts.

---

## Loop (Key Differentiator)

`/oodaloop-loop` triggers Sentinel reassessment using:

- `.oodaloop/STATE.md`
- `.oodaloop/ROADMAP.md`
- `.oodaloop/DECISIONS.md`
- recent phase `SUMMARY.md` + `VERIFICATION.md`

Sentinel outputs exactly one:

- `CONTINUE` (scope still valid)
- `REFINE` (adjust upcoming scope/tasks)
- `RESCOPE` (core assumptions broken; redefine forward plan)

Every verdict must include:

1. Evidence
2. Decision rationale
3. Confidence and unresolved uncertainty
4. Required state updates
5. Next recommended command

---

## Practical Translation From GSD

Adopt:

- Atomic task decomposition
- Context isolation per task/subagent
- File-based shared state
- Verification before closure

Adapt:

- Slash-command conventions into Cursor command/skill patterns
- Planner/executor handoff to Cursor agent orchestration semantics

Drop:

- Process overhead that does not improve delivery outcomes
- Runtime assumptions tied to Claude terminal harness internals

---

## Build Sequence

1. Scaffold plugin with valid manifest and component directories.
2. Add commands with clear frontmatter + concise behavior contracts.
3. Add skills for each OODA phase and quick path.
4. Add specialized agents (researcher/planner/executor/verifier/sentinel).
5. Add rules enforcing artifact hygiene and traceability.
6. Add `.oodaloop/` templates.
7. Write docs (`README.md`, `WORKFLOW.md`, `ARCHITECTURE.md`, `CHANGELOG.md`).
8. Validate with plugin quality gates and fix all structural issues.

---

## Definition of Done

The work is complete when:

1. Plugin loads locally from `~/.cursor/plugins/local/oodaloop/`.
2. `plugin.json` is valid and paths are relative.
3. All declared components exist with required metadata/frontmatter.
4. OODA commands map to coherent workflows.
5. Loop command produces explicit `CONTINUE` / `REFINE` / `RESCOPE` output format.
6. Documentation explains usage and design trade-offs clearly.

If any DoD item fails, do not claim completion.
