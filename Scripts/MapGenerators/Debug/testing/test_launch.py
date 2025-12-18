"""Test script to diagnose launch_generator.py issues"""
import sys
import os
from pathlib import Path

print("=== Diagnostic Test ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"__file__ exists: {'__file__' in globals()}")

if '__file__' in globals():
    print(f"__file__ = {__file__}")
    script_dir = Path(__file__).parent.absolute()
    print(f"script_dir = {script_dir}")
    project_root = script_dir.parent.parent
    print(f"project_root = {project_root}")
else:
    print("__file__ not available")
    script_dir = Path.cwd() / 'Scripts' / 'MapGenerators'
    print(f"script_dir (fallback) = {script_dir}")
    project_root = script_dir.parent.parent
    print(f"project_root (fallback) = {project_root}")

print(f"\nChecking paths:")
print(f"  script_dir exists: {script_dir.exists()}")
print(f"  project_root exists: {project_root.exists()}")

# Try to import the actual script
print(f"\nTrying to import launch_generator...")
sys.path.insert(0, str(script_dir))

try:
    import launch_generator
    print("✓ Successfully imported launch_generator")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")
