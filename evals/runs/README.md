# Eval run artifacts

`/oodaloop-eval` writes graded suite output here:

```text
evals/runs/<suite_id>/
  suite.json
  comparison.json
  REPORT.md
  <cell_id>/
    cell.json
    events.jsonl
    result.json
```

This tree is the **eval lab notebook**: append-only and tracked in git. Each
timestamped directory is one experiment. Do not rewrite a past suite; a new run
gets a new `suite_id`. Read `REPORT.md` first. `comparison.json` is the machine
record.

Do not add `evals/runs/` to `.cursorignore` or `.gitignore`.

Candidate workspaces stay in OS tempfile, outside this repository. Those copies
are large and ephemeral; their absolute paths are stored in each `cell.json`.
Do not nest workspaces under `evals/runs/` — a child could walk up into
`evals/scenarios/grading/`.

Scratch or debug matrices must use `prepare_suite.py --output-dir` outside this
directory so they never look like baselines. After a merge-bar or other run that
should survive as history, `git add evals/runs/<suite_id>` and commit it.

Keep structured grading records here (reports, scoreboards, per-cell results,
observational events). If a future run starts capturing full child transcripts,
screenshots, or other bulky blobs, those go to object storage — not this tree.

`.archive/` remains a human-only drawer (gitignored and cursorignored). The eval
skill must not copy suites there.

## History

| Suite | What |
|---|---|
| [`20260816T204235Z`](20260816T204235Z/REPORT.md) | 54-cell merge bar for the uncertainty-first redesign. `main` here is the last init-first harness; `pr1` is the redesign before merge. |
