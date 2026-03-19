# OpenCode Adapter

## How it works

OpenCode discovers commands from `.opencode/commands/` (project) or `~/.config/opencode/commands/` (global). Skills use the Agent Skills standard. Agent definitions can be created via CLI or config.

## Install (global)

```bash
OODALOOP_DIR="/path/to/oodaloop"

# Commands: symlink each command file
mkdir -p ~/.config/opencode/commands
for f in "$OODALOOP_DIR"/commands/*.md; do
  ln -sf "$f" ~/.config/opencode/commands/"$(basename "$f")"
done

# Skills: symlink each skill directory
mkdir -p ~/.config/opencode/skills
for d in "$OODALOOP_DIR"/skills/*/; do
  name=$(basename "$d")
  ln -sf "$d" ~/.config/opencode/skills/"$name"
done
```

## Install (project-level)

Same as above but target `.opencode/` in the project root instead of `~/.config/opencode/`.

## Agents

OpenCode agents can be registered via CLI:

```bash
# Example for each agent (adapt model/permissions to OpenCode's format)
opencode agent create --name oodaloop-researcher --description "Read-heavy discovery agent for codebase exploration"
opencode agent create --name oodaloop-planner --description "Task decomposition and dependency analysis"
opencode agent create --name oodaloop-executor --description "Implementation of atomic plan tasks"
opencode agent create --name oodaloop-assessor --description "Per-task verification, aggregate assessment, loop verdicts"
```

Or add to `opencode.json`:

```json
{
  "agents": {
    "oodaloop-researcher": { "description": "Read-heavy discovery agent", "readonly": true },
    "oodaloop-planner": { "description": "Task decomposition and dependency analysis", "readonly": true },
    "oodaloop-executor": { "description": "Implementation of atomic plan tasks" },
    "oodaloop-assessor": { "description": "Per-task verification, aggregate assessment, loop verdicts", "readonly": true }
  }
}
```

## Rules

Add to `.opencode/` config or project-level configuration as appropriate for your OpenCode version.

## Notes

- Command filenames determine command names (e.g., `oodaloop-observe.md` → `/oodaloop-observe`).
- Skills use the Agent Skills standard — OpenCode supports this natively.
- OpenCode's config merging follows: inline > `.opencode/` > project > global > remote.
