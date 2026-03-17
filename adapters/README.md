# OODALOOP Adapters

OODALOOP's core (skills, doctrine, state model) is host-agnostic. Adapters are thin mapping layers that place OODALOOP's components where each host environment can discover them.

## What an adapter provides

Each adapter maps five surfaces:

| Surface | What it does | Why it varies |
|---------|-------------|---------------|
| **Commands** | Places command `.md` files where the host finds them | Install path differs per host |
| **Skills** | Makes SKILL.md files discoverable | Most hosts auto-discover; some need explicit paths |
| **Agents** | Translates agent definitions to host format | Frontmatter keys and file locations differ |
| **Rules** | Translates rule content to host format | Format varies widely (`.mdc`, `CLAUDE.md`, config) |
| **Manifest** | Registers the plugin if required | Only Cursor requires a manifest file |

## What an adapter does NOT touch

- Skill logic (SKILL.md content is the open standard, works everywhere)
- `.oodaloop/` state directory (host-agnostic by design)
- `foundation/` doctrine
- `templates/`

## Host capability matrix

| Capability | Cursor | Claude Code | OpenCode |
|-----------|--------|-------------|----------|
| Slash commands | `commands/*.md` via plugin manifest | `.claude/commands/*.md` | `.opencode/commands/*.md` |
| Skills (SKILL.md) | `skills/*/SKILL.md` via manifest | Auto-discovered or `.claude/skills/` | `.opencode/skills/` or config |
| Agent definitions | `agents/*.md` with `model`, `readonly` | `.claude/agents/*.md` | CLI or config-based |
| Rules | `rules/*.mdc` with `alwaysApply` | `CLAUDE.md` + project settings | Config-based rules |
| Manifest required | Yes (`.cursor-plugin/plugin.json`) | No | No |
| Global install path | `~/.cursor/plugins/local/<name>/` | `~/.claude/` (personal) | `~/.config/opencode/` |
| Project install path | N/A (plugin is global) | `.claude/` in project root | `.opencode/` in project root |

## Install flow

```
clone repo → run install.sh → script detects host → applies adapter → done
```

The install script at the repo root handles host detection and setup. Each adapter directory contains host-specific instructions and any format-translated files.

## Adding a new host

1. Create `adapters/<host>/` with an `install.md`
2. Document where commands, skills, agents, and rules go
3. Add any format-translated files (e.g., rule files in host format)
4. Update the capability matrix above
5. Add a detection case to `install.sh`
