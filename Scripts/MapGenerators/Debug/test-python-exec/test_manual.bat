@echo off
cd /d "%~dp0..\..\..\.."

echo Testing UE5 -ExecCmds with simple Python script...
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
  "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
  -ExecCmds="py D:/001xm/shijiewuxian/Scripts/MapGenerators/Debug/test-python-exec/test_hello.py" ^
  -stdout ^
  -unattended ^
  -nopause ^
  -nosplash ^
  -DDC-ForceMemoryCache

echo.
echo Test completed. Check Saved/Logs/shijiewuxian.log for "HELLO FROM PYTHON!"
pause
