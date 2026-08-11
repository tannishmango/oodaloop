---
name: init
description: Create the minimal persistent OODALOOP state needed for restartable work.
---

## Trigger

`/oodaloop-init` only after work has actually been routed into OODALOOP, or when the user explicitly asks to initialize state.

Initialization is not a repository audit.

## Workflow

### 1. Refuse duplicate initialization

Read `.oodaloop/CONTEXT.md` directly.

- If it exists, stop rather than overwriting it.
- If it does not exist, continue.

### 2. Establish only cheap baseline facts

Determine:
- project name from workspace root (unless user supplied one),
- current host when it is obvious from the running environment or nearby host markers,
- today's date.

Do not ask the user to resolve host ambiguity unless the answer is required for the current operation; record `unknown` when harmless.

### 3. Optional lightweight sentinel scan

Capture only repository facts that are both cheap to obtain and broadly useful across future tasks, for example:
- primary dependency manifest/package manager,
- obvious test command/config,
- obvious formatter/linter config,
- obvious CI directory,
- `AGENTS.md` / project instruction files,
- obvious workspace host tooling.

Do not:
- dispatch a researcher merely to initialize state,
- inspect recent commit history by default,
- perform a full plugin-conflict/deconfliction survey,
- inventory every proof command or map every subsystem,
- ask the user to approve a plugin table,
- scan the entire repository for architecture.

Objective-relevant conventions, proof infrastructure, architecture, and host conflicts belong in Observe when they can actually affect a qualifying task.

### 4. Create minimal state

Create `.oodaloop/CONTEXT.md`:

```markdown
# Context: <project_name>

> Last refreshed: <today YYYY-MM-DD>

## Workspace
Host: <host | unknown>
<cheap durable tooling facts, if any>

## Conventions
<only cheap broadly reusable facts found at init; otherwise "Not yet inventoried — discover on demand.">

## Proof Infrastructure
<obvious test/validation command if cheaply known; otherwise "Discover on demand for the affected area.">

## Architecture
Discover on demand.

## Decisions
No decisions recorded.

## Surprising / Non-obvious Knowledge
None recorded.
```

Create `.oodaloop/BACKLOG.md`:

```markdown
# Backlog

## Next
No items yet.

## Later
No items yet.

## Done
No completed items.
```

Do not create task files during init.

### 5. Continue the qualifying work

Report only:
- state initialized,
- any cheap baseline facts captured,
- next step: the Observe/resume operation that caused initialization to be needed.

Do not produce a convention report or framework deconfliction ceremony.

## Output

Minimal persistent state that makes later OODALOOP work restartable without front-loading research unrelated to the current objective.
