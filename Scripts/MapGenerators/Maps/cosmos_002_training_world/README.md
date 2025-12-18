# Cosmos 002 Training World

## 地图概述

**地图名称**: Cosmos_002_Training_World
**用途**: FPS瞄准训练场
**状态**: ✅ 已修复并测试

## 地图结构

### 房间布局
- **3个房间**: 左房间、中间房间、右房间
- **尺寸**: 每个房间 600 x 800 x 400 cm
- **总尺寸**: 1800 x 800 x 400 cm

### 组件清单（预计14个Actor）

**房间几何体（8个）**:
1. Floor - 地板 (1800x800 cm)
2. Ceiling - 天花板 (1800x800 cm, 高度400 cm)
3. FrontWall - 前墙 (Y=+400)
4. BackWall - 后墙 (Y=-400)
5. LeftOuterWall - 左外墙 (X=-900)
6. RightOuterWall - 右外墙 (X=+900)
7. LeftPartition - 左透明隔板 (X=-300) ⭐
8. RightPartition - 右透明隔板 (X=+300) ⭐

**玩家系统（1个）**:
9. PlayerStart_Center - 玩家出生点 (0, 0, 100)

**照明系统（5个）**:
10. DirectionalLight_Sun - 太阳光
11. SkyLight_Ambient - 环境光
12. PointLight_Left - 左房间灯 (-600, 0, 350)
13. PointLight_Center - 中间房间灯 (0, 0, 350)
14. PointLight_Right - 右房间灯 (600, 0, 350)

## 快速开始

### 生成地图
```bash
cd Scripts\MapGenerators
python launch_generator.py cosmos_002_training_world
```

或使用批处理：
```bash
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```

### 验证地图
在UE5编辑器的Python控制台中：
```python
import sys
sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators/Maps/cosmos_002_training_world/Debug/verify')
import verify_structure
verify_structure.verify()
```

## 文档索引

- **README.md** (本文件) - 地图概述和快速开始
- **FINAL_SUMMARY.md** - 完整的调试总结
- **BUG_FIXES.md** - BUG修复详情
- **DEBUGGING_SUMMARY.md** - 技术细节
- **QUICK_FIX_GUIDE.md** - 快速测试指南
- **ROOM_STRUCTURE_VISUALIZATION.md** - 房间结构可视化

## 技术特性

### 透明隔板
- 使用 `MaterialInstanceDynamic` 实现透明效果
- 透明度: 0.4 (60%透明)
- 颜色: 浅蓝色 (0.8, 0.9, 1.0)
- 物理碰撞: 完全阻挡
- 视觉效果: 可以看穿

### 照明系统
- 太阳光: 主要光源，强度3.0
- 环境光: 提供基础环境照明
- 点光源: 每个房间一个，强度2000.0

## 已知问题

### 已修复
- ✅ 透明隔板不透明 - 已修复 (2025-12-18)

### 待优化
- 无

## 版本历史

### v1.1 (2025-12-18)
- 修复透明隔板材质问题
- 添加完整文档
- 创建验证工具

### v1.0 (2025-12-18)
- 初始版本
- 基础房间结构
- 照明系统
