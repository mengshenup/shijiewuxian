"""
在编辑器中重新生成地图
Run this in UE5 Editor Python console after Live Coding compile
"""
import unreal

def regenerate_map():
    """Delete old map and regenerate"""
    print("\n" + "="*60)
    print("Regenerating Map in Editor")
    print("="*60 + "\n")
    
    map_path = "/Game/Maps/Cosmos_002_Training_World"
    
    # Delete old map if exists
    if unreal.EditorAssetLibrary.does_asset_exist(map_path):
        print("Deleting old map...")
        success = unreal.EditorAssetLibrary.delete_asset(map_path)
        if success:
            print("✓ Old map deleted")
        else:
            print("✗ Failed to delete old map")
            return False
    
    # Import and run generator
    import sys
    sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators')
    
    # Reload module to get latest code
    import importlib
    if 'generate_cosmos_002_training_world' in sys.modules:
        importlib.reload(sys.modules['generate_cosmos_002_training_world'])
    
    import generate_cosmos_002_training_world
    result = generate_cosmos_002_training_world.main()
    
    if result == 0:
        print("\n✓ Map regenerated successfully!")
        print("Check World Outliner to see all actors")
        return True
    else:
        print("\n✗ Map regeneration failed")
        return False

if __name__ == "__main__":
    regenerate_map()
