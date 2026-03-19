#!/usr/bin/env bash
set -euo pipefail

OODALOOP_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="$HOME/.cursor/plugins/local/oodaloop"

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
