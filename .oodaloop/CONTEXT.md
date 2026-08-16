# Context: oodaloop

> Last refreshed: 2026-08-16

## Objective

Build OODALOOP as a minimal escalation and recovery harness for agentic software work under consequential uncertainty.

**Ordinary agent behavior is the default.** OODALOOP must earn invocation; needing a plan or touching multiple files is not sufficient.

## Architecture

- Commands are thin explicit entrypoints into skills.
- Core semantics: cheap entry routing → targeted Observe/Orient → weakest-sufficient Decide → leaf Act → lightweight Loop/reconciliation.
- Task tree is semantic; host subagents/worktrees/parallelism are execution substrate.
- A leaf is executable when the executor does not need to invent consequential intent/architecture/scope.
- Material **surprise** interrupts execution when evidence contradicts the current map.
- Re-entry is targeted: quick local fix, Decide split, Observe/Orient, or user judgment.
- There is no mandatory tri-mode assessor. `reviewer` is optional and fresh-context when consequential risk/surprise/integration/proof ambiguity makes review informative.
- Core roles: researcher (readonly), planner (readonly), executor (writer), reviewer (readonly optional).
- Model selection is host policy; role definitions do not hardcode a current model tier.

## State

```text
.oodaloop/
  CONTEXT.md       curated reusable knowledge
  BACKLOG.md       real future work
  <slug>.task.md   ephemeral active OODALOOP node
  CYCLES.log       optional cheap trajectory telemetry
```

Valid task phases: `observe`, `orient`, `decide`, `act`, `loop`.

Parent/child persistence is optional and only for genuinely independent nodes where restartability/coordination benefits. Minimal Waiting record: Child, Blocked leaf, New evidence, Resume at.

Obsolete semantic state: `paused` phase, `direct/delegated`, `subagent/in-chat/new-chat`, depth-consent machinery, assessor mode vocabulary.

## Conventions

### Git
Standard git workflow. Commit messages are descriptive/imperative. No branch protection currently recorded. Distinguish two ignored trees: `.archive/` is gitignored AND cursorignored (human-only notes such as the ATG assessment); `evals/runs/<suite_id>/` is gitignored but NOT cursorignored (agent-readable eval artifacts). Candidate eval workspaces stay in OS tempfile, not under `evals/runs/`. Do not commit `__pycache__/`, venvs, or `.DS_Store`.

### Code quality
`.githooks/pre-commit` enforces durable factual invariants only:
- no committed ephemeral `.oodaloop/*.task.md`,
- command → skill linkage,
- no deprecated begin kickoff naming,
- current factual task-state fixture checks (phase/evidence, Waiting fields, parent cycles).

It no longer requires CHANGELOG on every commit and no longer validates obsolete labor/pause/depth vocabulary.

### Testing
Stdlib `unittest` under `evals/tests/` (foundation suite: `python3 -m unittest discover -s evals/tests -v`). Plugin skills are still exercised by running commands against target projects. State-hygiene validator fixtures live at `tests/fixtures/state-hygiene/`; invoked via `SKIP_CHANGELOG=1 git add <fixture> && .githooks/pre-commit` (see README in that directory). No pytest/jest config.

Real behavioral validation of routing, leaf-readiness, surprise handling, and review economics still requires installing the branch into target repositories.

### CI/CD
None currently recorded.

### Dependencies
None; pure markdown/shell/plugin metadata. Eval runner uses stdlib Python only (`unittest`, `json`, `importlib`); no `pyproject.toml` or lockfile.

## Current design invariants

1. Framework invocation must earn its cost.
2. Complexity is remaining consequential judgment, not file/task count.
3. Plans minimize residual consequential decisions while preserving implementation optionality.
4. Executors act on decision-ready leaves.
5. Material surprise cannot be silently absorbed.
6. Re-entry begins at the lightest phase that resolves the new judgment.
7. Deterministic facts are mechanized when cheap; semantic judgment remains agent reasoning.
8. Routine leaves do not pay mandatory second-model review tax.
9. Persistent context stores surprising reusable knowledge, not execution history.
10. Host capabilities (hooks, subagents, worktrees, routing) remain adapter/substrate concerns.
11. Instrument trajectories before inventing complexity/entropy scoring.
12. The framework should get smaller as models and hosts improve.

## Adapter surfaces

Portable adapters map:
1. commands,
2. skills,
3. agents,
4. rules,
5. manifest/registration when required,
6. optional lifecycle hooks for deterministic must-happen behavior.

Targets: Cursor, Claude Code, OpenCode.

## Proof Infrastructure

Posture: adequate for eval substrate; weak for live plugin-skill contracts (routing is proven by the Cursor eval, not by unit tests).
- Strongest eval semantic proof: `python3 -m unittest discover -s evals/tests -v` plus `python3 -m evals.runner.run --condition main` (oracle only; no agent, no scenario extras unless `grade_scenario` is used).
- Strongest eval behavioral proof: `/oodaloop-eval` (6 scenarios × 3 conditions × `repetitions`). Grades semantic oracle + hidden anchors. Isolated worktrees; no `.oodaloop/` pre-created. Writes `comparison.json` and per-cell results under `evals/runs/<suite_id>/`.
- Strongest state-hygiene proof: `.githooks/pre-commit` block 4 on staged `tests/fixtures/state-hygiene/valid*.task.md`.
- Hardest relevant check for routing-before-init: `/oodaloop-eval` cell `small-local` × harness condition. `python3 -m evals.runner.run` cannot reproduce the init-gate failure.
- CI: none. No sandbox harness. No credentials required for foundation tests. Cursor eval requires the pinned Task slug `cursor-grok-4.6-high`.
- Gaps: `user_question` is not a `normal` anchor fail; telemetry is not a trustworthy measure of total tool use/latency/overhead.

## Active decisions

- 2026-08-10: OODALOOP becomes opt-in/escalation rather than default planning path.
- 2026-08-10: `/oodaloop-start` routes before state/bootstrap and may return NORMAL.
- 2026-08-10: mandatory plan/per-leaf/aggregate assessor architecture removed.
- 2026-08-10: task recursion reframed as leaf → branch promotion with targeted phase re-entry.
- 2026-08-10: lifecycle hooks added as an optional adapter surface for deterministic facts/safety/telemetry only.
- 2026-08-10: complexity theory remains qualitative/empirical; no hand-authored entropy score.

### Eval Cursor Task model
- 2026-08-16: `/oodaloop-eval` children must be launched with Cursor Task `model: "cursor-grok-4.6-high"`. That is Grok 4.6 at reasoning effort `high` with Fast off, matching `evals/config.json`. `cursor-grok-4.6-xhigh` is extra-high effort and must not be substituted.
- 2026-08-16: `/oodaloop-eval` durable artifacts live under `evals/runs/<suite_id>/` (gitignored, not cursorignored) so agents can Read `comparison.json`. Candidate workspaces stay in OS tempfile so children cannot walk into hidden grading data. `.archive/` remains human-only notes.
