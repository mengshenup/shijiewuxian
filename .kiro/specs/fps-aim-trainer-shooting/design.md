# FPS Aim Trainer - Shooting & Target System Design Document

## Overview

本文档描述射击和目标系统的设计，这是FPS瞄准训练系统的核心训练功能。

**核心特性：**
- **白板区域**：2400单位宽的目标出现区域
- **目标球体**：4个可射击的目标，击中后重生
- **射击检测**：准确的命中检测
- **60秒训练**：计时器和会话管理
- **重置功能**：可射击的重置按钮

## Core Components

### 1. AWhiteboard
白板区域Actor。

### 2. ATargetSphere
可射击的目标球体。

### 3. ATrainingManager
训练管理器，负责目标生成、计时、会话管理。

### 4. AResetButton
可射击的重置按钮。

## Implementation Notes

**此功能为扩展功能，建议在房间搭建完成后再实现。**

详细设计待补充。

