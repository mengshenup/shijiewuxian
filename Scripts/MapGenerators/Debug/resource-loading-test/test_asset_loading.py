"""
Resource Loading Test Script
Tests if UE5 Python can load the required assets for map generation.

Usage:
    Command Line:
        "D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
          "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
          -ExecutePythonScript="Scripts/MapGenerators/Debug/resource-loading-test/test_asset_loading.py" ^
          -stdout -unattended -nopause -nosplash -DDC-ForceMemoryCache
"""

import unreal


def test_asset_loading():
    """Test loading all required assets"""
    print("\n" + "="*60)
    print("ASSET LOADING TEST")
    print("="*60 + "\n")
    
    editor_asset_lib = unreal.EditorAssetLibrary()
    
    # Define assets to test - EXACT paths from generate_cosmos_002_training_world.py
    assets_to_test = [
        ("Cube Mesh", "/Game/LevelPrototyping/Meshes/SM_Cube"),
        ("Plane Mesh", "/Game/LevelPrototyping/Meshes/SM_Plane"),
        ("Floor Material", "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray"),
        ("Wall Material", "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02"),
        ("Ceiling Material", "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark"),
    ]
    
    results = []
    
    print("Testing asset loading with EXACT method from main script...\n")
    print("Method: editor_asset_lib.load_asset(path)\n")
    
    for name, path in assets_to_test:
        print(f"Testing: {name}")
        print(f"  Path: {path}")
        
        # Check if asset exists
        exists = editor_asset_lib.does_asset_exist(path)
        print(f"  does_asset_exist(): {exists}")
        
        # Try to load asset using EXACT same method as main script
        try:
            asset = editor_asset_lib.load_asset(path)
            print(f"  load_asset() returned: {asset}")
            
            if asset:
                print(f"  ✓ Loaded successfully")
                print(f"  Type: {type(asset).__name__}")
                print(f"  Class: {asset.get_class().get_name()}")
                results.append((name, True, "Success"))
            else:
                print(f"  ✗ Load returned None (asset exists but load failed)")
                # Try to understand why
                if not exists:
                    results.append((name, False, "Asset path does not exist"))
                else:
                    results.append((name, False, "load_asset() returned None despite asset existing"))
        except Exception as e:
            print(f"  ✗ Load failed with exception: {str(e)}")
            results.append((name, False, f"Exception: {str(e)}"))
        
        print()
    
    # Print summary
    print("="*60)
    print("SUMMARY")
    print("="*60 + "\n")
    
    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    
    for name, success, message in results:
        status = "✓" if success else "✗"
        print(f"{status} {name}: {message}")
    
    print(f"\nResult: {success_count}/{total_count} assets loaded successfully")
    
    if success_count == total_count:
        print("\n✓ ALL ASSETS LOADED SUCCESSFULLY!")
        return 0
    else:
        print("\n✗ SOME ASSETS FAILED TO LOAD")
        return 1


def main():
    """Main function"""
    try:
        return test_asset_loading()
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
