#!/usr/bin/env bash
# Yerly-Playground — Git Sync Helper
set -e

echo "🌸 Menyinkronkan Yerly-Playground dengan remote GitHub..."
git pull --rebase origin main 2>/dev/null || git pull --rebase origin master 2>/dev/null || true
git status
echo "🌸 Sinkronisasi selesai!"
