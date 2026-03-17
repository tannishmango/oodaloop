#!/usr/bin/env bash
set -euo pipefail

OODALOOP_DIR="$(cd "$(dirname "$0")" && pwd)"

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
  if [ -L "$target" ] || [ -d "$target" ]; then
    echo "Already installed at $target"
  else
    ln -s "$OODALOOP_DIR" "$target"
    echo "Symlinked $OODALOOP_DIR → $target"
  fi
  echo ""
  echo "Restart Cursor to activate. Commands: /oodaloop-init, /oodaloop-observe, etc."
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
  echo "Commands: /oodaloop-init, /oodaloop-observe, etc."
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
  echo "Commands: /oodaloop-init, /oodaloop-observe, etc."
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
echo "Done. Run /oodaloop-init in a project to start."
