# Claude Code Adapter

## How it works

Claude Code discovers commands, agents, and skills from `.claude/` in the project root (project-level) or `~/.claude/` (personal/global). No manifest file is needed. Skills in Agent Skills standard format (SKILL.md) are auto-discovered.

## Install (global — available across all projects)

```bash
OODALOOP_DIR="/path/to/oodaloop"

# Commands: symlink each command file
mkdir -p ~/.claude/commands
for f in "$OODALOOP_DIR"/commands/*.md; do
  ln -sf "$f" ~/.claude/commands/"$(basename "$f")"
done

# Skills: symlink each skill directory
mkdir -p ~/.claude/skills
for d in "$OODALOOP_DIR"/skills/*/; do
  name=$(basename "$d")
  ln -sf "$d" ~/.claude/skills/"$name"
done

# Agents: symlink each agent file
mkdir -p ~/.claude/agents
for f in "$OODALOOP_DIR"/agents/*.md; do
  ln -sf "$f" ~/.claude/agents/"$(basename "$f")"
done
```

## Install (project-level — single project only)

Same as above but target `.claude/` in the project root instead of `~/.claude/`.

## Rules

Claude Code uses `CLAUDE.md` at the project root for persistent rules. Append OODALOOP's rule content:

```bash
cat >> CLAUDE.md << 'RULES'

## OODALOOP Rules

- Match process depth to task complexity. Trivial tasks use /oodaloop-quick. Medium tasks use Observe → Orient → Decide → Act. Complex tasks use full OODA with Loop.
- Keep .oodaloop/ artifacts consistent. CONTEXT.md is persistent, task files are ephemeral. Never mix concerns.
- Every phase must emit evidence. Execution summaries require concrete file paths, test results, or command outputs.
RULES
```

## Notes

- Agent `readonly` and `model` frontmatter may be interpreted differently by Claude Code. The behavioral instructions in the agent body are what matter.
- Command filenames determine slash command names (e.g., `oodaloop-observe.md` → `/oodaloop-observe`).
- Skills use the Agent Skills standard — Claude Code supports this natively.
