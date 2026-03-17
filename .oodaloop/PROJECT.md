# Project: oodaloop

## Objective
Build OODALOOP into a functional Cursor plugin that orchestrates project delivery using an adaptive OODA loop. The plugin builds itself -- each milestone improves the tooling used to execute the next milestone.

## Requirements (M2: Working Observe/Orient)

### R1: Commands must be thin skill invocations
Reference plugins (superpowers, cursor-team-kit) use commands as one-line wrappers that invoke skills. Our commands duplicate workflow descriptions already in skills. Commands should slim to: frontmatter + skill invocation instruction.

### R2: Init skill must be executable
The init skill needs precise steps that an AI agent can follow to create `.oodaloop/`, copy templates, substitute variables, and set initial state. Current skeleton says "copy from templates" but doesn't specify how to resolve template paths relative to the plugin installation.

### R3: Observe skill must guide structured research
The observe skill needs a structured research procedure: what to look for, how to organize findings, when to declare observations sufficient. Current skeleton lists 6 steps but they're too abstract for reliable execution.

### R4: Orient skill must produce a real plan
The orient skill needs to specify the exact PLAN.md format: task structure, dependency notation, acceptance criteria format. Current skeleton describes the concept but not the output format.

### R5: File paths must be consistent
Commands reference flat paths (`.oodaloop/PLAN.md`). Skills and ARCHITECTURE.md reference nested paths (`.oodaloop/phases/<phase>/`). Must standardize. Flat paths are simpler for M2; nested can be added when multi-phase tracking is needed.

### R6: Plugin must be locally testable
Symlink to `~/.cursor/plugins/local/oodaloop/` and verify init/observe/orient run against a real project.

## Constraints

- No executable code (TypeScript/JS) in M2. Plugin is pure markdown/declarative.
- Skills must be rich enough that an AI agent can follow them without ambiguity.
- Commands must not duplicate skill content.
- File format must match what Cursor actually recognizes (verify agent frontmatter fields).
- Stay within the "minimum effective process" principle -- don't overbuild the procedures.

## Observations (from codebase research)

### O1: Cursor command format
Superpowers commands use `description` only in frontmatter (no `name`), plus `disable-model-invocation: true`. The filename is the command name. Our commands use both `name` and `description`. The create-plugin scaffold says commands need `name` and `description`, so our format is valid but heavier than needed.

### O2: Agent frontmatter uncertainty
Our agents use `readonly: true`. The ci-watcher agent from cursor-team-kit uses `is_background: true` but no `readonly` field. It's unclear whether `readonly` is a recognized Cursor agent field or just documentation. Need to verify.

### O3: Skills are the real substance
In all reference plugins, commands are thin invocation wrappers. Skills contain the actual procedure. Agents define roles and constraints. This confirms: M2 work is primarily about enriching skills.

### O4: Template variable substitution
Templates use `{{project_name}}` and `{{date}}` variables. The init skill must describe how to substitute these (the AI agent does it inline when copying -- there's no template engine).

### O5: Self-referential development
This repo uses `.oodaloop/` to track its own development. The state files are committed. Each milestone's observe/orient/decide/act cycle is performed manually now, then automated as the skills mature.

## Scope Boundaries
- **In scope**: Functional init/observe/orient commands+skills, path standardization, command slimming, symlink testing
- **Out of scope**: Decide/act/loop implementation (M3), hooks, MCP servers, marketplace publishing
- **Deferred**: Agent frontmatter field verification (test empirically during symlink testing), multi-phase nested paths
