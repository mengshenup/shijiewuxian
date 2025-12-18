@echo off
echo ========================================
echo Asset Loading Test
echo ========================================
echo.

set UE_EDITOR="D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
set PROJECT="D:\001xm\shijiewuxian\shijiewuxian.uproject"
set SCRIPT="Scripts/MapGenerators/Debug/resource-loading-test/test_asset_loading.py"

echo Running asset loading test...
echo.

%UE_EDITOR% %PROJECT% -ExecutePythonScript=%SCRIPT% -stdout -unattended -nopause -nosplash -DDC-ForceMemoryCache

echo.
echo ========================================
echo Test completed
echo ========================================
pause
