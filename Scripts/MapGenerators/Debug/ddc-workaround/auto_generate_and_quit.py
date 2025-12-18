"""
Auto-generate map and quit editor
This wrapper script generates the map and then quits the editor automatically.
"""

import unreal
import sys


def main():
    """Generate map and quit editor"""
    print("\n" + "="*60)
    print("Auto-Generate Map and Quit")
    print("="*60 + "\n")
    
    try:
        # Import and run the map generator
        sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators')
        import generate_cosmos_002_training_world
        
        result = generate_cosmos_002_training_world.main()
        
        if result == 0:
            print("\n✓ Map generation successful!")
            print("Quitting editor...\n")
        else:
            print("\n✗ Map generation failed!")
            print("Quitting editor...\n")
        
        # Quit editor
        unreal.SystemLibrary.quit_editor()
        
        return result
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Still quit editor even on error
        print("\nQuitting editor...\n")
        unreal.SystemLibrary.quit_editor()
        
        return 1


if __name__ == "__main__":
    exit(main())
