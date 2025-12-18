"""Test asset loading"""
import unreal

print("Testing asset loading...")

# Test EditorAssetLibrary
editor_asset_lib = unreal.EditorAssetLibrary()

# Try to load cube mesh
cube_path = "/Game/LevelPrototyping/Meshes/SM_Cube"
print(f"\nTrying to load: {cube_path}")
print(f"  Asset exists: {editor_asset_lib.does_asset_exist(cube_path)}")

cube_mesh = editor_asset_lib.load_asset(cube_path)
print(f"  Loaded: {cube_mesh}")
print(f"  Type: {type(cube_mesh)}")

if cube_mesh:
    print(f"  ✓ SUCCESS: Loaded {cube_mesh.get_name()}")
else:
    print(f"  ✗ FAILED: Could not load asset")
