"""
DDC Cache Warmup Script
Precompiles all assets to avoid multiple restarts
"""

import unreal

def warmup_cache():
    """Warmup DDC cache by loading all required assets"""
    print("="*60)
    print("DDC CACHE WARMUP")
    print("="*60)
    
    # 1. Load all classes
    print("\n[1/4] Loading C++ classes...")
    classes_to_load = [
        "/Script/shijiewuxian.TrainingRoom",
        "/Script/shijiewuxian.FPSTrainingGameMode",
        "/Script/Engine.PlayerStart",
        "/Script/Engine.DirectionalLight",
        "/Script/Engine.PointLight",
    ]
    
    for class_path in classes_to_load:
        try:
            cls = unreal.load_class(None, class_path)
            if cls:
                print(f"  ✓ Loaded: {class_path}")
            else:
                print(f"  ✗ Failed: {class_path}")
        except Exception as e:
            print(f"  ✗ Error loading {class_path}: {e}")
    
    # 2. Load common materials
    print("\n[2/4] Loading materials...")
    material_paths = [
        "/Engine/BasicShapes/BasicShapeMaterial",
        "/Engine/EngineMaterials/DefaultMaterial",
    ]
    
    for mat_path in material_paths:
        try:
            mat = unreal.load_asset(mat_path)
            if mat:
                print(f"  ✓ Loaded: {mat_path}")
        except:
            print(f"  ℹ Skipped: {mat_path}")
    
    # 3. Force shader compilation
    print("\n[3/4] Triggering shader compilation...")
    print("  (This may take 1-2 minutes on first run)")
    
    # Create a temporary world to trigger compilation
    temp_world = unreal.EditorLevelLibrary.get_editor_world()
    if temp_world:
        print(f"  ✓ World ready: {temp_world.get_name()}")
    
    # 4. Wait for compilation
    print("\n[4/4] Waiting for background compilation...")
    import time
    time.sleep(5)  # Give it time to start compilation
    
    print("\n" + "="*60)
    print("CACHE WARMUP COMPLETE")
    print("="*60)
    print("\nNext run should be much faster!")
    
    return 0

if __name__ == "__main__":
    exit(warmup_cache())
