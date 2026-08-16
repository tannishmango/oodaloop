# Eval run artifacts

`/oodaloop-eval` writes a suite under `evals/runs/<suite_id>/`. Only the published
record is tracked in git:

```text
evals/runs/<suite_id>/
  REPORT.md          tracked — human meaning of the run
  comparison.json    tracked — machine scoreboard, harness SHAs, failed oracle cases
```

Working files stay local and are gitignored (`suite.json`, per-cell `cell.json`,
`events.jsonl`, `result.json`). They hold `/tmp` workspace paths and live
telemetry. Do not commit them.

This tree is append-only. Each timestamped directory is one experiment. Do not
rewrite a past `REPORT.md`; a new run gets a new `suite_id`. Read `REPORT.md`
first.

Do not add `evals/runs/` to `.cursorignore`. After a merge-bar or other run that
should survive as history:

```sh
git add evals/runs/<suite_id>
```

gitignore keeps the working files out. Scratch matrices must use
`prepare_suite.py --output-dir` outside this directory.

Candidate workspaces stay in OS tempfile, outside this repository. Do not nest
workspaces under `evals/runs/` — a child could walk up into
`evals/scenarios/grading/`.

If a future run starts capturing full child transcripts, screenshots, or other
bulky blobs, those go to object storage — not this tree.

`.archive/` remains a human-only drawer (gitignored and cursorignored). The eval
skill must not copy suites there.

## History

| Suite | What |
|---|---|
| [`20260816T204235Z`](20260816T204235Z/REPORT.md) | 54-cell merge bar for the uncertainty-first redesign. `main` here is the last init-first harness; `pr1` is the redesign before merge. |
