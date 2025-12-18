@echo off
REM Open config.ini for editing

cls
echo.
echo ============================================================
echo   Edit Configuration
echo ============================================================
echo.
echo Opening config.ini in notepad...
echo.

notepad "%~dp0..\config.ini"

echo.
echo Configuration file closed.
echo Changes will take effect on next run.
echo.
pause
