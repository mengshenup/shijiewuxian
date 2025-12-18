# Requirements Document - Core Room Setup

## Introduction

本文档定义了FPS瞄准训练系统的核心房间搭建需求。系统需要创建3个训练房间（中间玩家房间和左右对手房间），使用透明隔板分隔，玩家可以看到相邻房间的情况。

## Glossary

- **Training System**: 瞄准训练系统，负责管理训练环境
- **Player**: 进行训练的玩家角色
- **Training Room**: 训练房间，玩家进行训练的封闭空间
- **Player Room**: 玩家房间，位于中间的房间
- **Opponent Room**: 对手房间，位于左右两侧的房间（暂时空置）
- **Transparent Partition**: 透明隔板，分隔相邻房间的透明墙壁

## Requirements

### Requirement 1

**User Story:** 作为玩家，我想要在一个训练房间中进行训练，以便我有一个专门的训练空间。

#### Acceptance Criteria

1. WHEN the Training System initializes THEN the Training System SHALL create a training room with dimensions of 600cm width, 800cm depth, and 400cm height
2. WHEN the training room is created THEN the Training System SHALL include a floor, ceiling, and walls
3. WHEN the Player enters the training room THEN the Training System SHALL ensure the room is properly lit and visible

### Requirement 2

**User Story:** 作为玩家，我想要看到相邻的对手房间，以便我能感受到竞争氛围（即使房间暂时是空的）。

#### Acceptance Criteria

1. WHEN the Training System initializes THEN the Training System SHALL create two additional opponent rooms on the left and right sides of the player room
2. WHEN the opponent rooms are created THEN the Training System SHALL ensure each opponent room has the same dimensions as the player room (600x800x400 cm)
3. WHEN the opponent rooms are created THEN the Training System SHALL position them adjacent to the player room

### Requirement 3

**User Story:** 作为玩家，我想要通过透明隔板看到相邻房间，以便我能观察到相邻空间的情况。

#### Acceptance Criteria

1. WHEN the Training System creates the rooms THEN the Training System SHALL place transparent partitions between the player room and each opponent room
2. WHEN the transparent partitions are created THEN the Training System SHALL make them semi-transparent with opacity between 0.3 and 0.5
3. WHEN the Player looks at the transparent partitions THEN the Training System SHALL allow visibility through the partitions to adjacent rooms
4. WHEN the Player or projectiles contact the transparent partitions THEN the Training System SHALL block physical passage through the partitions

### Requirement 4

**User Story:** 作为玩家，我想要使用第一人称视角在房间中移动，以便我能自由探索训练环境。

#### Acceptance Criteria

1. WHEN the Training System initializes THEN the Training System SHALL spawn the Player character in the center of the player room
2. WHEN the Player character spawns THEN the Training System SHALL use the FirstPerson character template from the project
3. WHEN the Player moves THEN the Training System SHALL allow the Player to move freely within the player room boundaries
4. WHEN the Player attempts to move through walls or partitions THEN the Training System SHALL prevent the Player from passing through

### Requirement 5

**User Story:** 作为玩家，我想要房间有适当的照明，以便我能清楚地看到训练环境。

#### Acceptance Criteria

1. WHEN the Training System creates the rooms THEN the Training System SHALL provide adequate lighting for each room
2. WHEN the rooms are lit THEN the Training System SHALL ensure the player room has sufficient brightness for training activities
3. WHEN the rooms are lit THEN the Training System SHALL ensure the opponent rooms are visible through the transparent partitions

