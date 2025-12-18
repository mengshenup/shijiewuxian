@echo off
chcp 65001 >nul
REM 立即执行 - 最快的地图生成方法

cls
echo.
echo ============================================================
echo          Cosmos 002 Training World 地图生成器
echo ============================================================
echo.

REM 检查编辑器状态
tasklist /FI "IMAGENAME eq UnrealEditor.exe" 2>NUL | find /I /N "UnrealEditor.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] 检测到运行中的UE5编辑器
    echo.
    echo ============================================================
    echo  执行步骤 - 只需3步
    echo ============================================================
    echo.
    echo  步骤1: 在UE5编辑器中打开Python控制台
    echo         Window -^> Developer Tools -^> Output Log -^> Python标签
    echo.
    echo  步骤2: 复制以下代码
    echo.
    echo  --------------------------------------------------------
    echo  import sys
    echo  sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators'^)
    echo  import generate_cosmos_002_training_world
    echo  generate_cosmos_002_training_world.main(^)
    echo  --------------------------------------------------------
    echo.
    echo  步骤3: 在Python控制台粘贴并按回车
    echo.
    echo ============================================================
    echo.
    echo  预计执行时间: 10-30秒
    echo  生成位置: Content/Maps/Cosmos_002_Training_World.umap
    echo.
    echo ============================================================
    echo.
    
    REM 复制到剪贴板
    (
        echo import sys
        echo sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators'^)
        echo import generate_cosmos_002_training_world
        echo generate_cosmos_002_training_world.main(^)
    ) | clip
    
    echo [OK] 代码已复制到剪贴板
    echo      直接在编辑器Python控制台按 Ctrl+V 粘贴即可
    echo.
    
) else (
    echo [ERROR] 未检测到运行中的UE5编辑器
    echo.
    echo 请先运行: generate_map_editor.bat
    echo.
)

echo ============================================================
echo.
pause
