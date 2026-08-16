---
name: run-cursor-eval
description: Run the complete OODALOOP Level-1 behavioral evaluation in Cursor with one invocation. Use when comparing host-native behavior, current main, PR1, or future harness revisions across the canonical scenario corpus using isolated fresh-context subagents, deterministic semantic grading, observational telemetry, and vector comparison.
---

# Run Cursor eval

Act as the evaluation controller. With no user arguments, run the complete suite
defined in `evals/config.json`; do not ask the user to choose scenario IDs.

## Invariants

- Use Grok 4.6 with high reasoning and Fast disabled for the parent and every child.
- Under the hood, launch every Cursor Task/subagent with
  `model: "cursor-grok-4.6-high"` (the value of `evals/config.json`
  `model.cursor_task_model`). That slug is Grok 4.6 at reasoning effort `high`,
  Fast off. It is not `cursor-grok-4.6-xhigh` (extra-high effort).
- Refuse to begin if that exact slug is unavailable or cannot be verified. Never
  silently substitute Auto, `inherit`, Fast, `cursor-grok-4.6-xhigh`, or another
  model.
- Give every run a fresh context and isolated worktree/repository.
- Give children only the public task, visible fixture territory, and the selected
  condition instructions. Never give them oracle cases, anchors, protected paths,
  prior results, or this controller skill.
- Hold model, fixture, task, tool policy, and starting context constant across the
  three conditions. Vary only the harness instructions.
- Treat host-native as no injected OODALOOP harness. Hold unavoidable ambient
  Cursor/user configuration constant and disclose it in the report.
- Record a result vector. Never invent a composite score.
- Every graded suite must have `evals/runs/<suite_id>/REPORT.md`. That file is the
  human meaning of the run. `finish_suite.py` writes it. If it is missing, run
  `python3 -m evals.runner.report SUITE_DIR` before talking to a human.
- Whenever you communicate to a human about a run, lead with that REPORT: what a
  cell is, what “code worked” vs “behaved as probed” mean, the scoreboard, and
  every miss in English. Do not paste `comparison.json`, check keys
  (`no_framework_state`, `route_normal`, …), or cell ids as the explanation.

## Re-run policy

The full matrix (6 scenarios × 3 conditions × `config.repetitions`) is a
**merge / blast-radius bar**, not a tweak loop. Do not re-run the full matrix
after every tweak.

After a failure or a harness edit, ask: *could this change alter routing, init,
surprise, leaf-readiness, or the injected `.harness/` surface for scenarios I
did not touch?* If a "local" fix required editing start/orient/act/surprise
globally, it was not local.

| Blast radius | What to run |
|---|---|
| Foundation-locked wording (route-before-init strings, model slug, `evals/runs/` contract) | `python3 -m unittest discover -s evals/tests -v` only. No agent cells. |
| One cell or one scenario failed; the fix is local to that task/fixture/oracle | Re-run that scenario across the conditions still under test. Use `repetitions: 1` unless the miss looked like flake (1 of 3 reps). |
| Only one condition's harness changed (e.g. PR1 skill text) | Re-run that condition's cells. Do not spend host-native or `main` cells. |
| Cannot bound the blast radius, or the change is global (routing/init order, surprise/Act interrupts, leaf contract, harness export, model pin) | Expand: all scenarios for the affected condition, or the full matrix. |
| Merge to `main`, or "is this stable?" | Full configured matrix with `repetitions: 3`. |

For a targeted run, temporarily set `evals/config.json` `scenarios` to an id
list and/or `repetitions` to `1`, then restore `scenarios: "all"` and the
default repetitions **before committing** unless the commit is itself a
default-matrix change. Keep the prior `evals/runs/<suite_id>/comparison.json`
as the baseline; compare new cells to those rows rather than throwing the
suite away.

Never repair a failing candidate and call that a rerun. Prepare a new cell.

## 1. Load and validate

Read `evals/config.json`, all `evals/scenarios/public/*.json`, and hidden anchors.
Confirm that every configured scenario exists, all requested fixture overlays can
be materialized, and the configured condition refs resolve. Record exact commits.

Run the deterministic unit suite before spending agent runs:

```sh
python3 -m unittest discover -s evals/tests -v
```

Stop on foundation failure.

## 2. Prepare the matrix

Run:

```sh
python3 skills/run-cursor-eval/scripts/prepare_suite.py
```

Use its printed suite directory and `suite.json`. The printed path defaults to
`evals/runs/<suite_id>/`. Never copy suites to `.archive/`. Candidate workspaces
remain in OS temp; each `cell.json` stores that absolute workspace path. It
creates one clean candidate repository for each scenario × condition ×
`repetitions` cell, without copying hidden grading data.

## 3. Launch isolated children

Launch **every** cell listed in `suite.json`, in batches up to the configured
parallelism. Never hardcode a cell count. Use Cursor subagents with isolated
worktrees when available; otherwise use the already isolated repos created by
the preparation script. Pass `model: "cursor-grok-4.6-high"` on every child Task
call. Each child receives only its cell's `AGENT_TASK.md` and workspace path.

Require each child to work only in its assigned workspace, solve the task normally
with the included condition instructions, run the strongest visible proof, and
finish with a factual summary. Record only events directly visible in its output or
workspace. Do not infer semantic intent from silence.

Append each observed event from the parent context with:

```sh
python3 skills/run-cursor-eval/scripts/record_event.py CELL_DIR EVENT key=value
```

Do not let one child's context or output enter another child's prompt.

## 4. Grade privately

After every child stops, run:

```sh
python3 skills/run-cursor-eval/scripts/finish_suite.py SUITE_DIR
```

The grader imports each candidate outside the child context, runs the fixed and
fixed-seed oracle cases, reduces observed events, applies hidden anchor invariants,
and writes per-cell `result.json`, `comparison.json`, and `REPORT.md`.

Never repair a candidate before grading. A failure, child timeout, unavailable
metric, or protocol deviation is data and must remain visible.

## 5. Report

`finish_suite.py` writes `REPORT.md` next to `comparison.json`. Your user-facing
message **is** that report (or a close paraphrase of *What this run is*, *How to
read a cell*, *Scoreboard*, the scenario implications, and *Every miss, in
English*). Point at `evals/runs/<suite_id>/REPORT.md`.

Do not lead with JSON. Do not declare a harness winner from a single run.
Describe directional evidence in the report's vocabulary.
