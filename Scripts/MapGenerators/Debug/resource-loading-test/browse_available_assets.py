"""
Browse Available Assets Script
Lists all available assets in the project to help identify correct paths.

Usage:
    Command Line:
        "D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
          "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
          -ExecutePythonScript="Scripts/MapGenerators/Debug/resource-loading-test/browse_available_assets.py" ^
          -stdout -unattended -nopause -nosplash -DDC-ForceMemoryCache
"""

import unreal


def browse_assets_in_path(path, asset_type=None):
    """Browse assets in a specific path"""
    editor_asset_lib = unreal.EditorAssetLibrary()
    
    print(f"\nBrowsing: {path}")
    print("-" * 60)
    
    # List assets in directory
    assets = editor_asset_lib.list_assets(path, recursive=True, include_folder=False)
    
    if not assets:
        print("  (No assets found)")
        return []
    
    filtered_assets = []
    for asset_path in assets:
        # Load asset to get type
        asset = editor_asset_lib.load_asset(asset_path)
        if asset:
            asset_class = asset.get_class().get_name()
            
            # Filter by type if specified
            if asset_type is None or asset_type.lower() in asset_class.lower():
                filtered_assets.append((asset_path, asset_class))
                print(f"  {asset_class}: {asset_path}")
    
    return filtered_assets


def main():
    """Main function"""
    print("\n" + "="*60)
    print("AVAILABLE ASSETS BROWSER")
    print("="*60)
    
    try:
        # Browse meshes
        print("\n" + "="*60)
        print("STATIC MESHES")
        print("="*60)
        meshes = browse_assets_in_path("/Game/LevelPrototyping/Meshes", "StaticMesh")
        
        # Browse materials
        print("\n" + "="*60)
        print("MATERIALS")
        print("="*60)
        materials = browse_assets_in_path("/Game/LevelPrototyping/Materials", "Material")
        
        # Browse all LevelPrototyping content
        print("\n" + "="*60)
        print("ALL LEVEL PROTOTYPING CONTENT")
        print("="*60)
        all_assets = browse_assets_in_path("/Game/LevelPrototyping")
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Static Meshes found: {len(meshes)}")
        print(f"Materials found: {len(materials)}")
        print(f"Total assets in LevelPrototyping: {len(all_assets)}")
        
        # Suggest alternatives if standard assets not found
        print("\n" + "="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        
        if len(meshes) == 0:
            print("\n⚠ No meshes found in /Game/LevelPrototyping/Meshes")
            print("  Possible solutions:")
            print("  1. Check if LevelPrototyping content is enabled in project")
            print("  2. Use engine content: /Engine/BasicShapes/Cube")
            print("  3. Create custom meshes")
        
        if len(materials) == 0:
            print("\n⚠ No materials found in /Game/LevelPrototyping/Materials")
            print("  Possible solutions:")
            print("  1. Check if LevelPrototyping content is enabled")
            print("  2. Use engine materials: /Engine/BasicShapes/BasicShapeMaterial")
            print("  3. Create custom materials")
        
        return 0
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
