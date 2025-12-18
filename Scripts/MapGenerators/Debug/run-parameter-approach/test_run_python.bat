@echo off
REM Test using -run=pythonscript parameter

cls
echo.
echo ============================================================
echo   Testing -run=pythonscript Parameter
echo ============================================================
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "D:\001xm\shijiewuxian\shijiewuxian.uproject" -run=pythonscript -script="D:/001xm/shijiewuxian/Scripts/MapGenerators/generate_cosmos_002_training_world.py" -stdout -unattended -nopause -nosplash -ddc=InstalledNoZenLocalFallback

echo.
echo ============================================================
echo   Test Complete
echo ============================================================
echo.
pause
