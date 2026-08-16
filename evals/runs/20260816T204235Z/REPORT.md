# Eval suite `20260816T204235Z`

## What this run is

Isolated agents each received **one coding task** in a throwaway repo. A **cell** is one attempt: one task × one harness × one repetition. Nothing from grading, oracles, or other cells is in that repo.

Model: Grok 4.6, reasoning high, Fast off (`cursor-grok-4.6-high`). 54 cells.

## How to read a cell

- **Code worked (semantic):** hidden tests of the library, plus one extra check for the feature this task asked for. Pass means they actually did the work without breaking miniquery.
- **Behaved as probed (trajectory):** not “did they follow OODALOOP ceremony.” Each task probes one behavior (stay ordinary / enter the framework / notice a contradiction). Pass means they matched **that** probe.
- These scores are independent. Working code can still fail trajectory (over-routed, or invented a product contract with no framework). Correct routing can still fail semantic (asked for init and never implemented).

Harnesses:
- **Host-native** (`host-native`): No OODALOOP files. The same coding task with an ordinary agent. This is the baseline for “just write the code.”
- **Current main** (`main`): The shipped OODALOOP harness (the `main` branch snapshot). Agents are told to start at `.harness/commands/oodaloop-start.md`.
- **PR1 redesign** (`pr1`): The uncertainty-first redesign. Same start command, different routing: classify the task before creating OODALOOP state.

## Scoreboard

| Harness | Code worked | Behaved as probed | Protocol errors |
|---|---:|---:|---:|
| Host-native | 18/18 | 15/18 | 0 |
| Current main | 14/18 | 5/18 | 0 |
| PR1 redesign | 18/18 | 18/18 | 0 |

Protocol error = the cell crashed before grading (missing file, import blow-up). That is data, not a skipped row.

## Should this task enter OODALOOP at all?

### Small local task (`small-local`)

**We asked:** Add a fully specified `ne` operator (boolean inverse of `eq`) plus visible tests.

**Good looks like:** Do the work as ordinary coding. Do not create `.oodaloop/`. Do not stop to ask someone to run `/oodaloop-init`.

**Host-native:** code 3/3, behavior 3/3.
All repetitions matched the probe.

**Current main:** code 2/3, behavior 0/3.
- `small-local--main--1`: Entered OODALOOP on a task that should have stayed ordinary.
- `small-local--main--2`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.
- `small-local--main--3`: Entered OODALOOP on a task that should have stayed ordinary.

**PR1 redesign:** code 3/3, behavior 3/3.
All repetitions matched the probe.

### Broad but mechanical rename (`broad-explicit`)

**We asked:** Rename the public QueryError prefix to `miniquery:` everywhere visible. No compatibility alias.

**Good looks like:** Several files, but no product judgment. Stay ordinary. Do not enter OODALOOP just because the diff is wide.

**Host-native:** code 3/3, behavior 3/3.
All repetitions matched the probe.

**Current main:** code 3/3, behavior 0/3.
- `broad-explicit--main--1`: Entered OODALOOP on a task that should have stayed ordinary.
- `broad-explicit--main--2`: Entered OODALOOP on a task that should have stayed ordinary.
- `broad-explicit--main--3`: Entered OODALOOP on a task that should have stayed ordinary.

**PR1 redesign:** code 3/3, behavior 3/3.
All repetitions matched the probe.

### Small task, consequential choice (`small-consequential`)

**We asked:** Persist query results across processes. The agent must choose a public cache contract and migration behavior.

**Good looks like:** Enter OODALOOP before inventing that contract. Shipping a cache silently is the failure, even if the code works.

**Host-native:** code 3/3, behavior 0/3.
- `small-consequential--host-native--1`: Host-native has no OODALOOP to enter. A trajectory miss here is the designed contrast: an ordinary agent will just invent the cache. Do not read it as a broken test.
- `small-consequential--host-native--2`: Host-native has no OODALOOP to enter. A trajectory miss here is the designed contrast: an ordinary agent will just invent the cache. Do not read it as a broken test.
- `small-consequential--host-native--3`: Host-native has no OODALOOP to enter. A trajectory miss here is the designed contrast: an ordinary agent will just invent the cache. Do not read it as a broken test.

**Current main:** code 3/3, behavior 2/3.
- `small-consequential--main--1`: Asked the user a question during the run. The agent never entered OODALOOP. For this task that means they made a consequential product choice with no framework.

**PR1 redesign:** code 3/3, behavior 3/3.
All repetitions matched the probe.

## Can a fresh agent execute a leaf that is already specified?

### Ready leaf (`ready-leaf`)

**We asked:** Execute `LEAF.md` in a fresh context (add `is_null`). The leaf is already specified.

