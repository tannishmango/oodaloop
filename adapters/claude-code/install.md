# Claude Code Adapter

## How it works

Claude Code discovers commands, agents, and skills from `.claude/` in the project root or `~/.claude/` for personal/global configuration. No OODALOOP-specific manifest is required.

## Install (global)

```bash
OODALOOP_DIR="/path/to/oodaloop"

mkdir -p ~/.claude/commands
for f in "$OODALOOP_DIR"/commands/*.md; do
  ln -sf "$f" ~/.claude/commands/"$(basename "$f")"
done

mkdir -p ~/.claude/skills
for d in "$OODALOOP_DIR"/skills/*/; do
  name=$(basename "$d")
  ln -sf "$d" ~/.claude/skills/"$name"
done

mkdir -p ~/.claude/agents
for f in "$OODALOOP_DIR"/agents/*.md; do
  ln -sf "$f" ~/.claude/agents/"$(basename "$f")"
done
```

## Install (project-level)

Same as above but target `.claude/` in the project root instead of `~/.claude/`.

## Persistent rules

When mapping OODALOOP rules into `CLAUDE.md` or equivalent persistent instructions, keep them small. The most important behavior is:

```markdown
## OODALOOP
- Ordinary agent behavior is the default. Do not invoke OODALOOP merely because work needs a plan, touches multiple files, or is moderately complex.
- Escalate only when consequential uncertainty/risk remains after cheap local reasoning, or when implementation produces material surprise.
- When OODALOOP is active, detect contradicted assumptions / consequential new choices and re-enter only the lightest phase that resolves them.
- Prefer deterministic hooks/permissions for must-happen factual safety checks; use semantic review only when it can change a consequential decision.
```

Do not inject the full doctrine into every ordinary coding turn.

## Hooks / permissions

When the installed Claude Code version exposes relevant lifecycle/tool hooks or permission controls, use them for deterministic boundaries such as:
- destructive/external-state interception,
- state/schema validation,
- changed-path or lifecycle telemetry,
- subagent completion/failure observation.

Keep architecture/rescope judgment in agents, not shell callbacks.

## Notes

- Agent frontmatter support can vary by host version; behavioral instructions are canonical.
- OODALOOP agent definitions intentionally do not hardcode a model tier. Select intelligence according to the remaining judgment.
- Command filenames determine slash-command names.
- Host-specific hook/config syntax belongs in this adapter, not in the portable skills.
