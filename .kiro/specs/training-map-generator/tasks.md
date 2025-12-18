# Implementation Plan - Training Map Generator (Python Script)

## Overview

本实施计划描述如何使用Python脚本自动生成训练地图"Cosmos 002 Training World"。

**引擎版本：** Unreal Engine 5.7.0 (Source Build)
**Python版本：** UE5内置Python 3.9+
**项目名称：** shijiewuxian
**引擎路径：** D:\UnrealEngine570

**实现方式：**
- 创建Python脚本自动生成地图
- 脚本位于项目的 `Scripts/MapGenerators/` 目录
- 脚本名称与地图名称对应
- 使用UE5的Python API操作编辑器
- 修改GameMode移除动态生成代码

## Tasks

- [x] 1. Enable Python plugin and create script directory


  - Verify PythonScriptPlugin is enabled in shijiewuxian.uproject
  - Create `Scripts/MapGenerators/` directory in project root
  - Create `.gitignore` entry for Python cache files
  - _Requirements: 1.1, 1.2_


- [x] 2. Create Python map generator script

  - Create `Scripts/MapGenerators/generate_cosmos_002_training_world.py`
  - Implement `TrainingMapGenerator` class with initialization
  - Implement `create_new_level()` method to create empty map
  - Implement `get_full_map_path()` helper method
  - Add error handling for map creation
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 3. Implement TrainingRoom placement

  - Implement `place_training_room()` method
  - Load TrainingRoom class from `/Script/shijiewuxian.TrainingRoom`
  - Spawn TrainingRoom Actor at coordinates (0, 0, 0)
  - Set Actor label to "TrainingRoom_Main"
  - Add error handling for class loading and spawning
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 4. Implement PlayerStart placement

  - Implement `place_player_start()` method
  - Load PlayerStart class from `/Script/Engine.PlayerStart`
  - Spawn PlayerStart at coordinates (0, 0, 100)
  - Set rotation to (0, 0, 0) facing +Y direction
  - Set Actor label to "PlayerStart_Center"
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 5. Implement lighting system

  - Implement `setup_lighting()` method
  - Implement `create_directional_light()` method
    - Spawn DirectionalLight at (0, 0, 0) with rotation (-45, 45, 0)
    - Set intensity to 3.0 and color to white
    - Set label to "DirectionalLight_Sun"
  - Implement `create_point_light()` method
    - Accept location and label parameters
    - Set intensity to 2000.0 and attenuation radius to 1000.0
    - Set color to warm white (1.0, 0.95, 0.9)
  - Create three point lights:
    - Left room: (-600, 0, 350) labeled "PointLight_Left"
    - Center room: (0, 0, 350) labeled "PointLight_Center"
    - Right room: (600, 0, 350) labeled "PointLight_Right"
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

- [x] 6. Implement GameMode configuration

  - Implement `configure_game_mode()` method
  - Get World Settings from the world
  - Load FPSTrainingGameMode class from `/Script/shijiewuxian.FPSTrainingGameMode`
  - Set default_game_mode property in World Settings
  - Add error handling for missing GameMode class
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 7. Implement map saving and verification

  - Implement `save_map()` method
  - Use `EditorLoadingAndSavingUtils.save_map()` to save the level
  - Verify the .umap file exists after saving
  - Add error handling for save failures
  - _Requirements: 6.1, 6.2, 6.3_

- [x] 8. Implement main execution flow

  - Implement `generate_map()` method that orchestrates all steps
  - Call methods in correct order:
    1. create_new_level()
    2. place_training_room()
    3. place_player_start()
    4. setup_lighting()
    5. configure_game_mode()
    6. save_map()
  - Add try-catch error handling
  - Implement `main()` function with success/error messages
  - Add usage instructions in output
  - _Requirements: 1.3, 6.4, 7.4_

