@echo off
REM 使用UnrealEditor.exe（非Cmd）执行Python脚本
REM 这个方法会打开编辑器UI，但可以自动执行脚本

echo ============================================================
echo 使用UnrealEditor.exe自动执行Python脚本
echo ============================================================
echo.

set ENGINE_PATH=D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor.exe
set PROJECT_PATH=D:\001xm\shijiewuxian\shijiewuxian.uproject
set SCRIPT_PATH=Scripts/MapGenerators/generate_cosmos_002_training_world.py

echo 启动编辑器并执行Python脚本...
echo.

"%ENGINE_PATH%" "%PROJECT_PATH%" -ExecutePythonScript="%SCRIPT_PATH%"

echo.
echo ============================================================
echo 编辑器已关闭
echo ============================================================
pause
