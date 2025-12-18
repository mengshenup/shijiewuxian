@echo off
REM Open generated map in UE5 Editor

cls
echo.
echo ============================================================
echo   Open Map in UE5 Editor
echo ============================================================
echo.

set "EDITOR_PATH=D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor.exe"
set "PROJECT_PATH=D:\001xm\shijiewuxian\shijiewuxian.uproject"
set "MAP_PATH=/Game/Maps/Cosmos_002_Training_World"

echo Opening map in editor...
echo Map: %MAP_PATH%
echo.

"%EDITOR_PATH%" "%PROJECT_PATH%" %MAP_PATH%

echo.
echo ============================================================
