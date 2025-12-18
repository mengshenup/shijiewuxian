@echo off
REM Test Python execution in UE5

cls
echo.
echo ============================================================
echo   Testing Python Execution in UE5
echo ============================================================
echo.
echo This will test if Python scripts can execute in UE5...
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "D:\001xm\shijiewuxian\shijiewuxian.uproject" -ExecutePythonScript="D:/001xm/shijiewuxian/Scripts/MapGenerators/test_python.py" -stdout -unattended -nopause -nosplash -ddc=InstalledNoZenLocalFallback

echo.
echo ============================================================
echo   Test Complete
echo ============================================================
echo.
echo Look for "PYTHON SCRIPT IS EXECUTING!" in the output above.
echo If you see it, Python is working correctly.
echo.
pause
