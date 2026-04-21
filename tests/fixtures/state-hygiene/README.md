# State-hygiene validator fixtures

Test harness for the pre-commit validator block (`#6`) in `.githooks/pre-commit`.

## Fixture inventory

| File | Expected result | Validator tested |
|---|---|---|
| `valid.task.md` | pass | all (valid baseline) |
| `invalid-mode.task.md` | fail (mode-vocabulary) | Mode must be `direct` or `delegated` |
| `invalid-paused.task.md` | fail (paused-completeness) | Missing `Strategy` field in Paused section |
| `invalid-phase-section.task.md` | fail (phase-section) | Phase `act` but no `## Plan` section |
| `invalid-depth.task.md` + `invalid-depth-parent-{1..4}.task.md` | fail (parent-depth) | 5-deep chain (4 hops, depth > 3) with no `Depth-consent:` marker |
| `valid-depth-consent.task.md` + `valid-depth-consent-parent-{1..4}.task.md` | pass | 5-deep chain (4 hops, depth > 3) WITH `Depth-consent:` marker |

## Commit-time vs. manual-test behavior

On every commit, the pre-commit hook runs block #6 against staged `valid*.task.md` fixtures only. This is a **regression test**: the validator must still pass well-formed files. If a `valid*.task.md` fixture starts failing, something broke in the validator.

The `invalid-*.task.md` fixtures are **manual-test tools** only. They are not validated on commit (intentionally — they violate the rules by design). Use the manual harness below to test that the validator correctly rejects them.

## Harness invocation

To manually test that the validator rejects specific violations, stage the fixture and invoke the hook directly:

```bash
# From repo root — test a single fixture
SKIP_CHANGELOG=1 git add tests/fixtures/state-hygiene/valid.task.md
.githooks/pre-commit  # should exit 0

SKIP_CHANGELOG=1 git add tests/fixtures/state-hygiene/invalid-mode.task.md
.githooks/pre-commit  # should exit 1 with mode-vocabulary error

# Stage a full depth chain (5 files = 4 hops = depth > 3 → rejected)
SKIP_CHANGELOG=1 git add tests/fixtures/state-hygiene/invalid-depth.task.md \
  tests/fixtures/state-hygiene/invalid-depth-parent-1.task.md \
  tests/fixtures/state-hygiene/invalid-depth-parent-2.task.md \
  tests/fixtures/state-hygiene/invalid-depth-parent-3.task.md \
  tests/fixtures/state-hygiene/invalid-depth-parent-4.task.md
.githooks/pre-commit  # should exit 1 with parent-depth error

# Clean up staged changes without committing
git restore --staged tests/fixtures/state-hygiene/
```

Note: `SKIP_CHANGELOG=1` bypasses hook block #5 (CHANGELOG requirement) so you can test just block #6 in isolation. Do NOT use `SKIP_CHANGELOG=1` for real commits.
