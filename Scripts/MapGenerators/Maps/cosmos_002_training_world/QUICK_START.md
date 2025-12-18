# 快速开始 - 模块化地图生成器

## 🚀 立即运行

```bash
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```

## 📊 查看结果

### 1. 检查地图文件
```
Content/Maps/Cosmos_002_Training_World.umap
```

### 2. 查看日志

**压缩摘要** (推荐先看):
```
Scripts/MapGenerators/Maps/cosmos_002_training_world/last_run.log
```

**完整日志** (详细调试):
```
Scripts/MapGenerators/ue5_full_log.txt
```

## 🔍 追踪标记说明

在完整日志中搜索 `[TRACE:` 可以看到执行追踪：

### 标记类型

| 标记 | 含义 | 示例 |
|------|------|------|
| `[TRACE:LINE:123]` | 执行到第123行 | `[TRACE:LINE:25] Loading meshes...` |
| `[TRACE:CHECKPOINT:123] NAME` | 到达检查点 | `[TRACE:CHECKPOINT:63] BEFORE_BUILD_ROOM` |
| `[TRACE:ENTER:123] func()` | 进入函数 | `[TRACE:ENTER:20] place_player_start()` |
| `[TRACE:EXIT:123] func()` | 退出函数 | `[TRACE:EXIT:61] place_player_start()` |
| `[TRACE:BEFORE_API:123] api` | 调用API前 | `[TRACE:BEFORE_API:27] load_asset(SM_Cube)` |
| `[TRACE:AFTER_API:123] api` | 调用API后 | `[TRACE:AFTER_API:29] load_asset(SM_Cube)` |

### 关键检查点

执行流程中的关键点：

```
SCRIPT_START
  ↓
BEFORE_GENERATOR_INIT
  ↓
AFTER_GENERATOR_INIT
  ↓
BEFORE_GENERATE_MAP
  ↓
START_GENERATION
  ↓
BEFORE_CREATE_LEVEL → AFTER_CREATE_LEVEL
  ↓
BEFORE_BUILD_ROOM → AFTER_BUILD_ROOM
  ↓
BEFORE_PLACE_PLAYER → AFTER_PLACE_PLAYER
  ↓
BEFORE_SETUP_LIGHTING → AFTER_SETUP_LIGHTING
  ↓
BEFORE_CONFIG_GAMEMODE → AFTER_CONFIG_GAMEMODE
  ↓
BEFORE_SAVE_MAP → AFTER_SAVE_MAP
  ↓
GENERATION_COMPLETE
  ↓
SCRIPT_SUCCESS
```

## 🐛 调试技巧

### 场景1: 脚本卡住

**症状**: 脚本运行后没有响应

**解决**:
1. 等待10秒（自动超时）
2. 打开 `ue5_full_log.txt`
3. 搜索最后的 `[TRACE:`
4. 查看卡在哪个API调用

**示例**:
```
[TRACE:BEFORE_API:27] load_asset(SM_Cube)
```
→ 卡在加载Cube网格

### 场景2: 脚本崩溃

**症状**: 脚本突然退出，没有完成

**解决**:
1. 打开 `ue5_full_log.txt`
2. 搜索最后的 `[TRACE:CHECKPOINT:`
3. 这会告诉你崩溃前的最后一个步骤

**示例**:
```
[TRACE:CHECKPOINT:63] BEFORE_BUILD_ROOM
[TRACE:LINE:64] Step 2: Building training room...
```
→ 在构建房间时崩溃

### 场景3: 地图生成失败

**症状**: 脚本完成但地图不正确

**解决**:
1. 检查 `last_run.log` 中的步骤完成情况
2. 查看是否所有6个步骤都完成
3. 检查创建的Actor数量

**示例**:
```
步骤完成: 6/6 (100%)
  ✓ [1/6]
  ✓ [2/6]
  ✓ [3/6]
  ✓ [4/6]
  ✓ [5/6]
  ✓ [6/6]
Actors创建: 15/15 (100%)
```

## 📁 文件结构

```
generate/
├── trace.py              # 追踪系统
├── level_manager.py      # Level管理
├── room_builder.py       # 房间构建
├── player_spawner.py     # 玩家放置
├── lighting_system.py    # 照明系统
├── game_mode_config.py   # GameMode配置
├── map_saver.py          # 地图保存
├── generator.py          # 主协调器
└── main.py               # 入口点
```

## ⚙️ 配置

### 调试模式

在 `launch_generator.py` 中：

```python
DEBUG_MODE = True   # 显示全部输出
DEBUG_MODE = False  # 只显示摘要（推荐）
```

### 超时设置

在 `launch_generator.py` 中：

```python
monitor_thread = threading.Thread(target=monitor_timeout, args=(monitor, 10, process))
#                                                                         ^^
#                                                                    超时秒数
```

## 🔧 常见问题

### Q: 看不到 `[TRACE:` 标记？

**A**: 检查 `DEBUG_MODE` 设置，或直接查看 `ue5_full_log.txt`

### Q: 追踪标记太多？

**A**: 设置 `DEBUG_MODE = False`，只看压缩摘要

### Q: 如何添加更多追踪点？

**A**: 在相应模块中调用 `log_trace()` 或 `log_checkpoint()`

### Q: 如何回到旧版本？

**A**: 从git历史恢复旧的 `generate.py`

## 📚 更多信息

- **详细文档**: `generate/README.md`
- **重构总结**: `REFACTORING_SUMMARY.md`
- **原始文档**: `README.md`

## 🎯 下一步

1. ✅ 运行生成器
2. ✅ 检查日志中的追踪标记
3. ✅ 验证地图生成成功
4. ✅ 在UE5编辑器中打开地图
5. ✅ 点击Play测试

## 💡 提示

- 首次运行时，仔细检查日志确认追踪正常工作
- 如果遇到问题，追踪标记会帮你快速定位
- 保留完整日志以便后续分析

---

**准备好了吗？运行命令开始吧！** 🚀

```bash
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```