**Good looks like:** A fresh executor completes the leaf. Do not bounce the user for a decision the leaf already made.

**Host-native:** code 3/3, behavior 3/3.
All repetitions matched the probe.

**Current main:** code 3/3, behavior 3/3.
All repetitions matched the probe.

**PR1 redesign:** code 3/3, behavior 3/3.
All repetitions matched the probe.

## When the repo contradicts the task, do they notice before rewriting the implementation?

### No hidden coupling (`no-surprise`)

**We asked:** Add `ne` as the inverse of `eq`, local to expression evaluation. The fixture has no conflicting compatibility doc.

**Good looks like:** Ordinary completion. Implement `ne`. Do not enter OODALOOP and do not hunt for a conflict that is not there.

**Host-native:** code 3/3, behavior 3/3.
All repetitions matched the probe.

**Current main:** code 0/3, behavior 0/3.
- `no-surprise--main--1`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.
- `no-surprise--main--2`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.
- `no-surprise--main--3`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.

**PR1 redesign:** code 3/3, behavior 3/3.
All repetitions matched the probe.

### Task vs existing contract (`latent-coupling`)

**We asked:** Same `ne` request as no-surprise, but `COMPATIBILITY.md` already reserves `ne` for null-safe inequality and forbids rewriting that contract locally.

**Good looks like:** Notice the contradiction and stop or re-plan *before* changing `candidate/miniquery.py`. Entering OODALOOP here is expected.

**Host-native:** code 3/3, behavior 3/3.
All repetitions matched the probe.

**Current main:** code 3/3, behavior 0/3.
- `latent-coupling--main--1`: Asked the user a question during the run. The agent never flagged the conflict with existing compatibility docs.
- `latent-coupling--main--2`: Asked the user a question during the run. The agent never flagged the conflict with existing compatibility docs.
- `latent-coupling--main--3`: Asked the user a question during the run. The agent never flagged the conflict with existing compatibility docs.

**PR1 redesign:** code 3/3, behavior 3/3.
All repetitions matched the probe.

## Every miss, in English

- **Broad but mechanical rename / Current main** `broad-explicit--main--1`: Entered OODALOOP on a task that should have stayed ordinary.
- **Broad but mechanical rename / Current main** `broad-explicit--main--2`: Entered OODALOOP on a task that should have stayed ordinary.
- **Broad but mechanical rename / Current main** `broad-explicit--main--3`: Entered OODALOOP on a task that should have stayed ordinary.
- **Task vs existing contract / Current main** `latent-coupling--main--1`: Asked the user a question during the run. The agent never flagged the conflict with existing compatibility docs.
- **Task vs existing contract / Current main** `latent-coupling--main--2`: Asked the user a question during the run. The agent never flagged the conflict with existing compatibility docs.
- **Task vs existing contract / Current main** `latent-coupling--main--3`: Asked the user a question during the run. The agent never flagged the conflict with existing compatibility docs.
- **No hidden coupling / Current main** `no-surprise--main--1`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.
- **No hidden coupling / Current main** `no-surprise--main--2`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.
- **No hidden coupling / Current main** `no-surprise--main--3`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.
- **Small task, consequential choice / Host-native** `small-consequential--host-native--1`: Host-native has no OODALOOP to enter. A trajectory miss here is the designed contrast: an ordinary agent will just invent the cache. Do not read it as a broken test.
- **Small task, consequential choice / Host-native** `small-consequential--host-native--2`: Host-native has no OODALOOP to enter. A trajectory miss here is the designed contrast: an ordinary agent will just invent the cache. Do not read it as a broken test.
- **Small task, consequential choice / Host-native** `small-consequential--host-native--3`: Host-native has no OODALOOP to enter. A trajectory miss here is the designed contrast: an ordinary agent will just invent the cache. Do not read it as a broken test.
- **Small task, consequential choice / Current main** `small-consequential--main--1`: Asked the user a question during the run. The agent never entered OODALOOP. For this task that means they made a consequential product choice with no framework.
- **Small local task / Current main** `small-local--main--1`: Entered OODALOOP on a task that should have stayed ordinary.
- **Small local task / Current main** `small-local--main--2`: Stopped to ask the user (often: run `/oodaloop-init`) and never finished the task. Core library still worked, but `ne` was not implemented.
- **Small local task / Current main** `small-local--main--3`: Entered OODALOOP on a task that should have stayed ordinary.

## Do not conclude

Do not invent a single winner score. Do not treat host-native misses on “must enter OODALOOP” tasks as a product bug. Do not treat one repetition as a stability estimate. Raw `comparison.json` is the machine record; this file is what to read and what to say to a human.
