# AGENTS.md

## Cursor Cloud specific instructions

OODALOOP is a host-agnostic agent framework distributed as markdown (`commands/`,
`skills/`, `rules/`, `agents/`, `foundation/`, `templates/`) plus a small Python
behavioral-eval harness under `evals/`. There is no package manager, lockfile, or
build step: the Python code is **stdlib-only** and runs on the system `python3`
(3.12). Nothing needs to be installed to run tests or the eval harness.

Common commands (run from the repo root):
- Tests: `python3 -m unittest discover -s evals/tests -v`
- Semantic eval grader (grades the seed candidate against the oracle):
  `python3 -m evals.runner.run --condition main` (writes JSON; add `--output <file>`)
- Compare two result artifacts: `python3 -m evals.runner.compare <a.json> <b.json>`
- Human eval report from a graded suite: `python3 -m evals.runner.report evals/runs/<suite_id>`
- Python parse/compile check: `python3 -m compileall -q evals`

Lint gate: the repo's lint is the git hook `.githooks/pre-commit`. It only inspects
**staged** files and only flags a subset (ephemeral `.oodaloop/*.task.md`, deprecated
"begin" kickoff naming, and factual invariants in `tests/fixtures/state-hygiene/valid*.task.md`).
It is not a full linter; a clean commit of unrelated files passes trivially.

Gotchas:
- `./install.sh` (the product installer) requires `rsync` and copies the plugin into
  the host at `~/.cursor/plugins/local/oodaloop`. It also runs
  `git config core.hooksPath .githooks`, which **overrides the Cursor cloud agent's
  own `core.hooksPath`**. Avoid running `install.sh` in the cloud VM; if you do,
  restore the platform value afterward (it looks like
  `~/.cursor/agent-hooks/<id>`) so platform git hooks keep working.
- The full `/oodaloop-eval` matrix is a merge/blast-radius bar; see
  `skills/run-cursor-eval/SKILL.md`. After grading, read
  `evals/runs/<suite_id>/REPORT.md` — that is the human meaning of the run. If it is
  missing, generate it with `python3 -m evals.runner.report SUITE_DIR` before
  explaining results to anyone.
- Eval run artifacts belong under `evals/runs/`. Git tracks `REPORT.md` and
  `comparison.json` per suite. Working files (`suite.json`, per-cell dirs) are
  gitignored. Do not add `evals/runs/` to `.cursorignore`. After a baseline run,
  commit `evals/runs/<suite_id>/` (gitignore strips the scratch).
