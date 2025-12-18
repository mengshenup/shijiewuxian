@echo off
REM Check Zen Server Status

cls
echo.
echo ============================================================
echo   Zen Server Status Check
echo ============================================================
echo.

echo Checking Zen server process...
tasklist /FI "IMAGENAME eq zenserver.exe" | find /I "zenserver.exe"

if %ERRORLEVEL% EQU 0 (
    echo [OK] Zen server is running
) else (
    echo [WARNING] Zen server is not running
)

echo.
echo Checking Zen HTTP service...
curl -s http://127.0.0.1:8558 >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] Zen HTTP service is accessible at http://127.0.0.1:8558
) else (
    echo [WARNING] Zen HTTP service is not accessible
)

echo.
echo ============================================================
pause
