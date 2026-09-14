#!/usr/bin/env bash
# Create a new activity-feed post. Usage: ./tools/new-update.sh "Short title"
set -euo pipefail

[ $# -ge 1 ] || { echo "usage: $0 \"Short title\" [author]" >&2; exit 1; }

TITLE="$1"
AUTHOR="${2:-$(git config user.name || echo unknown)}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')
DATE=$(date +%Y-%m-%d)
STAMP=$(date '+%Y-%m-%d %H:%M:%S %z')
FILE="$ROOT/docs/_posts/$DATE-$SLUG.md"

[ -e "$FILE" ] && { echo "already exists: $FILE" >&2; exit 1; }

cat > "$FILE" <<POST
---
layout: default
title: "$TITLE"
author: $AUTHOR
date: $STAMP
---

Write the update here. What changed, what it revealed, what it means for the next step.
POST

echo "$FILE"
