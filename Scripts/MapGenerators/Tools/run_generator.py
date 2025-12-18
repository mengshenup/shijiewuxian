"""Simple wrapper to run map generator - avoids path escaping issues"""
import sys
sys.path.insert(0, 'D:/001xm/shijiewuxian/Scripts/MapGenerators')

print("=" * 60)
print("STARTING MAP GENERATOR")
print("=" * 60)

try:
    import generate_cosmos_002_training_world
    result = generate_cosmos_002_training_world.main()
    if result == 0:
        print("\n" + "=" * 60)
        print("SUCCESS! Map generation completed.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ERROR! Map generation failed with code:", result)
        print("=" * 60)
    sys.exit(result if result is not None else 0)
except Exception as e:
    print("\n" + "=" * 60)
    print("FATAL ERROR:", str(e))
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
