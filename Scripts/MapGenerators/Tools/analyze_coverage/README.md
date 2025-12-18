# Analyze Coverage - 模块化覆盖率分析工具

## 概述

这是一个完全模块化的 Trace 覆盖率分析工具，用于分析 `generate` 模块中的所有输出语句。

## 特性

✅ **完全自动化** - 使用 Python AST 自动检测所有函数调用  
✅ **模块化设计** - 每个模块约 100 行代码，职责单一  
✅ **美观输出** - 清晰的表格和可视化图表  
✅ **智能分类** - 自动分类 print() 调用（异常处理、用户输出、调试输出）  
✅ **零维护** - 无需预定义模式，自动适应新的输出类型  

## 模块结构

```
analyze_coverage/
├── __init__.py          # 包初始化
├── config.py            # 配置（约 70 行）
├── ast_parser.py        # AST 解析器（约 70 行）
├── output_detector.py   # 输出语句检测器（约 90 行）
├── file_analyzer.py     # 文件分析器（约 80 行）
├── statistics.py        # 统计计算器（约 90 行）
├── reporter.py          # 报告生成器（约 100 行）
├── detail_reporter.py   # 详细报告生成器（约 100 行）
├── analyzer.py          # 主分析器（约 90 行）
├── main.py              # 主入口（约 40 行）
└── README.md            # 本文件
```

## 使用方法

### 方式 1：使用 batch 文件（推荐）
```bash
cd Scripts\MapGenerators
analyze_coverage.bat
```

### 方式 2：直接运行 Python
```bash
cd Scripts\MapGenerators\Tools
py -3 analyze_coverage.py
```

### 方式 3：作为模块导入
```python
from analyze_coverage import TraceCoverageAnalyzer, find_generate_dir

generate_dir = find_generate_dir()
analyzer = TraceCoverageAnalyzer(generate_dir)
analyzer.analyze_all()
analyzer.print_summary()
```

## 输出说明

### 1. 总体统计
- log_auto 类型统计（log_auto, log_checkpoint, log_step）
- 输出语句统计（print, unreal.log）
- 覆盖率分析和评级

### 2. 文件对比表格
- 每个文件的输出语句数量
- log_auto 调用数量
- 覆盖率百分比
- 状态评级

### 3. 覆盖率可视化
- 进度条显示每个文件的覆盖率

### 4. 详细分析报告
- 每个文件的详细统计
- print() 调用分类（异常处理、用户输出、调试输出）
- 所有输出语句的行号和内容

## 模块说明

### config.py
配置模块，包含：
- 控制台编码设置
- 输出关键词列表
- log_auto 类型前缀
- 系统调用排除规则
- 覆盖率评级标准
- 目录查找函数

### ast_parser.py
AST 解析模块，使用 Python 的 `ast` 模块解析代码：
- 解析 Python 源代码
- 提取所有函数调用
- 获取函数名和调用位置

### output_detector.py
输出语句检测模块：
- 检测 log_auto 类型（以 log_ 开头）
- 检测输出语句（print, unreal.log 等）
- 分类 print() 调用（异常、用户、调试）

### file_analyzer.py
文件分析模块：
- 分析单个文件
- 分析整个目录
- 协调 AST 解析和输出检测

### statistics.py
统计计算模块：
- 计算总体统计
- 计算文件级统计
- 排除系统调用
- 计算覆盖率

### reporter.py
报告生成模块：
- 打印总体统计
- 打印文件对比表格
- 打印可视化图表

### detail_reporter.py
详细报告生成模块：
- 打印每个文件的详细信息
- 打印输出语句详情
- 打印 log_auto 详情

### analyzer.py
主分析器模块：
- 协调各个模块
- 提供统一的分析接口
- 管理分析结果

### main.py
主入口模块：
- 查找 generate 目录
- 创建分析器
- 执行分析
- 打印报告

## 设计原则

1. **单一职责** - 每个模块只负责一个功能
2. **低耦合** - 模块之间通过接口交互
3. **高内聚** - 相关功能集中在同一模块
4. **易扩展** - 新增功能只需添加新模块
5. **易测试** - 每个模块可独立测试

## 扩展指南

### 添加新的输出类型检测
编辑 `config.py`，在 `OUTPUT_KEYWORDS` 中添加新的关键词。

### 添加新的报告格式
创建新的 reporter 模块，继承或参考 `reporter.py` 和 `detail_reporter.py`。

### 添加新的统计指标
编辑 `statistics.py`，添加新的计算方法。

### 添加新的分析功能
创建新的模块，在 `analyzer.py` 中集成。

## 注意事项

1. 工具会自动排除 `trace.py` 中的系统调用
2. 覆盖率计算只基于 `log_auto()`，不包括 `log_checkpoint()` 和 `log_step()`
3. print() 调用会自动分类为：异常处理、用户输出、调试输出
4. 工具使用 AST 解析，语法错误的文件会被跳过

## 版本历史

### v2.0.0 (2025-12-18)
- 完全模块化重构
- 每个模块约 100 行代码
- 改进输出格式
- 添加详细文档

### v1.0.0 (2025-12-18)
- 初始版本
- 使用 AST 自动检测
- 基本覆盖率分析
