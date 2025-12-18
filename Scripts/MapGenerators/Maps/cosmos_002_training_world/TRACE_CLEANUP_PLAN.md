# Trace Cleanup Plan - log_auto() 覆盖率分析

## 当前统计 (清理前)

### 总体统计
- **unreal.log() 调用**: 16 次 (包括 trace.py 的 3 次系统调用)
- **print() 调用**: 49 次 (包括 trace.py 的 3 次系统调用)
- **log_auto() 调用**: 26 次
- **log_checkpoint() 调用**: 18 次
- **log_step() 调用**: 6 次

### 覆盖率计算
- **总调试输出**: 16 + 49 = 65 次
- **trace.py 系统输出**: 3 + 3 = 6 次 (不计入)
- **实际调试输出**: 65 - 6 = 59 次
- **log_auto() 覆盖**: 26 / 59 = **44.1%**

## 文件详细分析

### ✅ trace.py (无需清理)
- **unreal.log()**: 3 次 (系统输出，保留)
- **print()**: 3 次 (系统输出，保留)
- **log_auto()**: 1 次 (函数定义)
- **log_checkpoint()**: 1 次 (函数定义)
- **状态**: 完美，无需修改

### 1. main.py (需要清理)
- **unreal.log()**: 3 次 → 删除
  - Line 16-18: 启动横幅 (重复，删除)
- **print()**: 9 次 → 保留 2 次
  - Line 19-21: 启动横幅 (保留)
  - Line 39-49: 成功输出 (保留)
  - Line 59-62: 错误输出 (保留，异常处理)
- **log_auto()**: 3 次 (保留)
- **log_checkpoint()**: 6 次 (保留)
- **建议**: 删除 3 个 unreal.log()，保留必要的 print()

### 2. level_manager.py (需要清理)
- **unreal.log()**: 5 次 → 删除全部
  - Line 35, 47, 59, 64, 76: 与 log_auto() 重复
- **print()**: 6 次 → 删除全部
  - Line 37, 49, 61, 66, 78: 与 log_auto() 重复
- **log_auto()**: 5 次 (保留)
- **建议**: 删除所有 unreal.log() 和 print()，已有 log_auto() 覆盖

### 3. room_builder.py (需要清理)
- **unreal.log()**: 0 次
- **print()**: 15 次 → 保留 3 次
  - Line 25-39: 资源加载进度 (删除，已有 log_auto())
  - Line 44-49: 错误信息 (保留，异常处理)
  - Line 103: 完成信息 (删除，已有 log_auto())
  - Line 131: Actor 创建 (删除，已有 log_auto())
  - Line 171: 透明隔断创建 (删除，已有 log_auto())
  - Line 174, 178: 警告信息 (保留，异常处理)
- **log_auto()**: 9 次 (保留)
- **建议**: 删除 12 个重复 print()，保留 3 个异常处理

### 4. player_spawner.py (需要清理)
- **unreal.log()**: 0 次
- **print()**: 2 次 → 删除全部
  - Line 50-51: 与 log_auto() 重复
- **log_auto()**: 6 次 (保留)
- **建议**: 删除 2 个重复 print()

### 5. lighting_system.py (需要清理)
- **unreal.log()**: 0 次
- **print()**: 6 次 → 删除全部
  - Line 37, 45, 64, 75, 94, 105, 124: 与 log_auto() 重复
- **log_auto()**: 7 次 (保留)
- **建议**: 删除所有重复 print()

### 6. map_saver.py (需要清理)
- **unreal.log()**: 0 次
- **print()**: 6 次 → 保留全部
  - Line 30, 54-55, 59, 61, 63, 68: 文件大小信息 (保留，用户关心的输出)
- **log_auto()**: 7 次 (保留)
- **建议**: 保留所有 print()，这些是用户需要的信息

### 7. generator.py (需要清理)
- **unreal.log()**: 5 次 → 删除全部
  - Line 45, 94-98: 与 log_auto() 重复
- **print()**: 2 次 → 保留全部
  - Line 47-48, 102-109: 用户输出 (保留)
- **log_auto()**: 9 次 (保留)
- **log_checkpoint()**: 12 次 (保留)
- **建议**: 删除 5 个 unreal.log()，保留 print()

### ✅ game_mode_config.py (无需清理)
- **unreal.log()**: 0 次
- **print()**: 0 次
- **log_auto()**: 1 次
- **log_checkpoint()**: 0 次
- **状态**: 完美，无需修改

## 清理目标

### 删除统计
- **unreal.log()**: 16 - 3 (trace.py) = **13 个需要删除**
- **print()**: 49 - 3 (trace.py) - 20 (保留) = **26 个需要删除**
- **总删除**: 39 个重复调试输出

### 保留统计
- **trace.py 系统输出**: 6 次
- **异常处理 print()**: 5 次 (room_builder.py)
- **用户信息 print()**: 15 次 (main.py, map_saver.py, generator.py)
- **log_auto()**: 26 次
- **log_checkpoint()**: 18 次
- **log_step()**: 6 次

### 清理后统计 (预期)
- **unreal.log()**: 3 次 (仅 trace.py 系统调用)
- **print()**: 23 次 (系统 3 + 异常 5 + 用户 15)
- **log_auto()**: 26 次
- **log_checkpoint()**: 18 次
- **log_step()**: 6 次
- **总调试输出**: 3 + 23 = 26 次
- **log_auto() 覆盖率**: 26 / (26 + 18 + 6) = **52.0%** (仅计算 trace 函数)

## 清理顺序

1. ✅ **trace.py** - 无需清理
2. **main.py** - 删除 3 个 unreal.log()
3. **level_manager.py** - 删除 5 个 unreal.log() + 6 个 print()
4. **room_builder.py** - 删除 12 个 print()
5. **player_spawner.py** - 删除 2 个 print()
6. **lighting_system.py** - 删除 6 个 print()
7. **map_saver.py** - 无需清理 (用户信息)
8. **generator.py** - 删除 5 个 unreal.log()
9. ✅ **game_mode_config.py** - 无需清理

## 清理原则

### 删除条件
1. **与 log_auto() 重复**: 同一位置既有 log_auto() 又有 unreal.log()/print()
2. **调试信息**: 仅用于开发调试的输出
3. **进度信息**: 已被 log_auto() 覆盖的进度输出

### 保留条件
1. **异常处理**: 错误、警告、异常信息
2. **用户信息**: 用户需要看到的最终结果
3. **系统输出**: trace.py 的系统级输出
4. **文件大小**: map_saver.py 的文件大小对比

## 执行计划

### Phase 1: 删除重复 unreal.log() (13 个)
- main.py: 3 个
- level_manager.py: 5 个
- generator.py: 5 个

### Phase 2: 删除重复 print() (26 个)
- level_manager.py: 6 个
- room_builder.py: 12 个
- player_spawner.py: 2 个
- lighting_system.py: 6 个

### Phase 3: 验证
- 运行 generate_map.bat
- 检查输出是否清晰
- 确认 log_auto() 覆盖所有关键步骤
- 生成最终覆盖率报告

## 最终目标

- **unreal.log()**: 3 次 (仅系统)
- **print()**: 23 次 (系统 + 异常 + 用户)
- **log_auto()**: 26 次
- **log_auto() 覆盖率**: 52.0%
- **输出清晰度**: 无重复，无冗余
- **用户体验**: 保留所有必要信息
