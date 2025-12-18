# 设计文档

## 概述

本功能为地图生成追踪系统的模块执行历史表格添加可视化状态标志。系统将通过关键词自动推断或显式指定的方式，为每个追踪条目分配状态（成功✅、警告⚠️、错误❌、信息ℹ️），并在执行历史表格中显示。

## 架构

### 组件关系图

```
┌─────────────────────────────────────────────────────────────┐
│                    Map Generation Script                     │
│  (level_manager.py, room_builder.py, player_spawner.py...)  │
└───────────────────────┬─────────────────────────────────────┘
                        │ calls
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      trace.py                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  log_auto(context, status=None)                      │   │
│  │    1. 获取调用者信息（模块名、行号）                  │   │
│  │    2. 推断或使用显式status                            │   │
│  │    3. 记录到全局trace数据                             │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  infer_status(context) → status                      │   │
│  │    根据关键词推断状态                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │ writes to
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  UE5 Log Output                              │
│  [TRACE:module:line:timestamp:status] context                │
└───────────────────────┬─────────────────────────────────────┘
                        │ parsed by
                        ▼
┌─────────────────────────────────────────────────────────────┐
│            Tools/launch_generator/trace_parser.py            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  parse_trace_line(line) → dict                       │   │
│  │    解析TRACE标记，提取status字段                      │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │ stores in
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                     TraceInfo                                │
│  module_history = [                                          │
│    {'module': str, 'line': int, 'timestamp': int,           │
│     'context': str, 'status': str},                          │
│    ...                                                       │
│  ]                                                           │
└───────────────────────┬─────────────────────────────────────┘
                        │ displayed by
                        ▼
┌─────────────────────────────────────────────────────────────┐
│          Tools/launch_generator/result_analyzer.py           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  print_trace_history(trace_info)                     │   │
│  │    1. 推断缺失的status（向后兼容）                    │   │
│  │    2. 格式化表格，包含状态列                          │   │
│  │    3. 显示状态图标                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  get_status_icon(status) → str                       │   │
│  │    返回对应的表情符号图标                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 组件和接口

### 1. trace.py 模块

#### 1.1 状态推断函数

```python
def infer_status(context: str) -> str:
    """
    根据context文字推断状态
    
    Args:
        context: 追踪上下文描述
        
    Returns:
        status: "success", "warning", "error", 或 "info"
        
    优先级规则：
        1. 错误关键词 > 警告关键词 > 成功关键词
        2. 无匹配 → 默认 "info"
    """
```

**关键词定义：**
```python
ERROR_KEYWORDS = ["错误", "失败", "异常"]
WARNING_KEYWORDS = ["警告", "跳过", "未找到"]
SUCCESS_KEYWORDS = ["成功", "完成", "创建", "生成", "保存", 
                    "验证成功", "放置成功", "配置", "初始化"]
```

#### 1.2 增强的 log_auto 函数

```python
def log_auto(context="", status=None):
    """
    自动记录当前执行位置（增强版，支持状态）
    
    Args:
        context: 可选的上下文描述
        status: 可选的显式状态 ("success", "warning", "error", "info")
                如果为None，将自动从context推断
    
    输出格式:
        [TRACE:module_name:line_number:timestamp_ms:status] context
    
    示例:
        [TRACE:room_builder:25:2450:success] 创建地板
        [TRACE:room_builder:30:2500:error] 错误：资源加载失败
    """
```

### 2. trace_parser.py 模块

#### 2.1 增强的解析函数

```python
def parse_trace_line(line: str) -> dict:
    """
    解析TRACE标记行（支持status字段）
    
    Args:
        line: 日志行
        
    Returns:
        dict: {
            'module': str,
            'line': int,
            'timestamp': int,
            'context': str,
            'status': str  # 新增字段
        }
        
    兼容性：
        - 新格式：[TRACE:module:line:timestamp:status] context
        - 旧格式：[TRACE:module:line:timestamp] context
          （旧格式将从context推断status）
    """
```

### 3. result_analyzer.py 模块

#### 3.1 状态图标映射函数

```python
def get_status_icon(status: str) -> str:
    """
    获取状态对应的图标
    
    Args:
        status: "success", "warning", "error", 或 "info"
        
    Returns:
        icon: 对应的表情符号
    """
    STATUS_ICONS = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }
