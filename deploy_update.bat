@echo off
echo ===================================================
echo  [SIREN] START CLOUD ASSETS SYNC PIPELINE
echo ===================================================
echo.

echo  1. Running database merger...
.venv\Scripts\python.exe merge_all_sources.py
if %errorlevel% neq 0 (
    echo  [ERROR] Database merge failed.
    pause
    exit /b %errorlevel%
)
echo.

echo  2. Packaging modified assets...
"C:\Program Files\Git\bin\git.exe" add .
"C:\Program Files\Git\bin\git.exe" commit -m "Update: sync assets and database v4.6"

echo.
echo  3. Transmitting to GitHub Pages remote...
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ===================================================
echo  [SYNC COMPLETE] Operation Successful!
echo  Rebuilding in 30 seconds...
echo  URL: https://bimangom.github.io/free_cul/
echo ===================================================
echo.
pause
