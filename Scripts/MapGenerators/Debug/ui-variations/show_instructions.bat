@echo off
REM 显示如何在运行中的编辑器生成地图

cls
echo.
echo ============================================================
echo 在运行中的编辑器生成 Cosmos 002 Training World 地图
echo ============================================================
echo.

REM 检查编辑器是否运行
tasklist /FI "IMAGENAME eq UnrealEditor.exe" 2>NUL | find /I /N "UnrealEditor.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [状态] 检测到运行中的UE5编辑器 ✓
    echo.
    echo ============================================================
    echo 执行步骤（复制粘贴到编辑器）
    echo ============================================================
    echo.
    echo 1. 在UE5编辑器中打开:
    echo    Window -^> Developer Tools -^> Output Log
    echo.
    echo 2. 切换到 [Python] 标签
    echo.
    echo 3. 复制以下代码（Ctrl+C）:
    echo.
    echo ============================================================
    echo import sys
    echo sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators'^)
    echo import generate_cosmos_002_training_world
    echo generate_cosmos_002_training_world.main(^)
    echo ============================================================
    echo.
    echo 4. 在Python控制台粘贴（Ctrl+V）并按回车
    echo.
    echo 5. 等待脚本执行完成（约10-30秒）
    echo.
    echo 6. 检查结果:
    echo    - Content Browser -^> Maps -^> Cosmos_002_Training_World
    echo    - 文件系统: Content\Maps\Cosmos_002_Training_World.umap
    echo.
    echo ============================================================
    echo.
    
) else (
    echo [状态] 未检测到运行中的UE5编辑器 ✗
    echo.
    echo 请先运行: generate_map_editor.bat 打开编辑器
    echo 然后重新运行此脚本查看说明
    echo.
    echo ============================================================
    echo.
)

echo 按任意键关闭...
pause > nul
