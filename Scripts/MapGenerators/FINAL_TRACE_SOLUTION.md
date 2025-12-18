# 🎯 最终追踪方案（简化版）

## ✅ 核心原则

1. **只用一个函数** `log_auto()` - 简单易用
2. **自动获取信息** - 模块名、行号、时间戳
3. **输出格式简洁** - 便于解析
4. **最终显示美观** - 清晰的列表格式

---

## 📝 实现方案

### 1️⃣ 简化的 `trace.py`

```python
"""
UE5-compatible execution tracing module (Simplified)
自动追踪，无需硬编码行号
"""

import unreal
import inspect
import time


# 全局变量：记录脚本启动时间
_start_time = time.time()


def log_auto(context=""):
    """
    自动追踪当前执行位置
    
    Args:
        context: 可选的上下文描述
    
    输出格式：
        [TRACE:模块名:行号:时间戳] 上下文
    
    示例：
        [TRACE:level_manager:25:1234.567] 准备Level
    """
    # 获取调用者的栈帧
    frame = inspect.currentframe().f_back
    
    # 自动获取模块名（从文件名提取）
    filename = frame.f_code.co_filename
    module_name = filename.split('/')[-1].split('\\')[-1].replace('.py', '')
    
    # 自动获取行号
    line_num = frame.f_lineno
    
    # 获取时间戳（相对于脚本启动时间，毫秒）
    elapsed_ms = int((time.time() - _start_time) * 1000)
    
    # 输出追踪标记（简洁格式）
    marker = f"[TRACE:{module_name}:{line_num}:{elapsed_ms}]"
    if context:
        marker += f" {context}"
    
    unreal.log(marker)
    print(marker, flush=True)


def log_step(step_num, total_steps, description):
    """
    进度步骤追踪（保持不变）
    
    Args:
        step_num: 当前步骤号
        total_steps: 总步骤数
        description: 步骤描述
    """
    marker = f"[{step_num}/{total_steps}] {description}"
    unreal.log(marker)
    print(marker)
    import sys
    sys.stdout.flush()


def log_checkpoint(checkpoint_name):
    """
    检查点追踪（自动获取行号）
    
    Args:
        checkpoint_name: 检查点名称
    """
    frame = inspect.currentframe().f_back
    line_num = frame.f_lineno
    elapsed_ms = int((time.time() - _start_time) * 1000)
    
    marker = f"[CHECKPOINT:{line_num}:{elapsed_ms}] {checkpoint_name}"
    unreal.log(marker)
    print(marker, flush=True)
```

---

### 2️⃣ 使用示例（超级简单）

```python
# level_manager.py
from trace import log_auto, log_step, log_checkpoint

def create_new_level(map_path):
    """创建新Level"""
    log_step(1, 6, "创建Level")
    
    log_auto("准备Level")  # ✅ 说明会显示在最终输出
    editor_level_lib = unreal.EditorLevelLibrary()
    
    log_auto("检查地图是否存在")  # ✅ 说明会显示
    if editor_asset_lib.does_asset_exist(map_path):
        log_auto("地图已存在，加载中")  # ✅ 说明会显示
        editor_level_lib.load_level(map_path)
    else:
        log_auto("创建新地图")  # ✅ 说明会显示
        world = editor_level_lib.new_level(map_path)
    
    log_auto("获取World引用")  # ✅ 说明会显示
    world = editor_level_lib.get_editor_world()
    
    log_checkpoint("LEVEL_CREATED")
    return world


# room_builder.py
from trace import log_auto, log_step

def place_training_room(world):
    """放置训练室"""
    log_step(2, 6, "构建训练室")
    
    log_auto("加载Cube网格")  # ✅ 说明：加载Cube网格
    cube_mesh = load_asset("/Engine/BasicShapes/Cube")
    
    log_auto("创建墙壁")  # ✅ 说明：创建墙壁
    walls = create_walls(world, cube_mesh)
    
    log_auto("创建地板")  # ✅ 说明：创建地板
    floor = create_floor(world, cube_mesh)
    
    log_auto("训练室完成")  # ✅ 说明：训练室完成
    return walls + [floor]
```

---

### 3️⃣ 原始输出（实时，用于调试）

```
[1/6] 创建Level
[TRACE:level_manager:15:1234] 准备Level
[TRACE:level_manager:18:1245] 检查地图是否存在
[TRACE:level_manager:20:1256] 地图已存在，加载中
[TRACE:level_manager:25:1890] 获取World引用
[CHECKPOINT:28:1920] LEVEL_CREATED
[2/6] 构建训练室
[TRACE:room_builder:10:1950] 加载Cube网格
[TRACE:room_builder:15:2100] 创建墙壁
[TRACE:room_builder:25:2450] 创建地板
[TRACE:room_builder:35:2780] 训练室完成
```

