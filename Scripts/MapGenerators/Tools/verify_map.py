"""
Verify generated map contents
Run this in UE5 Editor Python console
"""
import unreal

def verify_map():
    """Verify the generated map has all required actors"""
    print("\n" + "="*60)
    print("Verifying Map: Cosmos_002_Training_World")
    print("="*60 + "\n")
    
    # Load the map
    map_path = "/Game/Maps/Cosmos_002_Training_World"
    
    if not unreal.EditorAssetLibrary.does_asset_exist(map_path):
        print("ERROR: Map does not exist!")
        return False
    
    # Load the map
    success = unreal.EditorLevelLibrary.load_level(map_path)
    if not success:
        print("ERROR: Failed to load map!")
        return False
    
    print("✓ Map loaded successfully\n")
    
    # Get all actors in the level
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    
    print(f"Total actors in level: {len(all_actors)}\n")
    
    # Check for required actors
    training_room = None
    player_start = None
    directional_light = None
    point_lights = []
    
    for actor in all_actors:
        actor_label = actor.get_actor_label()
        actor_class = actor.get_class().get_name()
        
        print(f"  - {actor_label} ({actor_class})")
        
        if "TrainingRoom" in actor_label:
            training_room = actor
        elif "PlayerStart" in actor_label:
            player_start = actor
        elif "DirectionalLight" in actor_label:
            directional_light = actor
        elif "PointLight" in actor_label:
            point_lights.append(actor)
    
    print("\n" + "="*60)
    print("Verification Results:")
    print("="*60)
    
    results = []
    
    if training_room:
        print("✓ TrainingRoom found")
        results.append(True)
    else:
        print("✗ TrainingRoom NOT found")
        results.append(False)
    
    if player_start:
        print("✓ PlayerStart found")
        results.append(True)
    else:
        print("✗ PlayerStart NOT found")
        results.append(False)
    
    if directional_light:
        print("✓ DirectionalLight found")
        results.append(True)
    else:
        print("✗ DirectionalLight NOT found")
        results.append(False)
    
    if len(point_lights) == 3:
        print(f"✓ All 3 PointLights found")
        results.append(True)
    else:
        print(f"✗ Expected 3 PointLights, found {len(point_lights)}")
        results.append(False)
    
    print("="*60)
    
    if all(results):
        print("\n✓ MAP VERIFICATION PASSED!")
        return True
    else:
        print("\n✗ MAP VERIFICATION FAILED!")
        return False

if __name__ == "__main__":
    verify_map()
