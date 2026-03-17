# Cursor Adapter

## How it works

Cursor discovers OODALOOP through its plugin manifest (`.cursor-plugin/plugin.json`). All component paths in the manifest are relative, so Cursor finds commands, skills, agents, and rules automatically once the plugin is registered.

## Install

Symlink (or copy) the repo to Cursor's local plugin directory:

```bash
ln -s /path/to/oodaloop ~/.cursor/plugins/local/oodaloop
```

Restart Cursor. Commands appear as `/oodaloop-observe`, `/oodaloop-orient`, etc.

## What this adapter provides

- **Commands**: discovered via `"commands": "./commands/"` in plugin.json
- **Skills**: discovered via `"skills": "./skills/"` in plugin.json
- **Agents**: discovered via `"agents": "./agents/"` in plugin.json
- **Rules**: discovered via `"rules": "./rules/"` in plugin.json
- **Manifest**: `.cursor-plugin/plugin.json` (required, already exists)

## Notes

- No format translation needed. Cursor's native format matches the repo's canonical format.
- Rules use `.mdc` extension with `alwaysApply: true` frontmatter.
- Agent definitions use `model` and `readonly` frontmatter fields.
