@echo off
REM Test without Zen server - use local DDC only

cls
echo.
echo ============================================================
echo   Test Map Generation - No Zen Server
echo ============================================================
echo.

echo [1] Using local DDC only (no Zen)...
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "D:\001xm\shijiewuxian\shijiewuxian.uproject" -ExecutePythonScript="Scripts/MapGenerators/generate_cosmos_002_training_world.py" -stdout -unattended -nopause -nosplash -ddc=noshared

echo.
echo ============================================================
echo   Execution Complete
echo ============================================================
echo.
pause
