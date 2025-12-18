r"""
Cosmos 002 Training World Map Generator - Entry Point
Automatically generates the training map with TrainingRoom, PlayerStart, and lighting.

This is a modular refactored version with UE5-compatible execution tracing.
The code is split into atomic modules (~100 lines each) in the generate/ folder.

Usage:
    Command Line:
        "D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
          "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
          -ExecCmds="py D:/001xm/shijiewuxian/Scripts/MapGenerators/Maps/cosmos_002_training_world/generate.py" ^
          -stdout -unattended -nopause -nosplash
    
    Editor Console:
        import sys
        sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators/Maps/cosmos_002_training_world')
        import generate
        generate.main()

Modules:
    - trace.py: UE5-compatible execution tracing (manual unreal.log calls)
    - level_manager.py: Level creation and loading
    - room_builder.py: Training room geometry
    - player_spawner.py: PlayerStart placement
    - lighting_system.py: Lighting setup
    - game_mode_config.py: GameMode configuration
    - map_saver.py: Map saving
    - generator.py: Main orchestrator
    - main.py: Entry point
"""

import sys
from pathlib import Path

# DEBUG: Print to confirm script is running
print("="*60)
print("DEBUG: generate.py script started!")
print("="*60)
sys.stdout.flush()

# Add generate folder to path
generate_folder = Path(__file__).parent / "generate"
sys.path.insert(0, str(generate_folder))

print(f"DEBUG: Added to path: {generate_folder}")
sys.stdout.flush()

# Import and run main
# Note: Import from the module directly since we added it to sys.path
try:
    print("DEBUG: Importing main...")
    sys.stdout.flush()
    from main import main
    print("DEBUG: main imported successfully!")
    sys.stdout.flush()
except Exception as e:
    print(f"DEBUG: Failed to import main: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    exit(1)

# Always run main when this script is executed
# (UE5's -ExecCmds doesn't set __name__ to "__main__")
print("DEBUG: Calling main()...")
sys.stdout.flush()
exit(main())