**说明：**
- ✅ `log_auto("创建墙壁")` 中的 `"创建墙壁"` 就是说明
- ✅ 这个说明会被 `launch_generator.py` 解析
- ✅ 最终显示在表格的"说明"列

---

### 4️⃣ 最终显示（美观，用于报告）

`launch_generator.py` 解析后显示：

```
============================================================
  执行摘要
============================================================
[1/6] 创建Level
[2/6] 构建训练室
[3/6] 放置PlayerStart
[4/6] 设置照明
[5/6] 配置GameMode
[6/6] 保存地图

构建进度:
  步骤完成: 6/6 (100%)
    ✓ [1/6]
    ✓ [2/6]
    ✓ [3/6]
    ✓ [4/6]
    ✓ [5/6]
    ✓ [6/6]

📍 执行追踪:
  当前模块: map_saver.py
  模块行号: 42
  执行时间: 5.234秒

  📜 模块执行历史（共 25 条，按执行顺序）:
      序号  模块                    行号  说明                      耗时(ms)  总共(ms)
      ─────────────────────────────────────────────────────────────────────────────
        1.  level_manager.py        L15   准备Level                    11ms      1234ms
        2.  level_manager.py        L18   检查地图是否存在              11ms      1245ms
        3.  level_manager.py        L20   地图已存在，加载中           634ms      1890ms
        4.  level_manager.py        L25   获取World引用                 30ms      1920ms
        5.  room_builder.py         L10   加载Cube网格                  30ms      1950ms
        6.  room_builder.py         L15   创建墙壁                     150ms      2100ms
        7.  room_builder.py         L25   创建地板                     350ms      2450ms

  💡 时间说明：
      • 耗时(ms)：这一步花了多少时间（当前步骤 - 上一步骤）
      • 总共(ms)：从脚本启动到现在总共花了多少时间
      
      图解：
      ┌─────────────────────────────────────────────────────────────┐
      │  脚本启动                                                    │
      │  ↓ (1234ms后)                                               │
      │  步骤1: 准备Level                                            │
      │  ↓ 耗时11ms (1234→1245)                                     │
      │  步骤2: 检查地图是否存在      总共1245ms                     │
      │  ↓ 耗时634ms (1245→1890)                                    │
      │  步骤3: 地图已存在，加载中    总共1890ms  ← 最慢的步骤！     │
      │  ↓ 耗时30ms (1890→1920)                                     │
      │  步骤4: 获取World引用         总共1920ms                     │
      └─────────────────────────────────────────────────────────────┘
      
      实际示例：
        步骤1：耗时11ms，总共1234ms
          → 这一步花了11ms，从脚本启动到现在总共1234ms
        
        步骤3：耗时634ms，总共1890ms
          → 这一步花了634ms（加载地图很慢！），总共1890ms
        8.  room_builder.py         L35   训练室完成                   330ms      2780ms
        9.  player_spawner.py       L12   加载PlayerStart类             45ms      2825ms
       10.  player_spawner.py       L25   设置PlayerStart位置          120ms      2945ms
       11.  player_spawner.py       L34   PlayerStart放置完成           80ms      3025ms
       12.  lighting_system.py      L15   创建DirectionalLight          60ms      3085ms
       13.  lighting_system.py      L28   设置光照参数                 200ms      3285ms
       14.  lighting_system.py      L42   照明系统配置完成             150ms      3435ms
       15.  game_mode_config.py     L10   获取WorldSettings             40ms      3475ms
       16.  game_mode_config.py     L22   设置GameMode                  90ms      3565ms
       17.  game_mode_config.py     L35   GameMode配置完成              70ms      3635ms
       18.  map_saver.py            L15   准备保存地图                  50ms      3685ms
       19.  map_saver.py            L28   保存地图文件                 800ms      4485ms
       20.  map_saver.py            L42   验证地图保存                 749ms      5234ms
       21.  generator.py            L50   清理临时对象                  15ms      5249ms
       22.  generator.py            L65   生成完成报告                  20ms      5269ms
       23.  main.py                 L30   脚本执行完成                  10ms      5279ms

  ⏱️  性能分析:
      最慢的3个步骤:
        1. map_saver.py:L28 → 800ms (保存地图文件)
        2. map_saver.py:L42 → 749ms (验证地图保存)
        3. level_manager.py:L20 → 634ms (地图已存在，加载中)

✓ 成功: 地图文件已生成
  路径: D:\001xm\shijiewuxian\Content\Maps\Cosmos_002_Training_World.umap
  文件大小: 1,456,789 bytes (1422.64 KB)
  总耗时: 5.279秒
============================================================
```

---

## 🔧 实现细节

### 增强 `trace_parser.py`

