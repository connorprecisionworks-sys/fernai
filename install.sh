#!/usr/bin/env bash
# Fern AI installer.
#
#   curl -fsSL https://raw.githubusercontent.com/connorprecisionworks-sys/fernai/main/install.sh | bash
#
# or, from a clone:  ./install.sh
#
# Installs the skills into ~/.claude/skills and puts `fern` somewhere already
# on your PATH. Adds a PATH line to your shell profile only if it has to.
set -euo pipefail

REPO="${FERN_REPO:-connorprecisionworks-sys/fernai}"
BRANCH="${FERN_BRANCH:-main}"

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  B=$'\033[1m'; G=$'\033[38;5;114m'; Y=$'\033[38;5;221m'
  C=$'\033[38;5;80m'; D=$'\033[38;5;245m'; R=$'\033[38;5;203m'; Z=$'\033[0m'
else
  B=""; G=""; Y=""; C=""; D=""; R=""; Z=""
fi
ok()   { printf '  %s✓%s %s\n' "$G" "$Z" "$1"; }
warn() { printf '  %s!%s %s\n' "$Y" "$Z" "$1"; }
die()  { printf '\n  %s✗ %s%s\n\n' "$R" "$1" "$Z" >&2; exit 1; }
head() { printf '\n%s%s%s\n' "$B" "$1" "$Z"; }

command -v python3 >/dev/null 2>&1 || die "fern needs Python 3.8+. Try: brew install python3"
python3 -c 'import sys; sys.exit(0 if sys.version_info>=(3,8) else 1)' 2>/dev/null \
  || die "Python is too old — fern needs 3.8 or newer."

# ── 1. find the source: a clone we're sitting in, or download it ────────────
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
TMP=""
if [ -n "$SELF_DIR" ] && [ -d "$SELF_DIR/skills" ] && [ -f "$SELF_DIR/bin/fern" ]; then
  SRC="$SELF_DIR"
else
  command -v curl >/dev/null 2>&1 || die "curl not found."
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  head "downloading"
  curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/heads/$BRANCH" \
    | tar xz -C "$TMP" || die "Could not download $REPO@$BRANCH."
  SRC="$(find "$TMP" -maxdepth 1 -mindepth 1 -type d | head -1)"
  [ -f "$SRC/bin/fern" ] || die "Downloaded archive looks wrong."
  ok "got $REPO@$BRANCH"
fi

# ── 2. skills ───────────────────────────────────────────────────────────────
DEST="$HOME/.claude/skills"
head "skills → ~/.claude/skills"
mkdir -p "$DEST"
n=0
for dir in "$SRC"/skills/*/; do
  name="$(basename "$dir")"
  if [ -e "$DEST/$name" ] && [ "${FERN_FORCE:-0}" != "1" ]; then
    printf '  %s·%s /%s already there\n' "$D" "$Z" "$name"
  else
    rm -rf "${DEST:?}/$name"; cp -R "$dir" "$DEST/$name"; n=$((n+1))
  fi
done
ok "$n installed"

# ── 3. pick a bin dir that is already on PATH and writable ──────────────────
on_path() { case ":$PATH:" in *":$1:"*) return 0;; *) return 1;; esac; }
writable() { [ -d "$1" ] && [ -w "$1" ] || { mkdir -p "$1" 2>/dev/null && [ -w "$1" ]; }; }

BIN=""
if [ -n "${FERN_BIN_DIR:-}" ]; then
  BIN="$FERN_BIN_DIR"
else
  for cand in "$HOME/.local/bin" "$HOME/bin" "/usr/local/bin" "/opt/homebrew/bin"; do
    if on_path "$cand" && writable "$cand"; then BIN="$cand"; break; fi
  done
fi
NEEDS_PATH=0
if [ -z "$BIN" ]; then BIN="$HOME/.local/bin"; NEEDS_PATH=1; fi
mkdir -p "$BIN" || die "Can't create $BIN"

head "cli → $BIN/fern"
install -m 0755 "$SRC/bin/fern" "$BIN/fern"
ok "fern installed"

# ── 4. fix PATH only if we had to ───────────────────────────────────────────
if [ "$NEEDS_PATH" = "1" ]; then
  case "${SHELL:-}" in
    */zsh)  RC="$HOME/.zshrc" ;;
    */bash) RC="$HOME/.bash_profile"; [ -f "$HOME/.bashrc" ] && RC="$HOME/.bashrc" ;;
    */fish) RC="$HOME/.config/fish/config.fish" ;;
    *)      RC="" ;;
  esac
  LINE='export PATH="$HOME/.local/bin:$PATH"'
  [ "${RC##*/}" = "config.fish" ] && LINE='set -gx PATH $HOME/.local/bin $PATH'
  if [ -n "$RC" ] && ! grep -qs '\.local/bin' "$RC" 2>/dev/null; then
    mkdir -p "$(dirname "$RC")"; printf '\n# fern\n%s\n' "$LINE" >> "$RC"
    ok "added $BIN to your PATH in ${RC/#$HOME/~}"
    warn "run:  source ${RC/#$HOME/~}   (or open a new terminal)"
  else
    warn "add this to your shell profile, then reopen your terminal:"
    printf '\n      %s\n' "$LINE"
  fi
fi

head "done"
if [ "$NEEDS_PATH" = "1" ]; then
  printf '  %sReopen your terminal, then just run:%s  %sfern%s\n' "$D" "$Z" "$C" "$Z"
else
  printf '  %sRun:%s  %sfern%s\n' "$D" "$Z" "$C" "$Z"
fi
printf '  %sRestart Claude Code to pick up the skills.%s\n\n' "$D" "$Z"
