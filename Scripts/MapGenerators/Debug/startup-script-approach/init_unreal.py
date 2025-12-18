"""
Startup script that auto-executes map generation
Place this in a location where UE5 will auto-load it
"""

import sys
import unreal

# Add our scripts directory to path
sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators')

# Import and run the map generator
try:
    import generate_cosmos_002_training_world
    print("=" * 60)
    print("AUTO-EXECUTING MAP GENERATOR")
    print("=" * 60)
    generate_cosmos_002_training_world.main()
except Exception as e:
    print(f"ERROR in auto-execution: {str(e)}")
    import traceback
    traceback.print_exc()
