# OpenCode Adapter

## How it works

OpenCode discovers commands from `.opencode/commands/` (project) or `~/.config/opencode/commands/` (global). Skills use the Agent Skills standard. Agent definitions can be created via CLI or config.

## Install (global)

```bash
OODALOOP_DIR="/path/to/oodaloop"

mkdir -p ~/.config/opencode/commands
for f in "$OODALOOP_DIR"/commands/*.md; do
  ln -sf "$f" ~/.config/opencode/commands/"$(basename "$f")"
done

mkdir -p ~/.config/opencode/skills
for d in "$OODALOOP_DIR"/skills/*/; do
  name=$(basename "$d")
  ln -sf "$d" ~/.config/opencode/skills/"$name"
done
```

## Install (project-level)

Same as above but target `.opencode/` in the project root instead of `~/.config/opencode/`.

## Agents

Register the four semantic roles if useful in your OpenCode setup:

```bash
opencode agent create --name oodaloop-researcher --description "Targeted evidence and blind-spot discovery"
opencode agent create --name oodaloop-planner --description "Consequential planning and executable leaf decomposition"
opencode agent create --name oodaloop-executor --description "Execution of one decision-ready leaf"
opencode agent create --name oodaloop-reviewer --description "Optional independent review when risk or surprise warrants it"
```

Model selection should follow host policy: stronger reasoning where it collapses ambiguity, cheapest adequate intelligence for decision-ready execution. Do not hardcode current frontier model names into the adapter.

## Rules

Map the canonical rules into the OpenCode instruction/config surface appropriate to the installed version. Preserve the critical invariant: **normal agent behavior is the default; OODALOOP must earn invocation.**

## Hooks / deterministic events

If the installed OpenCode version exposes lifecycle/tool hooks, use them only for factual must-happen behavior such as destructive-operation interception, state validation, or cheap telemetry. Do not encode semantic rescoping/review decisions in callbacks.

## Notes

- Command filenames determine command names.
- Skills use the Agent Skills standard.
- Exact config/hook syntax may evolve independently of the OODALOOP core; keep host-specific details here rather than in core skills.
