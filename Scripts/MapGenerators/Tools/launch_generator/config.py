"""
Configuration module - paths and settings
"""

import sys
from pathlib import Path

# Engine and project paths
ENGINE_PATH = r"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
PROJECT_PATH = r"D:\001xm\shijiewuxian\shijiewuxian.uproject"

# Get map name from command line
MAP_NAME = sys.argv[1] if len(sys.argv) > 1 else "cosmos_002_training_world"
SCRIPT_PATH = f"D:/001xm/shijiewuxian/Scripts/MapGenerators/Maps/{MAP_NAME}/generate.py"

# Debug mode: True = show all output, False = compressed summary only
DEBUG_MODE = False

# Timeout settings
TIMEOUT_SECONDS = 10  # Auto-stop after N seconds of silence (after first output)
CHECK_INTERVAL = 5    # Check every N seconds

# Retry settings
MAX_ATTEMPTS = 5      # Maximum retry attempts
RETRY_DELAY = 3       # Seconds to wait between retries


def to_ue5_map_name(map_name):
    """Convert cosmos_002_training_world to Cosmos_002_Training_World"""
    parts = map_name.split('_')
    return '_'.join(word.capitalize() for word in parts)


# Derived paths
UE5_MAP_NAME = to_ue5_map_name(MAP_NAME)
MAP_PATH = Path(f"Content/Maps/{UE5_MAP_NAME}.umap")
LOG_FILE = Path(f"Scripts/MapGenerators/Maps/{MAP_NAME}/last_run.log")
FULL_LOG_FILE = Path(f"Scripts/MapGenerators/ue5_full_log.txt")
# UE5 log file - will be determined dynamically
UE5_LOG_DIR = Path("Saved/Logs")
UE5_LOG_FILE = None  # Will be set by get_latest_ue5_log()
