# Behavioral evaluation foundation

This directory is neutral Level-1 infrastructure for comparing host-native work,
current `main`, the last pre-redesign harness, and future harnesses. It has two
independent planes:

- `spec`, `oracle`, and `seed_project` measure black-box semantic correctness.
- `scenarios`, `schemas`, and `runner/telemetry.py` record behavioral trajectories.

In Cursor, install the plugin and invoke `/oodaloop-eval` with no arguments. The
controller reads `config.json`, prepares all six scenarios across host-native,
`pre-redesign`, and `main`, launches isolated fresh-context subagents, and grades the
resulting cells (6 scenarios × 3 conditions × `config.repetitions`). The default model is Grok 4.6 with high reasoning and Fast disabled
(`cursor-grok-4.6-high` for Cursor Task). The controller stops instead of silently
substituting `cursor-grok-4.6-xhigh`, Auto, Fast, or another model. `pre-redesign`
is the annotated tag at `b272352` (last init-first `main` before the redesign
merged).

The full matrix is a protocol-change bar, not a tweak loop and not a post-merge
ritual. Run it when the user invokes `/oodaloop-eval`, or once before landing an
architectural / protocol / process change. Do not run or propose it after merging
a change that already has a `REPORT.md`, or for cleanup, release, docs, or
ordinary commits. After a failure or harness edit, ask whether the change could
alter routing, init, surprise, leaf-readiness, or the injected `.harness/`
surface for scenarios you did not touch. If not, re-run only the affected
scenario or condition (usually with `repetitions: 1`). Foundation tests cover
wording contracts with no agent cells. See `skills/run-cursor-eval/SKILL.md`
**When to run** and **Re-run policy**. Restore `config.json` `scenarios: "all"`
and default repetitions before committing a targeted run.

Run the canonical semantic check from the repository root:

```sh
python3 -m evals.runner.run --condition main
python3 -m unittest discover -s evals/tests -v
```

Grade another implementation by making its module importable and passing
`--candidate package.module`. Compare saved result documents with:

```sh
python3 -m evals.runner.compare result-pre-redesign.json result-main.json
```

Telemetry is append-only JSONL. Adapters append only facts they can observe; an
absent host metric remains absent rather than guessed. The evaluator never decides
whether an event deserved to be a surprise or review, and it never creates a
complexity score.

## Durable run artifacts

Each graded suite lives under `evals/runs/<suite_id>/`. Git tracks two files per
run: `REPORT.md` (human) and `comparison.json` (machine scoreboard, harness SHAs,
failed oracle cases). Working files (`suite.json`, per-cell directories) hold
`/tmp` workspace paths and live telemetry; they are gitignored. Read `REPORT.md`
first. Do not add `evals/runs/` to `.cursorignore`. After a baseline run,
`git add evals/runs/<suite_id>` — gitignore strips the scratch. Use `--output-dir`
for throwaway debugging. See `evals/runs/README.md`.

`.archive/` is a separate human-only drawer (gitignored and cursorignored). The
eval controller must not copy suites there.

## Leakage boundary

Scenario workspaces receive `scenarios/public`, the fixture, and normal visible
documentation/tests. They do not receive `scenarios/grading`, oracle cases, result
expectations, or protected-boundary metadata. The canonical implementation imports
nothing from `evals.oracle`; tests enforce this boundary. Keep the oracle outside
candidate workspaces in real runs.

Candidate workspaces stay outside the repository (OS tempfile) so children cannot
walk into `evals/scenarios/grading/`. Those absolute paths live only in the
gitignored `suite.json` / `cell.json` working files. Do not nest workspaces under
`evals/runs/`.
