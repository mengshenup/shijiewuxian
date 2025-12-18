@echo off
echo.
echo ============================================================
echo   Testing sys.settrace() in UE5 Python
echo ============================================================
echo.

set ENGINE_PATH=D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe
set PROJECT_PATH=D:\001xm\shijiewuxian\shijiewuxian.uproject
set SCRIPT_PATH=D:/001xm/shijiewuxian/Scripts/MapGenerators/Debug/test_settrace.py

"%ENGINE_PATH%" "%PROJECT_PATH%" -ExecCmds="py %SCRIPT_PATH%" -stdout -unattended -nopause -nosplash -ddc=InstalledNoZenLocalFallback -NoZenAutoLaunch

echo.
echo ============================================================
echo   Test complete
echo ============================================================
pause
