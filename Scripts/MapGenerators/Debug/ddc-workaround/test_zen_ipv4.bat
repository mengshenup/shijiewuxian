@echo off
chcp 65001 >nul
REM 测试强制IPv4连接Zen服务器

cls
echo.
echo ============================================================
echo   测试Zen服务器IPv4连接
echo ============================================================
echo.

REM 设置环境变量强制IPv4
set UE-ZenServerURL=http://127.0.0.1:8558
set UE_ZENSERVER_HOST=127.0.0.1
set UE_ZENSERVER_PORT=8558

echo [1] 设置环境变量:
echo     UE-ZenServerURL=%UE-ZenServerURL%
echo     UE_ZENSERVER_HOST=%UE_ZENSERVER_HOST%
echo     UE_ZENSERVER_PORT=%UE_ZENSERVER_PORT%
echo.

echo [2] 执行Python脚本...
echo.

"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
  "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
  -ExecutePythonScript="Scripts/MapGenerators/generate_cosmos_002_training_world.py" ^
  -stdout -unattended -nopause -nosplash

echo.
echo ============================================================
echo   执行完成
echo ============================================================
echo.
pause
