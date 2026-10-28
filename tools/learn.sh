#!/usr/bin/env bash
# Yerly-Playground — Continuous Learning & Knowledge Push Helper
set -e

NOTE="$1"
if [ -z "$NOTE" ]; then
  echo "Usage: ./tools/learn.sh \"Catatan ilmu atau perbaikan baru\""
  exit 1
fi

TODAY=$(date +"%Y-%m-%d")
DAILY_FILE="memory/daily/${TODAY}.md"

mkdir -p memory/daily

if [ ! -f "$DAILY_FILE" ]; then
  echo "# 🌸 Catatan Harian — ${TODAY}" > "$DAILY_FILE"
  echo "" >> "$DAILY_FILE"
fi

echo "- [$(date +"%H:%M:%S")] $NOTE" >> "$DAILY_FILE"

git add memory/daily/ playbooks/ docs/
git commit -m "docs(learn): $NOTE" || true
git push origin main

echo "🌸 Ilmu baru berhasil dicatat dan disinkronisasikan ke Git!"
