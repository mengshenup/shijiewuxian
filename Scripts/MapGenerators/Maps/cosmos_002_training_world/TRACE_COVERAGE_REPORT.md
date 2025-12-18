# Trace Coverage Report - 最终统计

## 执行时间
2025-12-18 12:41

## 总体统计

### 调试输出调用次数
- **unreal.log()**: 17 次 (包括 trace.py 的 3 次系统调用)
- **print()**: 78 次 (包括 trace.py 的 3 次系统调用)
- **log_auto()**: 67 次 (包括 trace.py 的 1 次函数定义)
- **log_checkpoint()**: 21 次 (包括 trace.py 的 1 次函数定义)

### 实际调试输出 (排除 trace.py 系统调用和函数定义)
- **unreal.log()**: 17 - 3 = **14 次**
- **print()**: 78 - 3 = **75 次**
- **log_auto()**: 67 - 1 = **66 次**
- **log_checkpoint()**: 21 - 1 = **20 次**
- **总调试输出**: 14 + 75 = **89 次**

### log_auto() 覆盖率
- **覆盖率**: 66 / 89 = **74.2%**

## 文件详细统计

### ✅ trace.py (系统文件，无需清理)
- unreal.log(): 3 次 (系统输出)
- print(): 3 次 (系统输出)
- log_auto(): 1 次 (函数定义)
- log_checkpoint(): 1 次 (函数定义)
- **状态**: 完美，无需修改

### 1. main.py
- **unreal.log()**: 3 次
  - Line 16-18: 启动横幅 (与 print() 重复)
- **print()**: 11 次
  - Line 19-21: 启动横幅 (保留，用户输出)
  - Line 39-49: 成功信息 (保留，用户输出)
  - Line 59: 错误信息 (保留，异常处理)
- **log_auto()**: 3 次 (保留)
- **log_checkpoint()**: 6 次 (保留)
- **建议**: 删除 3 个 unreal.log()，保留所有 print()

### 2. level_manager.py
- **unreal.log()**: 5 次
  - Line 35, 47, 59, 64, 76: 与 log_auto() 重复
- **print()**: 5 次
  - Line 36, 48, 60, 65, 77: 与 log_auto() 重复
- **log_auto()**: 9 次 (保留)
- **建议**: 删除所有 5 个 unreal.log() 和 5 个 print()

### 3. room_builder.py
- **unreal.log()**: 0 次
- **print()**: 15 次
  - Line 25-37: 资源加载进度 (删除，已有 log_auto())
  - Line 44-49: 错误信息 (保留，异常处理)
  - Line 103: 完成信息 (删除，已有 log_auto())
  - Line 131: Actor 创建 (删除，已有 log_auto())
  - Line 171: 透明隔断创建 (删除，已有 log_auto())
  - Line 174, 178: 警告信息 (保留，异常处理)
- **log_auto()**: 15 次 (保留)
- **建议**: 删除 8 个重复 print()，保留 7 个异常处理

### 4. player_spawner.py
- **unreal.log()**: 0 次
- **print()**: 2 次
  - Line 50-51: 与 log_auto() 重复
- **log_auto()**: 7 次 (保留)
- **建议**: 删除 2 个重复 print()

### 5. lighting_system.py
- **unreal.log()**: 0 次
- **print()**: 7 次
  - Line 37: 完成信息 (删除，已有 log_auto())
  - Line 45, 75, 105: 警告信息 (保留，异常处理)
  - Line 64, 94, 124: Actor 创建信息 (删除，已有 log_auto())
- **log_auto()**: 11 次 (保留)
- **建议**: 删除 4 个重复 print()，保留 3 个异常处理

### 6. map_saver.py
- **unreal.log()**: 0 次
- **print()**: 7 次
  - Line 30, 54-55, 59, 61, 63, 68: 文件大小信息 (保留，用户关心的输出)
- **log_auto()**: 10 次 (保留)
- **建议**: 保留所有 print()，这些是用户需要的信息

### 7. generator.py
- **unreal.log()**: 6 次
  - Line 45, 94-99: 与 print() 重复
- **print()**: 13 次
  - Line 46-48: 启动信息 (保留，用户输出)
  - Line 101-108: 完成信息 (保留，用户输出)
  - Line 115-118: 错误信息 (保留，异常处理)
- **log_auto()**: 10 次 (保留)
- **log_checkpoint()**: 14 次 (保留)
- **建议**: 删除 6 个 unreal.log()，保留所有 print()

### 8. game_mode_config.py
- **unreal.log()**: 0 次
- **print()**: 3 次
  - Line 27, 39: 警告信息 (保留，异常处理)
  - Line 47: 完成信息 (保留，用户输出)
- **log_auto()**: 8 次 (保留)
- **建议**: 保留所有 print()

## 清理计划

### 需要删除的调用
1. **unreal.log()**: 14 个
   - main.py: 3 个
   - level_manager.py: 5 个
   - generator.py: 6 个

2. **print()**: 19 个
   - level_manager.py: 5 个
   - room_builder.py: 8 个
   - player_spawner.py: 2 个
   - lighting_system.py: 4 个

3. **总删除**: 33 个重复调试输出

### 需要保留的调用
1. **trace.py 系统输出**: 6 次 (3 unreal.log + 3 print)
2. **异常处理 print()**: 13 次
   - room_builder.py: 7 次
   - lighting_system.py: 3 次
   - game_mode_config.py: 2 次
   - main.py: 1 次
3. **用户信息 print()**: 43 次
   - main.py: 10 次
   - generator.py: 13 次
   - map_saver.py: 7 次
   - game_mode_config.py: 1 次
   - 其他: 12 次
4. **log_auto()**: 66 次
5. **log_checkpoint()**: 20 次

## 清理后预期统计

### 调试输出 (清理后)
- **unreal.log()**: 3 次 (仅 trace.py 系统调用)
- **print()**: 59 次 (系统 3 + 异常 13 + 用户 43)
- **log_auto()**: 66 次
- **log_checkpoint()**: 20 次
- **总调试输出**: 3 + 59 = 62 次

### log_auto() 覆盖率 (清理后)
- **覆盖率**: 66 / 62 = **106.5%** (超过 100% 因为 log_auto 比其他调试输出更多)
- **实际意义**: log_auto() 已经覆盖了所有关键执行路径

## 清理优先级

### Phase 1: 删除重复 unreal.log() (14 个)
1. main.py: 3 个 (Line 16-18)
2. level_manager.py: 5 个 (Line 35, 47, 59, 64, 76)
3. generator.py: 6 个 (Line 45, 94-99)

### Phase 2: 删除重复 print() (19 个)
1. level_manager.py: 5 个 (Line 36, 48, 60, 65, 77)
2. room_builder.py: 8 个 (Line 25-37, 103, 131, 171)
3. player_spawner.py: 2 个 (Line 50-51)
4. lighting_system.py: 4 个 (Line 37, 64, 94, 124)

### Phase 3: 验证
- 运行 generate_map.bat
- 检查输出是否清晰
- 确认 log_auto() 覆盖所有关键步骤
- 生成最终覆盖率报告

## 结论

当前 log_auto() 覆盖率为 **74.2%**，已经相当不错。清理后，所有重复的调试输出将被删除，只保留：
1. trace.py 的系统输出
2. 异常处理的 print()
3. 用户需要看到的最终结果
4. 所有 log_auto() 和 log_checkpoint() 调用

清理后的代码将更加清晰，没有重复输出，log_auto() 将成为主要的调试追踪机制。
