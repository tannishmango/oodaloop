#!/usr/bin/env bash
set -euo pipefail

OODALOOP_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="$HOME/.cursor/plugins/local/oodaloop"

ensure_git_hooks() {
  if ! git -C "$OODALOOP_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return
  fi

  if [ ! -f "$OODALOOP_DIR/.githooks/pre-commit" ]; then
    return
  fi

  chmod +x "$OODALOOP_DIR/.githooks/pre-commit"
  git -C "$OODALOOP_DIR" config core.hooksPath .githooks
}

ensure_git_hooks

mkdir -p "$(dirname "$TARGET")"

if [ -L "$TARGET" ]; then
  rm "$TARGET"
  echo "Removed legacy symlink at $TARGET"
fi

rsync -a --delete \
  --exclude ".git/" \
  --exclude ".DS_Store" \
  "$OODALOOP_DIR"/ "$TARGET"/

# Bump version in the synced copy so Cursor invalidates its plugin cache (it caches by version and does not invalidate on file change).
BUILD_ID="sync.$(date -u +%Y%m%d%H%M%S)"
if [ -f "$TARGET/.cursor-plugin/plugin.json" ]; then
  if sed -e "s/\"version\": \"[^\"]*\"/\"version\": \"0.1.0+$BUILD_ID\"/" "$TARGET/.cursor-plugin/plugin.json" > "$TARGET/.cursor-plugin/plugin.json.tmp" 2>/dev/null; then
    mv "$TARGET/.cursor-plugin/plugin.json.tmp" "$TARGET/.cursor-plugin/plugin.json"
  fi
fi

echo "Synced $OODALOOP_DIR → $TARGET"
echo "Reload Cursor (or restart) to pick up changes. If reload still shows old behavior, clear cache: rm -rf ~/.cursor/plugins/cache"