```

#### 3.2 增强的历史显示函数

```python
def print_trace_history(trace_info):
    """
    打印模块执行历史（包含状态列）
    
    表格格式：
        序号  模块                行号    说明                      状态    耗时      总共
        ─────────────────────────────────────────────────────────────────────────────
        1.    level_manager.py    L15     LevelManager初始化        ✅      0ms       0ms
        2.    level_manager.py    L25     开始准备Level             ℹ️      5ms       5ms
        3.    room_builder.py     L30     资源加载成功: SM_Cube     ✅      120ms     125ms
        4.    room_builder.py     L33     资源加载失败: SM_Plane    ❌      10ms      135ms
        5.    lighting_system.py  L44     警告：加载SkyLight类失败  ⚠️      50ms      185ms
    """
```

## 数据模型

### TraceInfo 数据结构

```python
class TraceInfo:
    def __init__(self):
        # ... 现有字段 ...
        
        # 模块执行历史（增强版）
        self.module_history = []  # List[dict]
        # 每个条目格式：
        # {
        #     'module': str,      # 模块名（不含.py）
        #     'line': int,        # 行号
        #     'timestamp': int,   # 时间戳（毫秒）
        #     'context': str,     # 上下文描述
        #     'status': str       # 状态：success/warning/error/info（新增）
        # }
```

### TRACE 标记格式

**新格式（包含status）：**
```
[TRACE:module_name:line_number:timestamp_ms:status] context
```

**示例：**
```
[TRACE:room_builder:30:2450:success] 资源加载成功: SM_Cube
[TRACE:room_builder:33:2500:error] 资源加载失败: SM_Plane
[TRACE:lighting_system:44:3000:warning] 警告：加载SkyLight类失败
[TRACE:level_manager:15:100:info] LevelManager初始化
```

**旧格式（向后兼容）：**
```
[TRACE:module_name:line_number:timestamp_ms] context
```
解析器将从context推断status。

## 正确性属性

*属性是一个应该在所有有效执行中保持为真的特征或行为——本质上是关于系统应该做什么的形式化陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。*

### 属性 1：状态推断一致性
*对于任何* 包含成功关键词的context字符串，如果不包含错误或警告关键词，则 `infer_status(context)` 应该返回 "success"
**验证：需求 4.1**

### 属性 2：错误关键词优先级
*对于任何* 同时包含错误关键词和成功关键词的context字符串（如"加载失败"），`infer_status(context)` 应该返回 "error" 而不是 "success"
**验证：需求 4.8**

### 属性 3：显式状态优先
*对于任何* context和显式status参数，调用 `log_auto(context, status=explicit_status)` 后，记录的trace条目的status字段应该等于 `explicit_status`，而不是从context推断的状态
**验证：需求 2.6, 4.5**

### 属性 4：默认状态推断
*对于任何* 不包含任何关键词的context字符串，`infer_status(context)` 应该返回 "info"
**验证：需求 4.4**

### 属性 5：状态图标映射完整性
*对于任何* 有效的status值（"success", "warning", "error", "info"），`get_status_icon(status)` 应该返回非空字符串
**验证：需求 1.2, 1.3, 1.4, 1.5**

### 属性 6：表格格式一致性
*对于任何* trace历史列表，`print_trace_history()` 输出的每一行（除表头外）应该具有相同的列数和列宽度
**验证：需求 3.3**

### 属性 7：向后兼容性
*对于任何* 不包含status字段的旧trace数据条目，显示时应该能够从context推断status并正常显示，不应该崩溃
**验证：需求 5.2, 5.5**

### 属性 8：状态持久化
*对于任何* 调用 `log_auto(context, status)` 的情况，生成的TRACE标记应该包含status字段，并且解析后的数据结构应该包含相同的status值
**验证：需求 2.1, 2.5**

### 属性 9：中文关键词支持
*对于任何* 包含中文成功关键词（如"成功"、"完成"）的context，`infer_status(context)` 应该正确识别并返回 "success"
**验证：需求 4.6**

### 属性 10：无效状态处理
*对于任何* 无效的status值（不在["success", "warning", "error", "info"]中），系统应该默认使用 "info" 并记录警告，而不是崩溃
**验证：需求 2.3**

## 错误处理

### 1. 无效status参数
- **场景**：调用 `log_auto(context, status="invalid")`
- **处理**：默认使用 "info"，记录警告到日志
- **用户反馈**：在UE5日志中输出警告信息

### 2. 缺失status字段（旧数据）
- **场景**：解析旧格式的TRACE标记（不含status）
- **处理**：从context自动推断status
- **用户反馈**：无（透明处理）

### 3. 空context
- **场景**：调用 `log_auto("")` 或 `log_auto()`
- **处理**：默认status为 "info"
- **用户反馈**：正常记录，显示为信息条目

### 4. 解析失败
- **场景**：TRACE标记格式错误
- **处理**：跳过该行，继续解析其他行
- **用户反馈**：在控制台输出解析错误警告

## 测试策略

### 单元测试

#### trace.py 测试
1. **test_infer_status_success**：测试成功关键词识别
2. **test_infer_status_error**：测试错误关键词识别
3. **test_infer_status_warning**：测试警告关键词识别
4. **test_infer_status_default**：测试默认info状态
5. **test_infer_status_priority**：测试关键词优先级（错误>警告>成功）
6. **test_log_auto_explicit_status**：测试显式status参数
7. **test_log_auto_inferred_status**：测试自动推断status

#### trace_parser.py 测试
1. **test_parse_new_format**：测试新格式解析（含status）
2. **test_parse_old_format**：测试旧格式解析（不含status）
3. **test_parse_invalid_format**：测试错误格式处理

#### result_analyzer.py 测试
1. **test_get_status_icon**：测试状态图标映射
2. **test_print_trace_history_with_status**：测试包含状态的历史显示
3. **test_print_trace_history_backward_compat**：测试向后兼容性

### 属性测试（Property-Based Testing）

使用 Python 的 `hypothesis` 库进行属性测试：

#### 属性 1-4：状态推断测试
```python
from hypothesis import given, strategies as st

