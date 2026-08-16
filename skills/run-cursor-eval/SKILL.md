---
name: run-cursor-eval
description: Run the complete OODALOOP Level-1 behavioral evaluation in Cursor with one invocation. Use when comparing host-native behavior, current main, PR1, or future harness revisions across the canonical scenario corpus using isolated fresh-context subagents, deterministic semantic grading, observational telemetry, and vector comparison.
---

# Run Cursor eval

Act as the evaluation controller. With no user arguments, run the complete suite
defined in `evals/config.json`; do not ask the user to choose scenario IDs.

## Invariants

- Use Grok 4.6 with high reasoning and Fast disabled for the parent and every child.
- Refuse to begin if that exact model configuration is unavailable or cannot be
  verified. Never silently use Auto, Fast, or another model.
- Give every run a fresh context and isolated worktree/repository.
- Give children only the public task, visible fixture territory, and the selected
  condition instructions. Never give them oracle cases, anchors, protected paths,
  prior results, or this controller skill.
- Hold model, fixture, task, tool policy, and starting context constant across the
  three conditions. Vary only the harness instructions.
- Treat host-native as no injected OODALOOP harness. Hold unavoidable ambient
  Cursor/user configuration constant and disclose it in the report.
- Record a result vector. Never invent a composite score.

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

Use its printed suite directory and `suite.json`. It creates one clean candidate
repository for each scenario × condition cell, without copying hidden grading data.

## 3. Launch isolated children

Launch children in batches up to the configured parallelism. Use Cursor subagents
with isolated worktrees when available; otherwise use the already isolated repos
created by the preparation script. Each child receives only its cell's
`AGENT_TASK.md` and workspace path.

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
and writes per-cell `result.json` plus `comparison.json`.

Never repair a candidate before grading. A failure, child timeout, unavailable
metric, or protocol deviation is data and must remain visible.

## 5. Report

Return the suite ID and exact model configuration; one row per cell with semantic
cases, anchor result, route, framework entry, surprise/reentry, reviewer calls,
questions, proof attempts, tools, tokens/cost, and wall time when available;
directional comparisons by scenario pair; missing telemetry and protocol
deviations; and paths to the comparison and individual results.

Do not declare a harness winner from a single run. Describe directional evidence.
