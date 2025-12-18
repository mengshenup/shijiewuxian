@echo off
REM 使用方法: generate_map.bat [map_name]
REM 例如: generate_map.bat cosmos_002_training_world
REM 如果不提供参数，默认生成 cosmos_002_training_world

cd /d "%~dp0..\.."

if "%1"=="" (
    echo 使用默认地图: cosmos_002_training_world
    py Scripts/MapGenerators/launch_generator.py cosmos_002_training_world
) else (
    echo 生成地图: %1
    py Scripts/MapGenerators/launch_generator.py %1
)