- [x] 9. Add overwrite protection

  - Check if map already exists before creating
  - Implement confirmation prompt for overwriting
  - Add option to delete old map or skip generation
  - Test multiple executions of the script
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 10. Update GameMode to remove dynamic generation


  - Modify `Source/shijiewuxian/FPSTrainingGameMode.cpp`
  - Comment out or remove `SpawnTrainingRoom()` call in BeginPlay
  - Comment out or remove `SpawnPlayerStartPoint()` call in BeginPlay
  - Comment out or remove `SetupLighting()` call in BeginPlay
  - Add log message indicating static map usage
  - Optional: Add conditional check to detect if TrainingRoom exists in map
  - Compile the modified code
  - _Requirements: 8.1, 8.2, 8.3, 8.4_



- [x] 11. Test script execution via command line ❌ FAILED
  - **STATUS:** Command-line `-ExecutePythonScript` parameter does not work in UE5.7.0
  - **TESTED:** Absolute path with `-ExecutePythonScript="D:/001xm/shijiewuxian/Scripts/MapGenerators/test_python.py"`
  - **RESULT:** Engine starts but Python script is not executed
  - **OBSERVATION:** Only plugin init_unreal.py scripts are executed
  - **CONCLUSION:** Must use editor-based execution (see task 11b)
  - See `Scripts/MapGenerators/Debug/editor-execution/notes.txt` for details
  - _Requirements: All_

- [x] 11b. Test script execution via -ExecCmds ✅ SUCCESS
  - **METHOD:** Use `-ExecCmds="py script.py"` parameter
  - **TESTED:** `generate_map.bat` → `launch_generator.py` → UE5 with `-ExecCmds`
  - **RESULT:** Map successfully generated!
  - **FILE:** `Content/Maps/Cosmos_002_Training_World.umap` (22KB)
  - **TIMESTAMP:** 2025-12-18 03:45:48
  - **FIXES APPLIED:**
    - Used `r"""` raw string for docstrings (fixed unicode escape error)
    - Used `EditorLevelLibrary.get_editor_world()` instead of `new_level()` return value
    - Simplified launcher to just run subprocess without complex timeout logic
  - _Requirements: All_

- [ ] 12. Verify generated map in editor
  - Open UE5 Editor
  - Navigate to Content Browser → Maps folder
  - Open `Cosmos_002_Training_World` map
  - Verify TrainingRoom Actor is present at (0, 0, 0)
  - Verify PlayerStart is present at (0, 0, 100)
  - Verify 1 DirectionalLight and 3 PointLights are present
  - Verify World Settings shows FPSTrainingGameMode
  - Check all Actor labels are correct
  - _Requirements: All_

- [ ] 13. Test map functionality
  - Click Play button in editor
  - Verify player spawns at PlayerStart location (center room)
  - Verify player can move with WASD
  - Verify player cannot pass through walls or partitions
  - Verify transparent partitions allow visibility to adjacent rooms
  - Verify lighting is adequate in all three rooms
  - Verify no console errors during gameplay
  - _Requirements: All_

- [ ] 14. Set map as default
  - Open Edit → Project Settings → Maps & Modes
  - Set Editor Startup Map to `/Game/Maps/Cosmos_002_Training_World`
  - Set Game Default Map to `/Game/Maps/Cosmos_002_Training_World`
  - Restart editor to verify it opens the training map
  - Test standalone game launch to verify it loads the training map
  - _Requirements: 6.4_

- [x] 15. Documentation and cleanup
  - ✅ Added README.md in Scripts/MapGenerators/ explaining usage
  - ✅ Documented script execution methods (command line, editor console)
  - ✅ Added comments to Python script explaining each section
  - ✅ Created additional documentation:
    - QUICK_START.md - Quick start guide
    - DDC_FIX_GUIDE.md - DDC issue solutions
    - 执行总结.md - Execution summary in Chinese
    - 批处理脚本说明.txt - Batch script descriptions
  - ✅ Created helper batch scripts:
    - show_instructions.bat - For running editor
    - generate_map_editor.bat - Open editor with instructions
    - generate_in_running_editor.bat - Remote execution attempt
  - ⏳ Pending: Commit Python script and generated map to version control (after map generation)
  - _Requirements: 6.4_
