# Requirements Document - Training Map Generator (Python Script)

## Introduction

本文档定义了使用Python脚本自动生成训练地图的需求。脚本将创建名为"Cosmos 002 Training World"的地图，并自动放置训练房间、玩家出生点和照明系统。

## Glossary

- **Python Script**: Python脚本，用于自动化UE5编辑器操作
- **Training Map**: 训练地图，名为"Cosmos_002_Training_World"
- **TrainingRoom Actor**: 训练房间Actor，包含3个房间（左、中、右）和透明隔板
- **Map Generation**: 地图生成，通过脚本自动创建.umap文件
- **Scene Population**: 场景填充，在地图中自动放置Actor

## Requirements

### Requirement 1

**User Story:** 作为开发者，我想要通过Python脚本自动创建训练地图，以便无需手动操作编辑器。

#### Acceptance Criteria

1. WHEN the Python script executes THEN the System SHALL create a new level file named "Cosmos_002_Training_World.umap"
2. WHEN the level is created THEN the System SHALL save it in the "/Game/Maps/" directory
3. WHEN the script completes THEN the System SHALL output a success message with the map file path
4. WHEN the script encounters errors THEN the System SHALL output clear error messages and exit gracefully

### Requirement 2

**User Story:** 作为开发者，我想要脚本自动放置TrainingRoom Actor，以便地图包含完整的训练房间结构。

#### Acceptance Criteria

1. WHEN the script places the TrainingRoom THEN the System SHALL spawn a TrainingRoom Actor instance at coordinates (0, 0, 0)
2. WHEN the TrainingRoom is spawned THEN the System SHALL ensure it includes all components (floor, ceiling, walls, partitions)
3. WHEN the TrainingRoom is spawned THEN the System SHALL verify the room dimensions are 1800cm x 800cm x 400cm (total for 3 rooms)
4. WHEN the TrainingRoom is spawned THEN the System SHALL ensure transparent partitions are at X = -300 and X = +300

### Requirement 3

**User Story:** 作为开发者，我想要脚本自动放置玩家出生点，以便玩家在正确位置开始游戏。

#### Acceptance Criteria

1. WHEN the script places the PlayerStart THEN the System SHALL spawn a PlayerStart Actor at coordinates (0, 0, 100)
2. WHEN the PlayerStart is spawned THEN the System SHALL set its rotation to (0, 0, 0) facing forward (+Y direction)
3. WHEN the PlayerStart is spawned THEN the System SHALL position it in the center of the middle room
4. WHEN the game starts THEN the System SHALL spawn the player at this PlayerStart location

### Requirement 4

**User Story:** 作为开发者，我想要脚本自动配置照明系统，以便训练环境有充足的光照。

#### Acceptance Criteria

1. WHEN the script sets up lighting THEN the System SHALL create one Directional Light for ambient lighting
2. WHEN the Directional Light is created THEN the System SHALL position it at (0, 0, 0) with rotation (-45, 45, 0)
3. WHEN the Directional Light is created THEN the System SHALL set its intensity to 3.0 and color to white
4. WHEN the script sets up lighting THEN the System SHALL create three Point Lights for room illumination
5. WHEN the Point Lights are created THEN the System SHALL position them at:
   - Left room: (-600, 0, 350)
   - Center room: (0, 0, 350)
   - Right room: (600, 0, 350)
6. WHEN the Point Lights are created THEN the System SHALL set their intensity to 2000.0 and attenuation radius to 1000.0
7. WHEN the Point Lights are created THEN the System SHALL set their color to warm white (1.0, 0.95, 0.9)

### Requirement 5

**User Story:** 作为开发者，我想要脚本配置地图的GameMode，以便使用正确的游戏规则。

#### Acceptance Criteria

1. WHEN the script configures the map THEN the System SHALL set the World Settings GameMode Override to FPSTrainingGameMode
2. WHEN the GameMode is set THEN the System SHALL ensure it uses the FirstPerson character template
3. WHEN the map is loaded THEN the System SHALL use the configured GameMode automatically

### Requirement 6

**User Story:** 作为开发者，我想要脚本保存并验证生成的地图，以便确保地图文件正确创建。

#### Acceptance Criteria

1. WHEN the script completes all placements THEN the System SHALL save the level to disk
2. WHEN the level is saved THEN the System SHALL verify the .umap file exists at the correct path
3. WHEN the level is saved THEN the System SHALL output the file size and creation timestamp
4. WHEN the script finishes THEN the System SHALL provide instructions for opening the map in the editor

### Requirement 7

**User Story:** 作为开发者，我想要脚本可以重复执行，以便可以重新生成或更新地图。

#### Acceptance Criteria

1. WHEN the script runs and the map already exists THEN the System SHALL prompt for confirmation before overwriting
2. WHEN the user confirms overwrite THEN the System SHALL delete the old map and create a new one
3. WHEN the user cancels overwrite THEN the System SHALL exit without making changes
4. WHEN the script runs multiple times THEN the System SHALL produce identical results with the same parameters

### Requirement 8

**User Story:** 作为开发者，我想要移除GameMode中的动态生成代码，以便使用静态地图结构。

#### Acceptance Criteria

1. WHEN the GameMode is updated THEN the System SHALL remove or comment out the SpawnTrainingRoom() call from BeginPlay
2. WHEN the GameMode is updated THEN the System SHALL remove or comment out the SpawnPlayerStartPoint() call from BeginPlay
3. WHEN the GameMode is updated THEN the System SHALL remove or comment out the SetupLighting() call from BeginPlay
4. WHEN the game starts with the new map THEN the System SHALL use the map's pre-placed actors instead of dynamic generation
