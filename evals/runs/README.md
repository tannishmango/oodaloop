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

Run contents are gitignored. Cursor must index them so the controller and later agents can Read `REPORT.md` and `comparison.json`. Read `REPORT.md` first. Do not add `evals/runs/` to `.cursorignore`.

Candidate workspaces stay in OS tempfile, outside this repository. Their absolute paths are stored in each `cell.json`. Do not nest workspaces under `evals/runs/` — a child could walk up into `evals/scenarios/grading/`.

`.archive/` remains a human-only drawer (gitignored and cursorignored). The eval skill must not copy suites there.
