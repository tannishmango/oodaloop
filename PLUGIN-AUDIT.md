# Plugin Ecosystem Audit for OODALOOP

## Objective

Minimize external plugin interference and redundancy while preserving only high-signal capabilities that improve OODALOOP.

This audit treats marketplace plugins as immutable dependencies (no hand edits).  
Strategy is **keep / disable / absorb pattern**.

---

## Installed Plugin Snapshot (from local environment)

- `superpowers`
- `cursor-team-kit`
- `create-plugin`
- `continual-learning`
- `database-skills`
- local skills: `skill-authoring`, `chainalysis-skills-pr`, plus `skills-cursor/*`

---

## High-Risk Interference Findings

1. **`superpowers` session hook injects large mandatory context**
   - Hook script: `hooks/session-start.sh`
   - Injects full `using-superpowers` content into every session as "EXTREMELY_IMPORTANT".
   - Enforces rigid "must use skills first" behavior that can override local process intent.
   - **Impact:** major prompt/context hijack risk, reduced process autonomy, conflict with adaptive rigor.

2. **`superpowers` skills contain universal hard gates**
   - `brainstorming`: requires design + approval before any implementation for every task.
   - `using-superpowers`: "not optional" invocation language.
   - **Impact:** can add ceremony to trivial tasks and conflict with OODALOOP quick-path execution.

3. **`continual-learning` stop hook can introduce autonomous follow-up loops**
   - Hook script emits follow-up message to run continual-learning skill.
   - **Impact:** periodic process detours and memory-update overhead; useful for long-term memory, but noisy during focused build loops.

---

## Medium/Low-Risk Findings

- **`cursor-team-kit` rules are mostly harmless and scoped**
  - `no-inline-imports` and `typescript-exhaustive-switch` are code-quality constraints.
  - **Impact:** low conflict; useful where applicable.

- **`create-plugin` is aligned**
  - `plugin-quality-gates` directly supports OODALOOP plugin correctness.
  - **Impact:** high value, low interference.

- **`database-skills` are domain-specific**
  - Not disruptive unless auto-selected for non-database tasks.
  - **Impact:** low for plugin authoring flow.

---

## Keep / Disable / Absorb Matrix

### Keep as external

- `create-plugin`
  - Keep `create-plugin-scaffold`, `review-plugin-submission`, `plugin-quality-gates`.
- `cursor-team-kit` (selective)
  - Keep practical QA skills (compile checks, CI review) when needed.
- `database-skills`
  - Keep for DB-heavy product tasks; ignore for plugin-core work.

### Disable or deprioritize during OODALOOP development

- `superpowers` (recommended: disable plugin at workspace level while building OODALOOP)
  - Main reason: SessionStart context injection + rigid mandatory process language.
- `continual-learning` (optional: disable during active architecture iterations)
  - Re-enable later if AGENTS memory curation proves beneficial.

### Absorb ideas into OODALOOP (without dependency)

- From `superpowers`:
  - debugging discipline
  - verification-before-completion checks
  - parallel task decomposition heuristics
- From `cursor-team-kit`:
  - smoke-test and compiler-check workflows
  - practical PR/review loops
- From `create-plugin`:
  - manifest/path/frontmatter quality gates

---

## Compression Policy (for OODALOOP)

1. **Default minimal runtime surface**
   - No global mandatory hook text injection in OODALOOP v1.

2. **Policy over prescription**
   - OODALOOP should define outcome contracts (evidence, state update, verification), not force one heavy ritual for all tasks.

3. **Optional rigor modules**
   - Advanced flows (deep planning, extended design, multi-agent review) should be opt-in or auto-triggered by risk/complexity, never unconditional.

4. **Fast path first-class**
   - Preserve a lightweight mode for local changes with mandatory safety minimums only.

---

## Practical Deconfliction Plan

1. Disable `superpowers` for this workspace while building OODALOOP.
2. Optionally disable `continual-learning` during intense iteration windows.
3. Keep `create-plugin` and `cursor-team-kit` enabled.
4. Encode OODALOOP-first behavior in your own commands/skills/rules.
5. After OODALOOP v1 is stable, re-evaluate whether any external plugin remains necessary.

---

## Decision Criteria for Future Plugins

Adopt an external plugin only if it passes all checks:

1. No unconditional global context injection.
2. No one-size-fits-all hard gate that blocks adaptive rigor.
3. Clear measurable value not already covered by OODALOOP.
4. Low maintenance burden and no fragile cross-plugin coupling.
5. Easy to disable without breaking core workflow.

If any check fails, prefer to absorb only the useful pattern into OODALOOP.
