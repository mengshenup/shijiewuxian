@echo off
REM Test if -ExecCmds can execute Python scripts

cd /d "%~dp0..\..\..\.."

echo Testing UE5 Python execution...
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
  "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
  -ExecCmds="py D:/001xm/shijiewuxian/Scripts/MapGenerators/Debug/test-python-exec/test_simple.py" ^
  -stdout ^
  -unattended ^
  -nopause ^
  -nosplash

echo.
echo Test completed. Check output above for "TEST:" messages.
pause
