#!/usr/bin/env bash
set -euo pipefail

OODALOOP_DIR="$(cd "$(dirname "$0")" && pwd)"

setup_git_hooks() {
  if [ ! -f "$OODALOOP_DIR/.githooks/pre-commit" ]; then
    return
  fi

  if git -C "$OODALOOP_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    chmod +x "$OODALOOP_DIR/.githooks/pre-commit"
    git -C "$OODALOOP_DIR" config core.hooksPath .githooks
    echo "Configured git hooks: core.hooksPath=.githooks"
  else
    echo "Skipping git hook setup (not in a git worktree)."
  fi
}

detect_host() {
  if [ -d "$HOME/.cursor" ]; then
    echo "cursor"
  elif [ -d "$HOME/.claude" ] || command -v claude &>/dev/null; then
    echo "claude-code"
  elif [ -d "$HOME/.config/opencode" ] || command -v opencode &>/dev/null; then
    echo "opencode"
  else
    echo "unknown"
  fi
}

install_cursor() {
  local target="$HOME/.cursor/plugins/local/oodaloop"
  mkdir -p "$(dirname "$target")"
  if [ -L "$target" ]; then
    rm "$target"
    echo "Removed legacy symlink at $target"
  fi

  if [ -d "$target" ]; then
    echo "Updating existing local plugin at $target"
  else
    echo "Creating local plugin at $target"
  fi

  rsync -a --delete \
    --exclude ".git/" \
    --exclude ".DS_Store" \
    "$OODALOOP_DIR"/ "$target"/

  echo "Synced $OODALOOP_DIR → $target"
  echo ""
  echo "Reload or restart Cursor to activate. Start with /oodaloop-start."
}

install_claude_code() {
  mkdir -p "$HOME/.claude/commands" "$HOME/.claude/skills" "$HOME/.claude/agents"

  for f in "$OODALOOP_DIR"/commands/*.md; do
    ln -sf "$f" "$HOME/.claude/commands/$(basename "$f")"
  done
  echo "Commands symlinked to ~/.claude/commands/"

  for d in "$OODALOOP_DIR"/skills/*/; do
    name=$(basename "$d")
    ln -sf "$d" "$HOME/.claude/skills/$name"
  done
  echo "Skills symlinked to ~/.claude/skills/"

  for f in "$OODALOOP_DIR"/agents/*.md; do
    ln -sf "$f" "$HOME/.claude/agents/$(basename "$f")"
  done
  echo "Agents symlinked to ~/.claude/agents/"

  echo ""
  echo "For rules, append OODALOOP rules to your project's CLAUDE.md."
  echo "See adapters/claude-code/install.md for the rule snippet."
  echo ""
  echo "Start with /oodaloop-start."
}

install_opencode() {
  mkdir -p "$HOME/.config/opencode/commands" "$HOME/.config/opencode/skills"

  for f in "$OODALOOP_DIR"/commands/*.md; do
    ln -sf "$f" "$HOME/.config/opencode/commands/$(basename "$f")"
  done
  echo "Commands symlinked to ~/.config/opencode/commands/"

  for d in "$OODALOOP_DIR"/skills/*/; do
    name=$(basename "$d")
    ln -sf "$d" "$HOME/.config/opencode/skills/$name"
  done
  echo "Skills symlinked to ~/.config/opencode/skills/"

  echo ""
  echo "For agents, register via CLI or config. See adapters/opencode/install.md."
  echo ""
  echo "Start with /oodaloop-start."
}

echo "OODALOOP Installer"
echo "=================="
echo "Source: $OODALOOP_DIR"
echo ""

HOST="${1:-$(detect_host)}"

case "$HOST" in
  cursor)
    echo "Detected: Cursor"
    install_cursor
    ;;
  claude-code)
    echo "Detected: Claude Code"
    install_claude_code
    ;;
  opencode)
    echo "Detected: OpenCode"
    install_opencode
    ;;
  *)
    echo "Could not auto-detect host environment."
    echo ""
    echo "Usage: ./install.sh [cursor|claude-code|opencode]"
    echo ""
    echo "Or see adapters/<host>/install.md for manual setup."
    exit 1
    ;;
esac

echo ""
setup_git_hooks
echo ""
echo "Done. Run /oodaloop-start in a project to start."
