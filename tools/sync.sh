#!/usr/bin/env bash
# Yerly-Playground — Git Sync Helper
set -e

echo "🌸 Menyinkronkan Yerly-Playground dengan remote GitHub..."
git pull --rebase origin main
git status
echo "🌸 Sinkronisasi selesai!"
