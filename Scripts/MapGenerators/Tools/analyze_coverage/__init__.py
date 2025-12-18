# -*- coding: utf-8 -*-
"""
Trace Coverage Analyzer - 模块化版本
分析 generate 模块中的所有输出语句覆盖率
"""

from .analyzer import TraceCoverageAnalyzer
from .main import main
from .config import find_generate_dir

__all__ = ['TraceCoverageAnalyzer', 'main', 'find_generate_dir']
