# Trace 覆盖率分析工具使用指南

## 工具概览

本项目提供两种覆盖率分析工具：
1. **批处理工具** - 快速统计，无需 Python
2. **Python 工具** - 详细分析，需要 Python 3

## 1. 批处理工具 (推荐 - 快速使用)

### 位置
```
Scripts/MapGenerators/analyze_coverage.bat
```

### 使用方法
```bash
cd Scripts\MapGenerators
.\analyze_coverage.bat
```

### 功能
- ✅ 快速统计所有调试输出类型
- ✅ 计算 log_auto() 覆盖率
- ✅ 计算非 log_auto() 覆盖率
- ✅ 显示详细调用位置
- ✅ 提供清理建议
- ✅ 无需 Python 环境

### 输出示例
```
=== 统计摘要 ===
  unreal.log()     : 17 次
  print()          : 72 次
  log_auto()       : 80 次
  log_checkpoint() : 22 次

=== 覆盖率分析 ===
  实际调试输出 (排除 trace.py 系统调用):
    unreal.log()     : 14 次
    print()          : 69 次
    总调试输出       : 83 次

  Trace 函数:
    log_auto()       : 79 次
    log_checkpoint() : 21 次

  log_auto() 覆盖率      : 95% (79/83)
  非log_auto() 覆盖率    : 5% (4/83)

  非log_auto()类型详细:
    unreal.log()     : 14 次 (16%)
    print()          : 69 次 (83%)
```

## 2. Python 工具 (详细分析)

### 位置
```
Scripts/MapGenerators/Tools/analyze_trace_coverage.py
```

### 使用方法

**方法 1: 直接运行**
```bash
cd Scripts\MapGenerators
py -3 Tools\analyze_trace_coverage.py
```

**方法 2: 使用 python 命令**
```bash
cd Scripts\MapGenerators
python Tools\analyze_trace_coverage.py
```

### 功能
- ✅ 详细的文件级统计
- ✅ 覆盖率可视化图表
- ✅ 文件对比表格
- ✅ 分类 print() 调用 (异常处理/用户输出/调试输出)
- ✅ 详细的清理建议
- ✅ log_auto() 和非 log_auto() 覆盖率
- ✅ 中文输出

### 输出示例
```
================================================================================
TRACE 覆盖率分析报告
================================================================================

【总体统计】
  unreal.log()    :  17 次
  print()         :  72 次
  log_auto()      :  80 次
  log_checkpoint():  22 次
  log_step()      :   7 次

【实际调试输出】(排除 trace.py 系统调用)
  unreal.log()    :  14 次
  print()         :  69 次
  总调试输出      :  83 次

【Trace 函数】
  log_auto()      :  79 次
  log_checkpoint():  21 次
  log_step()      :   7 次

【覆盖率】
  log_auto() 覆盖率    : 95.2% (79/83)
  非log_auto() 覆盖率  : 4.8% (4/83)

  评级: 优秀 ✓

  【非log_auto()类型详细统计】
  unreal.log()         :  14 次 (16.9%)
  print()              :  69 次 (83.1%)

================================================================================
文件对比表格
================================================================================

文件名                       unreal   print    log_auto   覆盖率        状态
--------------------------------------------------------------------------------
game_mode_config.py       0        3        8          266.7%     ✓ 优秀
generator.py              6        14       12         60.0%      △ 一般
level_manager.py          5        5        10         100.0%     ✓ 优秀
lighting_system.py        0        7        12         171.4%     ✓ 优秀
main.py                   3        15       3          16.7%      ✗ 需改进
map_saver.py              0        7        10         142.9%     ✓ 优秀
player_spawner.py         0        2        7          350.0%     ✓ 优秀
room_builder.py           0        16       17         106.2%     ✓ 优秀
trace.py                  3        3        1          N/A        系统文件

================================================================================
覆盖率可视化
================================================================================

game_mode_config.py   [████████████████████████████████████████] 266.7%
generator.py          [████████████████░░░░░░░░░░░░░░░░░░░░░░░░]  60.0%
level_manager.py      [████████████████████████████████████████] 100.0%
lighting_system.py    [████████████████████████████████████████] 171.4%
main.py               [██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  16.7%
map_saver.py          [████████████████████████████████████████] 142.9%
player_spawner.py     [████████████████████████████████████████] 350.0%
room_builder.py       [████████████████████████████████████████] 106.2%
```

## 工具对比

| 特性 | 批处理工具 | Python 工具 |
|------|-----------|------------|
| 运行速度 | ⚡ 快速 | 🐌 较慢 |
| 环境要求 | ✅ 无需 Python | ❌ 需要 Python 3 |
| 基本统计 | ✅ | ✅ |
| 覆盖率计算 | ✅ | ✅ |
| 非log_auto()统计 | ✅ | ✅ |
| 文件对比表格 | ❌ | ✅ |
| 可视化图表 | ❌ | ✅ |
| 分类分析 | ❌ | ✅ |
| 详细清理建议 | ⚠️ 简单 | ✅ 详细 |

## 推荐使用场景

### 使用批处理工具
- ✅ 快速检查覆盖率
- ✅ 不想安装 Python
- ✅ 只需要基本统计
- ✅ 在 CI/CD 中使用

### 使用 Python 工具
- ✅ 需要详细分析
- ✅ 需要可视化图表
- ✅ 需要分类统计
- ✅ 准备清理代码前的详细评估

## 常见问题

### Q: Python 工具运行失败怎么办？
A: 尝试以下方法：
1. 确认 Python 3 已安装: `py -3 --version`
2. 使用 `py -3` 而不是 `python`
3. 如果还是失败，使用批处理工具

### Q: 覆盖率超过 100% 是什么意思？
A: 这表示 log_auto() 的数量超过了 unreal.log() + print() 的总和，说明：
- log_auto() 提供了更详细的追踪
- 代码已经很好地使用了 log_auto()
- 这是好事！

### Q: 哪些 print() 应该保留？
A: 应该保留：
- 异常处理的 print() (ERROR, WARNING)
- 用户需要看到的输出 (SUCCESS, 文件大小等)
- 不应该保留：
- 与 log_auto() 重复的调试输出

### Q: 删除了 analyze_coverage_py.bat 有影响吗？
A: 没有影响。这是一个临时启动器文件，可以直接运行 Python 脚本：
```bash
py -3 Tools\analyze_trace_coverage.py
```

## 下一步

运行分析后，参考以下文档进行清理：
- `TRACE_COVERAGE_FINAL.md` - 最终分析报告
- `TRACE_CLEANUP_PLAN.md` - 清理计划
- `TRACE_COVERAGE_REPORT.md` - 详细报告
