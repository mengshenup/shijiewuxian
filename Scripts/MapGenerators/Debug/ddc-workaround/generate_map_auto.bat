@echo off
REM 自动生成地图的批处理脚本
REM 启动编辑器，执行Python脚本生成地图，然后自动关闭

echo ============================================================
echo 自动生成 Cosmos 002 Training World 地图
echo ============================================================
echo.
echo 此脚本将：
echo 1. 启动UE5编辑器
echo 2. 自动执行Python脚本生成地图
echo 3. 生成完成后自动关闭编辑器
echo.
echo 请稍候...
echo ============================================================
echo.

REM 设置路径
set ENGINE_PATH=D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor.exe
set PROJECT_PATH=D:\001xm\shijiewuxian\shijiewuxian.uproject
set SCRIPT_PATH=Scripts/MapGenerators/auto_generate_and_quit.py

REM 启动编辑器并执行Python脚本
REM 使用 -DDC=ForceMemoryCache 来绕过DDC配置问题
"%ENGINE_PATH%" "%PROJECT_PATH%" -ExecutePythonScript="%SCRIPT_PATH%" -DDC=ForceMemoryCache -stdout -unattended -nopause -nosplash

echo.
echo ============================================================
echo 编辑器已关闭
echo.
echo 请检查生成结果：
echo - Content Browser: /Game/Maps/Cosmos_002_Training_World
echo - 文件系统: Content\Maps\Cosmos_002_Training_World.umap
echo ============================================================
echo.
pause
