@echo off
REM 生成地图 - 显示详细说明

echo ============================================================
echo 地图生成说明
echo ============================================================
echo.

REM 检查编辑器是否运行
tasklist /FI "IMAGENAME eq UnrealEditor.exe" 2>NUL | find /I /N "UnrealEditor.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✓ 检测到运行中的UE5编辑器
    echo.
    echo ============================================================
    echo 方法1：使用Python控制台（推荐）
    echo ============================================================
    echo.
    echo 1. 在编辑器中打开: Window -^> Developer Tools -^> Output Log
    echo 2. 切换到 Python 标签
    echo 3. 复制粘贴以下代码并按回车：
    echo.
    echo    import sys
    echo    sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators'^)
    echo    import generate_cosmos_002_training_world
    echo    generate_cosmos_002_training_world.main(^)
    echo.
    echo ============================================================
    echo 方法2：使用控制台命令
    echo ============================================================
    echo.
    echo 1. 在编辑器中按 ` (反引号) 键打开控制台
    echo 2. 输入以下命令：
    echo.
    
    REM 生成临时脚本
    python Scripts/MapGenerators/generate_via_file.py
    
) else (
    echo ✗ 未检测到运行中的UE5编辑器
    echo.
    echo 请先运行: generate_map_editor.bat
    echo.
)

echo.
pause
