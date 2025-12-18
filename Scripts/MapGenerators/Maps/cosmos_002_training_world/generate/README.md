# Cosmos 002 Training World - Modular Map Generator

## 概述

这是重构后的模块化地图生成器，代码被拆分成约100行的原子模块，并添加了UE5环境适配的执行追踪。

## 为什么重构？

1. **原代码太长**: 原 `generate.py` 有600+行，难以维护和调试
2. **追踪机制不工作**: `sys.settrace()` 和 `threading` 在UE5 Python环境中不可用
3. **调试困难**: 当脚本卡住或崩溃时，无法知道具体在哪一行

## 新架构

### 模块结构 (每个约100行)

```
generate/
├── __init__.py              # 包初始化
├── trace.py                 # UE5适配的追踪系统 (手动 unreal.log)
├── level_manager.py         # Level创建和加载
├── room_builder.py          # 训练室几何体构建
├── player_spawner.py        # PlayerStart放置
├── lighting_system.py       # 照明系统设置
├── game_mode_config.py      # GameMode配置
├── map_saver.py             # 地图保存
├── generator.py             # 主协调器
├── main.py                  # 入口点
└── README.md                # 本文档
```

### 追踪系统

**问题**: UE5的Python环境不支持 `sys.settrace()` 和 `threading`

**解决方案**: 使用手动 `unreal.log()` 调用在关键位置输出追踪标记

**追踪标记格式**:
- `[TRACE:LINE:123]` - 普通行号追踪
- `[TRACE:CHECKPOINT:123] NAME` - 检查点（用于恢复）
- `[TRACE:ENTER:123] function_name()` - 函数进入
- `[TRACE:EXIT:123] function_name()` - 函数退出
- `[TRACE:BEFORE_API:123] api_name` - UE5 API调用前
- `[TRACE:AFTER_API:123] api_name` - UE5 API调用后

**关键检查点**:
- `SCRIPT_START` - 脚本开始
- `BEFORE_GENERATOR_INIT` - 生成器初始化前
- `AFTER_GENERATOR_INIT` - 生成器初始化后
- `BEFORE_GENERATE_MAP` - 地图生成前
- `START_GENERATION` - 开始生成
- `BEFORE_CREATE_LEVEL` - 创建Level前
- `AFTER_CREATE_LEVEL` - 创建Level后
- `BEFORE_BUILD_ROOM` - 构建房间前
- `AFTER_BUILD_ROOM` - 构建房间后
- `BEFORE_PLACE_PLAYER` - 放置玩家前
- `AFTER_PLACE_PLAYER` - 放置玩家后
- `BEFORE_SETUP_LIGHTING` - 设置照明前
- `AFTER_SETUP_LIGHTING` - 设置照明后
- `BEFORE_CONFIG_GAMEMODE` - 配置GameMode前
- `AFTER_CONFIG_GAMEMODE` - 配置GameMode后
- `BEFORE_SAVE_MAP` - 保存地图前
- `AFTER_SAVE_MAP` - 保存地图后
- `GENERATION_COMPLETE` - 生成完成
- `SCRIPT_SUCCESS` - 脚本成功
- `SCRIPT_ERROR` - 脚本错误

## 使用方法

### 运行生成器

```bash
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```

或直接运行:

```bash
python launch_generator.py cosmos_002_training_world
```

### 查看追踪日志

生成后会创建两个日志文件:

1. **压缩摘要**: `Scripts/MapGenerators/Maps/cosmos_002_training_world/last_run.log`
   - 只包含关键信息和进度
   - 适合快速查看

2. **完整日志**: `Scripts/MapGenerators/ue5_full_log.txt`
   - 包含所有UE5输出
   - 包含所有TRACE标记
   - 适合详细调试

### 调试卡住的脚本

如果脚本卡住或崩溃:

1. 打开 `ue5_full_log.txt`
2. 搜索最后的 `[TRACE:` 标记
3. 查看最后的检查点 `[TRACE:CHECKPOINT:`
4. 这会告诉你脚本卡在哪个步骤的哪一行

**示例**:

```
[TRACE:CHECKPOINT:63] BEFORE_BUILD_ROOM
[TRACE:LINE:64] Step 2: Building training room...
[TRACE:BEFORE_API:27] load_asset(SM_Cube)
```

这表明脚本卡在加载Cube网格资源时（第27行）。

## 优势

### 1. 模块化
- 每个模块职责单一
- 易于理解和维护
- 可以独立测试

### 2. 可追踪
- 每个关键操作都有追踪标记
- 可以精确定位卡住的位置
- 即使进程被强制终止也能看到最后执行的位置

### 3. UE5适配
- 不依赖 `sys.settrace()` 或 `threading`
- 使用 `unreal.log()` 确保输出可见
- 所有追踪标记都会出现在UE5日志中

### 4. 易于扩展
- 添加新功能只需创建新模块
- 在 `generator.py` 中集成
- 添加相应的追踪标记

## 性能影响

追踪标记对性能的影响极小:
- 每个 `unreal.log()` 调用 < 1ms
- 总共约50-100个追踪点
- 总开销 < 100ms（可忽略）

## 未来改进

1. **更细粒度的追踪**: 在更多位置添加追踪标记
2. **自动恢复**: 使用检查点实现自动恢复机制
3. **性能分析**: 记录每个步骤的耗时
4. **错误恢复**: 在特定错误后自动重试

## 迁移指南

如果你有基于旧 `generate.py` 的自定义代码:

1. 识别你的修改属于哪个模块
2. 在相应的模块文件中进行修改
3. 添加适当的追踪标记
4. 在 `generator.py` 中集成（如果是新功能）

## 故障排除

### 问题: 看不到TRACE标记

**原因**: 可能是 `unreal.log()` 被禁用

**解决**: 检查UE5日志级别设置

### 问题: 脚本仍然卡住

**原因**: 可能卡在UE5 API调用内部

**解决**: 
1. 查看最后的 `[TRACE:BEFORE_API:` 标记
2. 这会告诉你哪个UE5 API调用导致卡住
3. 考虑添加超时或替代方案

### 问题: 追踪标记太多

**原因**: 调试模式下输出详细

**解决**: 
1. 在 `launch_generator.py` 中设置 `DEBUG_MODE = False`
2. 这会只显示压缩摘要

## 贡献

如果你改进了追踪系统或添加了新模块，请:

1. 保持每个模块约100行
2. 添加适当的追踪标记
3. 更新本README
4. 测试确保追踪标记正常工作
