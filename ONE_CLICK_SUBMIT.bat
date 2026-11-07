@echo off
chcp 65001 >nul
echo ============================================================================
echo   Apart Research: AI x Epistemics Research Sprint — One-Click Project Submit
echo   Author: Zeshuai Pi (pizeshuai@gmail.com)
echo   Submission Window: 2026-11-13 20:00 to 2026-11-16 21:00 (UTC+8)
echo ============================================================================
echo.
C:\Python313\python.exe -X utf8 "%~dp0src\submit_to_apart.py" --mode submit
echo.
echo Done! Check outputs\portal_receipts\ for confirmation screenshots.
pause
