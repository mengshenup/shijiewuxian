"""
Verify TrainingRoom components in the map
"""
import unreal

def verify_training_room():
    """Check if TrainingRoom has all required components"""
    print("\n" + "="*60)
    print("Verifying TrainingRoom Components")
    print("="*60 + "\n")
    
    # Get all actors in the level
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    
    training_room = None
    for actor in all_actors:
        if actor and 'TrainingRoom' in actor.get_class().get_name():
            training_room = actor
            break
    
    if not training_room:
        print("❌ ERROR: TrainingRoom not found in level!")
        return False
    
    print(f"✓ Found TrainingRoom: {training_room.get_actor_label()}")
    print(f"  Location: {training_room.get_actor_location()}")
    print(f"  Class: {training_room.get_class().get_name()}")
    
    # Get all components
    components = training_room.get_components_by_class(unreal.StaticMeshComponent)
    
    print(f"\n✓ Found {len(components)} StaticMeshComponents:")
    
    expected_components = [
        'Floor', 'Ceiling', 
        'FrontWall', 'BackWall', 
        'LeftOuterWall', 'RightOuterWall',
        'LeftPartition', 'RightPartition'
    ]
    
    found_components = {}
    for comp in components:
        comp_name = comp.get_name()
        print(f"  - {comp_name}")
        print(f"    Mesh: {comp.static_mesh.get_name() if comp.static_mesh else 'None'}")
        print(f"    Scale: {comp.get_relative_transform().scale3d}")
        print(f"    Location: {comp.get_relative_transform().translation}")
        
        for expected in expected_components:
            if expected in comp_name:
                found_components[expected] = True
    
    print(f"\n{'='*60}")
    print("Component Check:")
    print("="*60)
    
    all_found = True
    for expected in expected_components:
        if expected in found_components:
            print(f"  ✓ {expected}")
        else:
            print(f"  ❌ {expected} - MISSING!")
            all_found = False
    
    if all_found:
        print(f"\n✓ All components found!")
        return True
    else:
        print(f"\n❌ Some components are missing!")
        print(f"\nPossible causes:")
        print(f"  1. C++ code not compiled")
        print(f"  2. TrainingRoom class definition changed")
        print(f"  3. Components not created in constructor")
        return False

if __name__ == "__main__":
    verify_training_room()
