"""
Test script to verify all modules can be imported correctly
Run this OUTSIDE of UE5 to check for syntax errors
"""

import sys
from pathlib import Path

# Mock unreal module for testing outside UE5
class MockUnreal:
    def log(self, msg):
        pass
    
    def get_editor_subsystem(self, subsystem_class):
        return None
    
    def load_class(self, outer, path):
        return None
    
    class Vector:
        def __init__(self, x, y, z):
            pass
    
    class Rotator:
        def __init__(self, p, y, r):
            pass
    
    class LinearColor:
        def __init__(self, r, g, b, a):
            pass
    
    class LevelEditorSubsystem:
        pass
    
    class UnrealEditorSubsystem:
        pass
    
    class EditorAssetSubsystem:
        pass
    
    class ComponentMobility:
        STATIC = 0
    
    class CollisionEnabled:
        QUERY_AND_PHYSICS = 0
    
    class CollisionChannel:
        ECC_WORLD_STATIC = 0
    
    class EditorLevelLibrary:
        @staticmethod
        def spawn_actor_from_class(cls, loc, rot):
            return None
    
    class DirectionalLightComponent:
        pass
    
    class PointLightComponent:
        pass
    
    class SkyLightComponent:
        pass
    
    class MaterialInstanceDynamic:
        @staticmethod
        def create(mat, owner):
            return None
    
    class EditorLoadingAndSavingUtils:
        @staticmethod
        def save_map(world, path):
            return True

sys.modules['unreal'] = MockUnreal()

# Add generate folder to path
generate_folder = Path(__file__).parent / "generate"
sys.path.insert(0, str(generate_folder))

print("Testing module imports...")
print("="*60)

try:
    print("1. Importing trace module...")
    from generate import trace
    print("   ✓ trace module imported")
    
    print("2. Importing level_manager module...")
    from generate import level_manager
    print("   ✓ level_manager module imported")
    
    print("3. Importing room_builder module...")
    from generate import room_builder
    print("   ✓ room_builder module imported")
    
    print("4. Importing player_spawner module...")
    from generate import player_spawner
    print("   ✓ player_spawner module imported")
    
    print("5. Importing lighting_system module...")
    from generate import lighting_system
    print("   ✓ lighting_system module imported")
    
    print("6. Importing game_mode_config module...")
    from generate import game_mode_config
    print("   ✓ game_mode_config module imported")
    
    print("7. Importing map_saver module...")
    from generate import map_saver
    print("   ✓ map_saver module imported")
    
    print("8. Importing generator module...")
    from generate import generator
    print("   ✓ generator module imported")
    
    print("9. Importing main module...")
    from generate import main
    print("   ✓ main module imported")
    
    print("="*60)
    print("✓ All modules imported successfully!")
    print("="*60)
    print("\nModule structure:")
    print(f"  - trace: {len(dir(trace))} exports")
    print(f"  - level_manager: {len(dir(level_manager))} exports")
    print(f"  - room_builder: {len(dir(room_builder))} exports")
    print(f"  - player_spawner: {len(dir(player_spawner))} exports")
    print(f"  - lighting_system: {len(dir(lighting_system))} exports")
    print(f"  - game_mode_config: {len(dir(game_mode_config))} exports")
    print(f"  - map_saver: {len(dir(map_saver))} exports")
    print(f"  - generator: {len(dir(generator))} exports")
    print(f"  - main: {len(dir(main))} exports")
    
    print("\nReady to run in UE5!")
    
except ImportError as e:
    print(f"\n✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
