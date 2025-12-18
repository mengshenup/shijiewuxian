@echo off
REM Test using -ExecCmds to execute Python

cls
echo.
echo ============================================================
echo   Testing -ExecCmds Python Execution
echo ============================================================
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "D:\001xm\shijiewuxian\shijiewuxian.uproject" -ExecCmds="py D:/001xm/shijiewuxian/Scripts/MapGenerators/run_generator.py" -stdout -unattended -nopause -nosplash -ddc=InstalledNoZenLocalFallback

echo.
echo ============================================================
echo   Test Complete
echo ============================================================
echo.
pause
