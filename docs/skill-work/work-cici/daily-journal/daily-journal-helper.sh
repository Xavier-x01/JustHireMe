#!/usr/bin/env bash
# daily-journal-helper.sh
# Creates a draft journal entry for today, opens it for review, and optionally commits it.
# Run from the repo root: bash docs/skill-work/work-cici/daily-journal/daily-journal-helper.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$SCRIPT_DIR/daily-journal-template.md"
ENTRIES_DIR="$SCRIPT_DIR/entries"
TODAY="$(date +%Y-%m-%d)"

# --- Determine author ---
if [[ -n "${JOURNAL_AUTHOR:-}" ]]; then
  AUTHOR="$JOURNAL_AUTHOR"
else
  echo ""
  echo "=== Daily Journal Helper ==="
  echo ""
  read -rp "Your name (e.g. alice): " AUTHOR
  AUTHOR="${AUTHOR// /-}"   # replace spaces with hyphens
  if [[ -z "$AUTHOR" ]]; then
    echo "Error: name cannot be empty."
    exit 1
  fi
fi

ENTRY_FILE="$ENTRIES_DIR/${TODAY}-${AUTHOR}.md"

# --- Check for existing entry ---
if [[ -f "$ENTRY_FILE" ]]; then
  echo ""
  echo "An entry already exists for today: $ENTRY_FILE"
  read -rp "Open it for editing anyway? [y/N] " OVERWRITE
  if [[ "${OVERWRITE,,}" != "y" ]]; then
    echo "Exiting. Your existing entry is at:"
    echo "  $ENTRY_FILE"
    exit 0
  fi
else
  # Create entries dir if it doesn't exist
  mkdir -p "$ENTRIES_DIR"

  # Copy template and fill in date + author
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
  if command -v nano &>/dev/null; then
    EDITOR="nano"
  elif command -v vi &>/dev/null; then
    EDITOR="vi"
  else
    echo "No editor found. Open this file manually, then re-run to commit:"
    echo "  $ENTRY_FILE"
    exit 0
  fi
fi

echo "Opening in $EDITOR — fill in each section, then save and close."
echo ""
"$EDITOR" "$ENTRY_FILE"

# --- Review summary ---
echo ""
echo "--- Entry saved ---"
echo "File : $ENTRY_FILE"
echo "Lines: $(wc -l < "$ENTRY_FILE")"
echo ""

# --- Optional commit ---
read -rp "Commit this journal entry to git? [y/N] " COMMIT
if [[ "${COMMIT,,}" != "y" ]]; then
  echo ""
  echo "Not committed. When you are ready, run:"
  echo "  git add \"$ENTRY_FILE\""
  echo "  git commit -m \"journal: $TODAY $AUTHOR\""
  echo "  git push -u origin \$(git branch --show-current)"
  exit 0
fi

git add "$ENTRY_FILE"
git commit -m "journal: $TODAY $AUTHOR"

echo ""
echo "Committed. To push to GitHub, run:"
echo "  git push -u origin \$(git branch --show-current)"
