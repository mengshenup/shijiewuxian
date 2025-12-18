# -*- coding: utf-8 -*-
"""
主入口模块
"""

from .config import find_generate_dir
from .analyzer import TraceCoverageAnalyzer

def main():
    """主函数"""
    # 查找 generate 目录
    generate_dir = find_generate_dir()
    
    if generate_dir is None:
        print("❌ 错误: 找不到 generate 目录")
        print("\n尝试过的路径:")
        from pathlib import Path
        possible_paths = [
            Path(__file__).resolve().parent.parent.parent / "Maps" / "cosmos_002_training_world" / "generate",
            Path("Scripts/MapGenerators/Maps/cosmos_002_training_world/generate"),
            Path("Maps/cosmos_002_training_world/generate"),
        ]
        for p in possible_paths:
            print(f"   - {p.resolve()}")
        return 1
    
    # 创建分析器
    analyzer = TraceCoverageAnalyzer(generate_dir)
    
    # 分析所有文件
    analyzer.analyze_all()
    
    # 打印报告
    analyzer.print_summary()
    analyzer.print_file_table()
    analyzer.print_visualization()
    analyzer.print_detailed_report()
    
    return 0

if __name__ == "__main__":
    exit(main())
