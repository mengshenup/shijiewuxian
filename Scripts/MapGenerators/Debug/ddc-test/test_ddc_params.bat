@echo off
REM Test different DDC parameter combinations
cd /d "%~dp0..\..\..\.."

echo ============================================================
echo Testing DDC Parameters
echo ============================================================
echo.

set ENGINE=D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe
set PROJECT=D:\001xm\shijiewuxian\shijiewuxian.uproject
set SCRIPT=D:/001xm/shijiewuxian/Scripts/MapGenerators/Debug/ddc-test/test_simple.py

echo Creating simple test script...
echo import unreal > "%SCRIPT%"
echo print("HELLO FROM PYTHON!") >> "%SCRIPT%"
echo unreal.log("Python script executed successfully") >> "%SCRIPT%"

echo.
echo Test 1: -DDC=ForceMemoryCache (uppercase DDC)
echo ============================================================
"%ENGINE%" "%PROJECT%" -ExecCmds="py %SCRIPT%" -stdout -unattended -nopause -nosplash -DDC=ForceMemoryCache 2>&1 | findstr /C:"HELLO" /C:"Python script" /C:"Fatal" /C:"Error" /C:"ZenServer"
echo.

echo Test 2: -ddc=noshared (lowercase, no shared)
echo ============================================================
"%ENGINE%" "%PROJECT%" -ExecCmds="py %SCRIPT%" -stdout -unattended -nopause -nosplash -ddc=noshared 2>&1 | findstr /C:"HELLO" /C:"Python script" /C:"Fatal" /C:"Error" /C:"ZenServer"
echo.

echo Test 3: -DDC=Cold (cold start)
echo ============================================================
"%ENGINE%" "%PROJECT%" -ExecCmds="py %SCRIPT%" -stdout -unattended -nopause -nosplash -DDC=Cold 2>&1 | findstr /C:"HELLO" /C:"Python script" /C:"Fatal" /C:"Error" /C:"ZenServer"
echo.

echo ============================================================
echo Tests complete
echo ============================================================
pause