@given(st.text())
def test_infer_status_consistency(context):
    """属性1-4：测试状态推断的一致性和优先级"""
    status = infer_status(context)
    assert status in ["success", "warning", "error", "info"]
    
    # 测试优先级规则
    if any(kw in context for kw in ERROR_KEYWORDS):
        assert status == "error"
    elif any(kw in context for kw in WARNING_KEYWORDS):
        assert status == "warning"
    elif any(kw in context for kw in SUCCESS_KEYWORDS):
        assert status == "success"
    else:
        assert status == "info"
```

#### 属性 3：显式状态优先
```python
@given(st.text(), st.sampled_from(["success", "warning", "error", "info"]))
def test_explicit_status_priority(context, explicit_status):
    """属性3：显式status应该优先于推断"""
    # 模拟log_auto调用并检查记录的status
    recorded_status = simulate_log_auto(context, status=explicit_status)
    assert recorded_status == explicit_status
```

#### 属性 6：表格格式一致性
```python
@given(st.lists(st.dictionaries(...), min_size=1, max_size=100))
def test_table_format_consistency(trace_history):
    """属性6：表格每行应该有一致的格式"""
    output = capture_print_trace_history(trace_history)
    lines = output.split('\n')
    
    # 跳过表头和分隔线
    data_lines = [l for l in lines if l and not l.startswith('─')]
    
    # 检查每行的列数一致
    column_counts = [len(line.split()) for line in data_lines]
    assert len(set(column_counts)) == 1  # 所有行列数相同
```

#### 属性 7：向后兼容性
```python
@given(st.lists(st.dictionaries(...)))
def test_backward_compatibility(old_trace_data):
    """属性7：旧数据（无status字段）应该正常显示"""
    # 移除status字段模拟旧数据
    for entry in old_trace_data:
        entry.pop('status', None)
    
    # 应该不崩溃并能推断status
    try:
        output = capture_print_trace_history_from_data(old_trace_data)
        assert output is not None
    except Exception as e:
        pytest.fail(f"Backward compatibility failed: {e}")
```

### 集成测试

1. **test_end_to_end_with_status**：
   - 运行完整的地图生成流程
   - 验证所有trace条目都有status
   - 验证显示的表格包含状态列

2. **test_mixed_old_new_format**：
   - 混合旧格式和新格式的trace数据
   - 验证解析和显示都正常工作

3. **test_real_world_keywords**：
   - 使用实际代码中的context字符串
   - 验证状态推断符合预期

## 实现注意事项

### 1. 性能考虑
- 关键词匹配使用简单的字符串包含检查（`in` 操作符）
- 避免正则表达式以提高性能
- 状态推断在log_auto调用时完成，不在显示时重复计算

### 2. 国际化
- 当前仅支持中文关键词
- 未来可扩展为多语言支持（通过配置文件定义关键词）

### 3. 可扩展性
- 关键词列表定义为常量，易于修改
- 状态类型可以扩展（如添加 "debug" 状态）
- 图标映射可以自定义

### 4. 向后兼容性
- 旧代码无需修改即可工作
- 旧trace数据可以正常显示
- 新功能是增量式的，不破坏现有功能

### 5. 调试支持
- 无效status会记录警告，便于调试
- 解析错误会输出详细信息
- 可以通过环境变量启用详细日志
