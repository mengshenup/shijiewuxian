# -*- coding: utf-8 -*-
"""
配置模块
"""

import sys
from pathlib import Path

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# 输出语句关键词（用于识别输出语句）
OUTPUT_KEYWORDS = [
    'print(',
    'unreal.log(',
    'logging.debug(',
    'logging.info(',
    'logging.warning(',
    'logging.error(',
    'logging.critical(',
    'sys.stdout.write(',
    'sys.stderr.write(',
    'console.log(',
    'logger.debug(',
    'logger.info(',
    'logger.warning(',
    'logger.error(',
]

# log_auto 类型前缀
LOG_AUTO_PREFIX = 'log_'

# 排除的系统调用（trace.py 中的系统调用）
TRACE_SYSTEM_CALLS = {
    'unreal.log': 3,
    'print': 3,
    'log_auto': 1,
    'log_checkpoint': 1,
    'log_step': 1,
}

# 覆盖率评级
COVERAGE_RATINGS = [
    (90, "优秀 ✓"),
    (75, "良好 ○"),
    (50, "一般 △"),
    (0, "需改进 ✗"),
]

def get_coverage_rating(coverage):
    """获取覆盖率评级"""
    for threshold, rating in COVERAGE_RATINGS:
        if coverage >= threshold:
            return rating
    return "未知"

def find_generate_dir():
    """查找 generate 目录"""
    possible_paths = [
        Path(__file__).resolve().parent.parent.parent / "Maps" / "cosmos_002_training_world" / "generate",
        Path("Scripts/MapGenerators/Maps/cosmos_002_training_world/generate"),
        Path("Maps/cosmos_002_training_world/generate"),
    ]
    
    for p in possible_paths:
        if p.exists():
            return p
    
    return None
