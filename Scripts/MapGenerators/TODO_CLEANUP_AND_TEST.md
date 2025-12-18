# 📋 待办：清理和测试

## ✅ 已完成

1. ✅ 更新 `generate/trace.py` - 添加 `log_auto()` 自动追踪
2. ✅ 更新 `launch_generator/trace_parser.py` - 解析新格式
3. ✅ 更新 `launch_generator/result_analyzer.py` - 美观输出
4. ✅ 更新 `launch_generator/process_runner.py` - 移除重复代码
5. ✅ 创建测试脚本 `test_new_trace.py`

---

## ⚠️ 待清理：旧的追踪调用

### 需要更新的文件

以下文件仍在使用旧的追踪函数，需要更新为 `log_auto()`：

#### 1. `generate/room_builder.py`
**旧代码：**
```python
from trace import log_trace, log_step, log_function_entry, log_function_exit, log_api_call

log_trace(14, "RoomBuilder.__init__")
log_function_entry("build_training_room", 21)
log_api_call("load_asset(SM_Cube)", 27, before=True)
```

**新代码：**
```python
from trace import log_auto, log_step, log_checkpoint

log_auto("RoomBuilder初始化")
log_auto("开始构建训练室")
log_auto("加载Cube网格")
```

#### 2. `generate/player_spawner.py`
**需要更新：** 同样的模式

#### 3. `generate/level_manager.py`
**需要检查：** 是否使用旧函数

#### 4. `generate/lighting_system.py`
**需要检查：** 是否使用旧函数

#### 5. `generate/game_mode_config.py`
**需要检查：** 是否使用旧函数

#### 6. `generate/map_saver.py`
**需要检查：** 是否使用旧函数

---

## 🧪 待测试

### 测试1：本地测试（不需要UE5）

**运行：**
```bash
cd Scripts\MapGenerators
python test_new_trace.py
```

**预期输出：**
```
🧪 开始测试新的自动追踪系统

============================================================
测试 1: log_auto() 自动追踪
============================================================
[UNREAL.LOG] [TRACE:test_new_trace:45:0] 测试开始
[UNREAL.LOG] [TRACE:test_new_trace:47:10] 加载资源
[UNREAL.LOG] [TRACE:test_new_trace:49:30] 创建对象
[UNREAL.LOG] [TRACE:test_new_trace:51:40] 测试完成
✓ log_auto() 测试通过

...

✅ 所有测试通过！
```

### 测试2：UE5集成测试

**运行：**
```bash
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```

**预期输出：**
```
============================================================
  执行摘要
============================================================
[1/6] 创建Level
[2/6] 构建训练室
...

📍 执行追踪:
  当前模块: map_saver.py
  模块行号: 42
  执行时间: 5.234秒

  📜 模块执行历史（共 23 条，按执行顺序）:
      序号  模块                    行号  说明                      耗时(ms)  总共(ms)
      ─────────────────────────────────────────────────────────────────────────────
        1.  level_manager.py        L15   准备Level                    11ms      1234ms
        ...

  ⏱️  性能分析:
      最慢的3个步骤:
        1. map_saver.py:L28 → 800ms (保存地图文件)
        ...
```

---

## 📝 清理步骤

### 步骤1：更新 room_builder.py

```python
# 旧代码（删除）
from trace import log_trace, log_step, log_function_entry, log_function_exit, log_api_call

# 新代码（使用）
from trace import log_auto, log_step, log_checkpoint

# 替换所有调用
log_trace(14, "xxx") → log_auto("xxx")
log_function_entry("func", 21) → log_auto("开始func")
log_function_exit("func", 118) → log_auto("完成func")
log_api_call("api", 27, before=True) → log_auto("调用api")
log_api_call("api", 29, before=False) → 删除（不需要after）
```

### 步骤2：更新其他模块

重复步骤1的模式

### 步骤3：删除旧函数（可选）

在 `trace.py` 中，可以删除标记为 DEPRECATED 的函数：
```python
# 可以删除这些（但保留也可以，向后兼容）
def log_trace(line_num, context=""):
def log_function_entry(func_name, line_num):
def log_function_exit(func_name, line_num):
def log_api_call(api_name, line_num, before=True):
```

---

## 🎯 优先级

### 高优先级（必须）
1. ✅ 测试 `test_new_trace.py` - 验证新系统工作
2. ⚠️ 测试 UE5 集成 - 运行 `generate_map.bat`

### 中优先级（建议）
3. ⚠️ 更新 `room_builder.py` 使用 `log_auto()`
4. ⚠️ 更新其他模块使用 `log_auto()`

### 低优先级（可选）
5. ⚠️ 删除 `trace.py` 中的 DEPRECATED 函数

---

## 💡 注意事项

1. **向后兼容**：旧函数仍然可用，不会破坏现有代码
2. **渐进式更新**：可以逐个模块更新，不需要一次全部更新
3. **测试优先**：先测试新系统工作，再更新旧代码

---

## 🚀 快速开始

**最小测试（验证新系统）：**
```bash
# 1. 本地测试
python test_new_trace.py

# 2. UE5测试
generate_map.bat cosmos_002_training_world

# 3. 检查输出是否包含新格式
#    [TRACE:模块名:行号:时间戳] 说明
```

**完整清理（更新所有模块）：**
```bash
# 1. 更新 room_builder.py
# 2. 更新 player_spawner.py
# 3. 更新其他模块
# 4. 测试
# 5. 删除旧函数（可选）
```

