import sys
import os
from pathlib import Path

print("=== Path Test ===")
print(f"Current working directory: {os.getcwd()}")
print(f"__file__: {__file__}")
print(f"Script dir: {Path(__file__).parent.absolute()}")
print(f"Project root: {Path(__file__).parent.parent.absolute()}")

# Test ENGINE_PATH
ENGINE_PATH = r"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
print(f"\nENGINE_PATH exists: {Path(ENGINE_PATH).exists()}")

# Test PROJECT_PATH
PROJECT_PATH = r"D:\001xm\shijiewuxian\shijiewuxian.uproject"
print(f"PROJECT_PATH exists: {Path(PROJECT_PATH).exists()}")

# Test MAP_PATH
MAP_PATH = Path("Content/Maps/Cosmos_002_Training_World.umap")
print(f"MAP_PATH (relative): {MAP_PATH}")
print(f"MAP_PATH exists: {MAP_PATH.exists()}")

print("\n=== Test Complete ===")
