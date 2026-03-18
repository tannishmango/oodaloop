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

echo "Synced $OODALOOP_DIR → $TARGET"
echo "Reload or restart Cursor to pick up changes."
