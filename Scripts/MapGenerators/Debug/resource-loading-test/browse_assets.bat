@echo off
echo ========================================
echo Browse Available Assets
echo ========================================
echo.

set UE_EDITOR="D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
set PROJECT="D:\001xm\shijiewuxian\shijiewuxian.uproject"
set SCRIPT="Scripts/MapGenerators/Debug/resource-loading-test/browse_available_assets.py"

echo Browsing project assets...
echo This will show all available meshes and materials.
echo.

%UE_EDITOR% %PROJECT% -ExecutePythonScript=%SCRIPT% -stdout -unattended -nopause -nosplash -DDC-ForceMemoryCache

echo.
echo ========================================
echo Browse completed
echo ========================================
pause
