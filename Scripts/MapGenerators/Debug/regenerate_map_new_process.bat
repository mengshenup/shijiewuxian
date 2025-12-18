@echo off
REM 使用新的UE5进程重新生成地图（不影响当前打开的编辑器）
echo.
echo ============================================================
echo   重新生成地图（新进程）
echo ============================================================
echo.
echo 注意：这将启动一个新的UE5进程来生成地图
echo 你当前打开的编辑器不会受影响
echo.
pause

REM 删除旧地图文件（如果被锁定会跳过）
echo 尝试删除旧地图文件...
del /F /Q "%~dp0..\..\Content\Maps\Cosmos_002_Training_World.umap" 2>nul
if exist "%~dp0..\..\Content\Maps\Cosmos_002_Training_World.umap" (
    echo 警告：旧地图文件被锁定，无法删除
    echo 生成可能会失败，请先关闭编辑器中的该地图
    echo.
    pause
)

REM 运行生成器
python "%~dp0launch_generator.py"

echo.
echo 完成！请在编辑器中重新加载地图查看更新
pause
