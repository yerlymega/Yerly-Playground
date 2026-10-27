@echo off
REM Yerly-Playground — Git Sync Helper for Windows
echo 🌸 Menyinkronkan Yerly-Playground dengan remote GitHub...
git pull --rebase origin main 2>nul || git pull --rebase origin master 2>nul
git status
echo 🌸 Sinkronisasi selesai!
