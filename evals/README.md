# Behavioral evaluation foundation

This directory is neutral Level-1 infrastructure for comparing host-native work,
current `main`, PR #1, and future harnesses. It has two independent planes:

- `spec`, `oracle`, and `seed_project` measure black-box semantic correctness.
- `scenarios`, `schemas`, and `runner/telemetry.py` record behavioral trajectories.

In Cursor, install the plugin and invoke `/oodaloop-eval` with no arguments. The
controller reads `config.json`, prepares all six scenarios across host-native,
`main`, and PR1, launches isolated fresh-context subagents, and grades the resulting
18 cells. The default model is Grok 4.6 with high reasoning and Fast disabled; the
controller stops instead of silently substituting another model.

Run the canonical semantic check from the repository root:

```sh
python3 -m evals.runner.run --condition main
python3 -m unittest discover -s evals/tests -v
```

Grade another implementation by making its module importable and passing
`--candidate package.module`. Compare saved result documents with:

```sh
python3 -m evals.runner.compare result-main.json result-pr1.json
```

Telemetry is append-only JSONL. Adapters append only facts they can observe; an
absent host metric remains absent rather than guessed. The evaluator never decides
whether an event deserved to be a surprise or review, and it never creates a
complexity score.

## Leakage boundary

Scenario workspaces receive `scenarios/public`, the fixture, and normal visible
documentation/tests. They do not receive `scenarios/grading`, oracle cases, result
expectations, or protected-boundary metadata. The canonical implementation imports
nothing from `evals.oracle`; tests enforce this boundary. Keep the oracle outside
candidate workspaces in real runs.
