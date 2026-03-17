# OODALOOP Deconfliction Checklist

## Purpose

Prevent plugin interference and process bloat before OODALOOP implementation begins.

This checklist is a **hard gate**: do not start building plugin components until all "Now" items are done.

---

## Now (Blockers)

- [ ] Confirm `PLUGIN-AUDIT.md` is current for this workspace/session.
- [ ] Disable `superpowers` in this workspace before implementation starts.
- [ ] Decide whether to temporarily disable `continual-learning` during architecture-heavy iterations.
- [ ] Keep `create-plugin` enabled.
- [ ] Keep `cursor-team-kit` enabled (selective use only).
- [ ] Record the active plugin decision set in `.oodaloop/STATE.md` under a "Deconfliction" section when OODALOOP state files are initialized.
- [ ] Confirm the build runner understands: marketplace plugins are immutable dependencies (no hand edits in cache).
- [ ] Confirm OODALOOP precedence rule: when behavior conflicts occur, OODALOOP contracts win.

---

## During Build (Enforcement)

- [ ] For every imported external pattern, classify as:
  - `adopt unchanged`
  - `adapt for OODALOOP`
  - `reject as bloat`
- [ ] Reject any unconditional hard-gate flow for trivial tasks.
- [ ] Reject any global context injection behavior in OODALOOP v1.
- [ ] Require fast-path support for low-risk/local changes.
- [ ] Keep one canonical source for each concept (no duplicate state/progress artifacts).
- [ ] Run a subtraction pass at the end of each milestone: remove anything that does not increase reliability, clarity, or throughput.

---

## Before v1 Completion

- [ ] Re-run plugin overlap audit and update `PLUGIN-AUDIT.md`.
- [ ] Validate that OODALOOP can run end-to-end without `superpowers`.
- [ ] Verify external dependencies are optional where possible.
- [ ] Document "kept external vs absorbed into OODALOOP" in `ARCHITECTURE.md`.
- [ ] Confirm no hidden workflow coupling to disabled plugins.

---

## Simplicity Test (Jobs Filter)

A design change passes only if all are true:

1. It reduces user-facing complexity.
2. It preserves or improves reliability.
3. It reduces or contains cognitive load for the orchestrator.
4. It does not introduce duplicate control surfaces.
5. It is explainable in a few sentences without losing precision.

If any fail, simplify or remove.
