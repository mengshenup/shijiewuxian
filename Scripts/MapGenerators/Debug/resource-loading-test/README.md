# Resource Loading Test

## Purpose

Diagnose why `generate_cosmos_002_training_world.py` fails to load assets, resulting in an empty map (22848 bytes, no content generated).

## Problem

The main script calls `editor_asset_lib.load_asset(path)` which returns `None` for all assets, causing the generation to fail silently.

## Test Scripts

### 1. test_asset_loading.py
Tests the EXACT asset paths and loading method used in the main script.

**Run:** `test_asset_loading.bat`

**What it does:**
- Tests each asset path from the original script
- Uses the same `load_asset()` method
- Reports which assets exist vs load successfully
- Provides detailed diagnostics

### 2. browse_available_assets.py
Lists all assets in the project to verify what's actually available.

**Run:** `browse_assets.bat`

**What it does:**
- Scans `/Game/LevelPrototyping/` directory
- Lists all meshes and materials found
- Helps verify if the content exists at all

## Required Assets

From `generate_cosmos_002_training_world.py`:

```python
cube_mesh = load_asset("/Game/LevelPrototyping/Meshes/SM_Cube")
plane_mesh = load_asset("/Game/LevelPrototyping/Meshes/SM_Plane")
floor_material = load_asset("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray")
wall_material = load_asset("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02")
ceiling_material = load_asset("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark")
```

## Constraint

**MUST use these exact asset paths.** Do NOT suggest alternative assets. If they don't load, we need to fix the loading mechanism or asset references.

## Next Steps

1. Run `test_asset_loading.bat` to see which assets fail
2. Run `browse_assets.bat` to see what assets actually exist
3. Based on results:
   - If assets don't exist: Check if LevelPrototyping content is enabled
   - If assets exist but don't load: Fix the loading method
   - If paths are wrong: Correct the paths in main script

## Expected Fix

Once we identify the issue, we'll update `generate_cosmos_002_training_world.py` to correctly load the assets.
