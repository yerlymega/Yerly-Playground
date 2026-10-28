@echo off
REM Yerly-Playground — Continuous Learning & Knowledge Push Helper for Windows
setlocal enabledelayedexpansion

set NOTE=%~1
if "%NOTE%"=="" (
  echo Usage: tools\learn.bat "Catatan ilmu atau perbaikan baru"
  exit /b 1
)

for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set TODAY=%%c-%%a-%%b)
set DAILY_FILE=memory\daily\%TODAY%.md

if not exist memory\daily mkdir memory\daily

if not exist "%DAILY_FILE%" (
  echo # 🌸 Catatan Harian — %TODAY% > "%DAILY_FILE%"
  echo. >> "%DAILY_FILE%"
)

echo - [%TIME%] %NOTE% >> "%DAILY_FILE%"

git add memory\daily\ playbooks\ docs\
git commit -m "docs(learn): %NOTE%"
git push origin main

echo 🌸 Ilmu baru berhasil dicatat dan disinkronisasikan ke Git!
