@echo off
REM Test with forced memory cache

cls
echo.
echo ============================================================
echo   Test Map Generation - Force Memory Cache
echo ============================================================
echo.

echo [1] Using memory cache only (bypass DDC)...
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "D:\001xm\shijiewuxian\shijiewuxian.uproject" -ExecutePythonScript="Scripts/MapGenerators/generate_cosmos_002_training_world.py" -stdout -unattended -nopause -nosplash -DDC-ForceMemoryCache

echo.
echo ============================================================
echo   Execution Complete
echo ============================================================
echo.
pause
