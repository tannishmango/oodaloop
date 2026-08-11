# Cursor Adapter

## How it works

Cursor discovers OODALOOP through its plugin manifest (`.cursor-plugin/plugin.json`). Core commands, skills, agents, and rules remain portable; Cursor-specific capabilities are optional execution substrate.

## Install

Symlink (or copy) the repo to Cursor's local plugin directory:

```bash
ln -s /path/to/oodaloop ~/.cursor/plugins/local/oodaloop
```

Restart Cursor. OODALOOP commands become available explicitly; installation must not make them the default planning path.

## What this adapter provides

- **Commands**: plugin entrypoints
- **Skills**: portable procedures
- **Agents**: researcher, planner, executor, optional reviewer
- **Rules**: lightweight invariants, especially default-NORMAL routing
- **Manifest**: `.cursor-plugin/plugin.json`
- **Hooks/lifecycle events**: optional, when supported by the installed Cursor version

## Host-native execution substrate

When available, Cursor-native subagents, parallelism, worktrees, lifecycle events, or model routing may be used to execute independent ready leaves more efficiently.

These capabilities do not change OODALOOP semantics and should not introduce persistent `direct/delegated` or child-strategy state.

## Hooks

Use lifecycle/tool hooks only for deterministic must-happen behavior such as:
- destructive-operation interception,
- state/schema validation,
- changed-path/proof telemetry,
- subagent completion/failure observation.

Do not put architecture, surprise significance, or REFINE/RESCOPE judgment in hooks.

## Notes

- Cursor's native formats may evolve; keep version-specific syntax in this adapter.
- Agent definitions intentionally do not hardcode a model tier. Use the cheapest adequate intelligence for the remaining judgment.
- The always-on rule must preserve the core routing invariant: ordinary agent behavior is the default and OODALOOP must earn invocation.
