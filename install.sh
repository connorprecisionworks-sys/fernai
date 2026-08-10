#!/usr/bin/env bash
# Installs the Back to School skills into ~/.claude/skills/
# so you can run them as /tutor, /triage, /draft, etc.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"
DEST="$HOME/.claude/skills"

mkdir -p "$DEST"

for dir in "$SRC"/*/; do
  name="$(basename "$dir")"
  if [ -e "$DEST/$name" ]; then
    echo "skip  /$name  (already exists at $DEST/$name)"
  else
    cp -R "$dir" "$DEST/$name"
    echo "ok    /$name"
  fi
done

echo
echo "Done. Restart Claude Code, then type / to see them."
