"""
Test script to verify the KismetMaterialLibrary fix
"""

import sys
import os

# Add generate module to path
generate_path = os.path.join(os.path.dirname(__file__), 'generate')
sys.path.insert(0, generate_path)

print("Testing import of room_builder module...")

try:
    from room_builder import RoomBuilder
    print("✓ Successfully imported RoomBuilder")
    
    # Check if the module has any references to KismetMaterialLibrary
    import inspect
    source = inspect.getsource(RoomBuilder)
    
    if 'KismetMaterialLibrary' in source:
        print("✗ ERROR: Found KismetMaterialLibrary reference in source code")
        sys.exit(1)
    else:
        print("✓ No KismetMaterialLibrary references found")
    
    print("\n✓ All checks passed!")
    sys.exit(0)
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
