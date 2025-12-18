#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trace Coverage Analyzer - 主入口
分析 generate 模块中的所有输出语句覆盖率

使用方法:
    python analyze_coverage.py
    或
    py -3 analyze_coverage.py
"""

from analyze_coverage.main import main

if __name__ == "__main__":
    exit(main())
