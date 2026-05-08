#!/usr/bin/env bash
# daily-journal-helper.sh
# Creates your journal entry for today, opens it for editing, and optionally commits.
# Zero dependencies — requires only bash and a text editor.
#
# Run from the repo root:
#   bash docs/skill-work/work-cici/daily-journal/daily-journal-helper.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$SCRIPT_DIR/daily-journal-template.md"
USERS_DIR="$SCRIPT_DIR/users"
TODAY="$(date +%Y-%m-%d)"

# --- Determine author ---
if [[ -n "${JOURNAL_AUTHOR:-}" ]]; then
  AUTHOR="$JOURNAL_AUTHOR"
else
  echo ""
  echo "=== Daily Journal Helper ==="
  echo ""
  read -rp "Your username (e.g. alice  — use the same one every day): " AUTHOR
  AUTHOR="${AUTHOR// /-}"
  if [[ -z "$AUTHOR" ]]; then
    echo "Error: username cannot be empty."
    exit 1
  fi
fi

USER_DIR="$USERS_DIR/$AUTHOR"
ENTRY_FILE="$USER_DIR/$TODAY.md"

# --- Check for existing entry ---
if [[ -f "$ENTRY_FILE" ]]; then
  echo ""
  echo "Entry already exists: $ENTRY_FILE"
  read -rp "Open it for editing anyway? [y/N] " REOPEN
  if [[ "${REOPEN,,}" != "y" ]]; then
    echo "Exiting. Your entry is at:"
    echo "  $ENTRY_FILE"
    exit 0
  fi
else
  mkdir -p "$USER_DIR"
  sed \
    -e "s/YYYY-MM-DD/$TODAY/g" \
    -e "s/YOUR_NAME/$AUTHOR/g" \
    "$TEMPLATE" > "$ENTRY_FILE"
  echo ""
  echo "Draft created: $ENTRY_FILE"
fi

# --- Open in editor ---
EDITOR="${EDITOR:-}"
if [[ -z "$EDITOR" ]]; then
  if   command -v nano &>/dev/null; then EDITOR="nano"
  elif command -v vi   &>/dev/null; then EDITOR="vi"
  else
    echo ""
    echo "No editor found. Fill in the file manually, then run this script again to commit:"
    echo "  $ENTRY_FILE"
    exit 0
  fi
fi

echo "Opening in $EDITOR — fill in each section, save, and close when done."
echo ""
"$EDITOR" "$ENTRY_FILE"

# --- Summary ---
echo ""
echo "Saved: $ENTRY_FILE  ($(wc -l < "$ENTRY_FILE") lines)"
echo ""

# --- Optional commit ---
read -rp "Commit this entry? [y/N] " COMMIT
if [[ "${COMMIT,,}" != "y" ]]; then
  echo ""
  echo "Not committed yet. When ready, run from the repo root:"
  echo "  git add \"${ENTRY_FILE#$SCRIPT_DIR/../../../}\""
  echo "  git commit -m \"journal: $TODAY $AUTHOR\""
  echo "  git push -u origin \$(git branch --show-current)"
  exit 0
fi

# Resolve path relative to repo root for git add
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
REL_PATH="${ENTRY_FILE#$REPO_ROOT/}"

git -C "$REPO_ROOT" add "$REL_PATH"
git -C "$REPO_ROOT" commit -m "journal: $TODAY $AUTHOR"

echo ""
echo "Committed. To share it with the team, run:"
echo "  git push -u origin \$(git branch --show-current)"
