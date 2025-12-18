@echo off
REM 在已运行的编辑器中生成地图
REM 使用UE5的远程执行功能向运行中的编辑器发送Python命令

echo ============================================================
echo 在运行中的编辑器生成地图
echo ============================================================
echo.
echo 检查编辑器状态...

REM 检查编辑器是否运行
tasklist /FI "IMAGENAME eq UnrealEditor.exe" 2>NUL | find /I /N "UnrealEditor.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✓ 检测到运行中的UE5编辑器
    echo.
    echo 正在向编辑器发送地图生成命令...
    echo.
    
    REM 使用Python执行远程命令
    python Scripts/MapGenerators/execute_in_running_editor.py
    
    echo.
    echo ============================================================
    echo 完成
    echo ============================================================
) else (
    echo ✗ 未检测到运行中的UE5编辑器
    echo.
    echo 请先启动编辑器，然后重新运行此脚本
    echo 或使用 generate_map_editor.bat 打开编辑器
    echo ============================================================
)

echo.
pause
