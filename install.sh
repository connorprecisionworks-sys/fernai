#!/usr/bin/env bash
# Installs the Fern AI skills into ~/.claude/skills/
# and the `fern` CLI onto your PATH.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude/skills"
BIN="${FERN_BIN_DIR:-$HOME/.local/bin}"

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
ok()   { printf '  \033[38;5;114m✓\033[0m %s\n' "$1"; }
skip() { printf '  \033[38;5;245m·\033[0m %s\n' "$1"; }
warn() { printf '  \033[38;5;221m!\033[0m %s\n' "$1"; }

echo
bold "skills → $DEST"
mkdir -p "$DEST"
for dir in "$ROOT"/skills/*/; do
  name="$(basename "$dir")"
  if [ -e "$DEST/$name" ] && [ "${FERN_FORCE:-0}" != "1" ]; then
    skip "/$name already exists (FERN_FORCE=1 to overwrite)"
  else
    rm -rf "${DEST:?}/$name"
    cp -R "$dir" "$DEST/$name"
    ok "/$name"
  fi
done

echo
bold "cli → $BIN/fern"
mkdir -p "$BIN"
install -m 0755 "$ROOT/bin/fern" "$BIN/fern"
ok "fern installed"

if ! command -v fern >/dev/null 2>&1; then
  echo
  warn "$BIN is not on your PATH. Add this to your shell profile:"
  printf '\n      export PATH="%s:$PATH"\n' "$BIN"
fi

echo
bold "next"
echo "  fern setup                 set up Canvas (optional, opt-in)"
echo "  fern due                   what's due"
echo "  restart Claude Code, then type / to see the skills"
echo