```python
import time

class TraceInfo:
    def __init__(self):
        # ... 现有字段 ...
        
        # 新增：模块执行历史（完整记录）
        self.module_history = []  # 格式: {'module': str, 'line': int, 'timestamp': int, 'context': str}
        self.start_time = None    # 脚本启动时间


def _parse_trace_marker(line, trace_info):
    """解析追踪标记"""
    try:
        # 解析新格式: [TRACE:模块名:行号:时间戳] 上下文
        if '[TRACE:' in line and 'LogPython' in line:
            # 提取标记部分
            marker_start = line.find('[TRACE:')
            marker_end = line.find(']', marker_start)
            
            if marker_start != -1 and marker_end != -1:
                marker = line[marker_start+7:marker_end]  # 去掉 "[TRACE:"
                parts = marker.split(':')
                
                if len(parts) >= 3:
                    module_name = parts[0]
                    line_num = int(parts[1])
                    timestamp_ms = int(parts[2])
                    
                    # 提取上下文
                    context = line[marker_end+1:].strip() if marker_end+1 < len(line) else ""
                    
                    # 更新当前状态
                    trace_info.current_module = module_name
                    trace_info.current_module_line = line_num
                    
                    # 记录历史
                    trace_info.module_history.append({
                        'module': module_name,
                        'line': line_num,
                        'timestamp': timestamp_ms,
                        'context': context
                    })
                    
                    # 记录启动时间（第一条记录）
                    if trace_info.start_time is None:
                        trace_info.start_time = timestamp_ms
        
        # 解析检查点: [CHECKPOINT:行号:时间戳] 名称
        elif '[CHECKPOINT:' in line:
            marker_start = line.find('[CHECKPOINT:')
            marker_end = line.find(']', marker_start)
            
            if marker_start != -1 and marker_end != -1:
                marker = line[marker_start+12:marker_end]
                parts = marker.split(':')
                
                if len(parts) >= 2:
                    line_num = int(parts[0])
                    timestamp_ms = int(parts[1])
                    checkpoint_name = line[marker_end+1:].strip()
                    
                    trace_info.last_checkpoint = checkpoint_name
                    trace_info.last_trace_line = line_num
        
    except:
        pass
```

### 增强输出显示

```python
def print_trace_history(trace_info):
    """打印模块执行历史（美观格式）"""
    if not trace_info.module_history:
        print("\n  📜 模块执行历史: (无)")
        return
    
    history = trace_info.module_history
    total_count = len(history)
    
    print(f"\n  📜 模块执行历史（共 {total_count} 条，按执行顺序）:")
    print(f"      {'序号':<4}  {'模块':<20}  {'行号':<6}  {'说明':<25}  {'耗时':<10}  {'总共':<10}")
    print(f"      {'─'*95}")
    
    for i, entry in enumerate(history, 1):
        module = entry['module'] + '.py'
        line = f"L{entry['line']}"
        timestamp = entry['timestamp']
        context = entry.get('context', '')  # 获取说明
        
        # 计算耗时（与上一条的时间差）
        if i == 1:
            elapsed = 0
        else:
            elapsed = timestamp - history[i-2]['timestamp']
        
        print(f"      {i:3d}.  {module:<20}  {line:<6}  {context:<25}  {elapsed:6d}ms  {timestamp:8d}ms")
    
    # 性能分析：找出最慢的3个步骤
    if len(history) > 1:
        # 计算每步耗时
        steps_with_time = []
        for i in range(1, len(history)):
            elapsed = history[i]['timestamp'] - history[i-1]['timestamp']
            steps_with_time.append({
                'module': history[i]['module'],
                'line': history[i]['line'],
                'elapsed': elapsed,
                'context': history[i]['context']
            })
        
        # 排序找出最慢的3个
        slowest = sorted(steps_with_time, key=lambda x: x['elapsed'], reverse=True)[:3]
        
        print(f"\n  ⏱️  性能分析:")
        print(f"      最慢的3个步骤:")
        for i, step in enumerate(slowest, 1):
            context = f"({step['context']})" if step['context'] else ""
            print(f"        {i}. {step['module']}.py:L{step['line']} → {step['elapsed']}ms {context}")
```

---

## 📊 对比

| 特性 | 旧方案 | 新方案 |
|------|--------|--------|
| 函数数量 | 多个 | 1个主函数 |
| 硬编码行号 | ❌ 需要 | ✅ 不需要 |
| 输出格式 | 冗长 | 简洁 |
| 最终显示 | 原始 | 美观表格 |
| 时间追踪 | ❌ 无 | ✅ 毫秒级 |
| 性能分析 | ❌ 无 | ✅ 自动分析 |

---

## 🎯 总结

**最终方案特点：**
1. ✅ 只用一个函数 `log_auto()`
2. ✅ 自动获取模块名、行号、时间戳
3. ✅ 输出格式简洁（便于解析）
4. ✅ 最终显示美观（表格格式）
5. ✅ 自动性能分析（找出最慢步骤）
6. ✅ 完全兼容 UE5.7.0

**使用超级简单：**
```python
from trace import log_auto

def my_function():
    log_auto("开始")
    # ... 代码 ...
    log_auto("完成")
```

**这才是最终的完美方案！** 🎉
