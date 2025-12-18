# -*- coding: utf-8 -*-
"""
报告生成模块
生成美观的分析报告
"""

from .config import get_coverage_rating
from .output_detector import OutputDetector

class Reporter:
    """报告生成器"""
    
    def __init__(self):
        self.output_detector = OutputDetector()
    
    def print_header(self, title):
        """打印标题"""
        print("\n┌" + "─" * 78 + "┐")
        print(f"│ {title:<76} │")
        print("└" + "─" * 78 + "┘\n")
    
    def print_section(self, title):
        """打印章节标题"""
        print(f"\n┌{'─' * 78}┐")
        print(f"│ {title:<76} │")
        print(f"└{'─' * 78}┘\n")
    
    def print_summary(self, stats):
        """打印总体统计"""
        self.print_header("📊 TRACE 覆盖率分析报告")
        
        # log_auto 类型统计
        print("┌─ 📌 log_auto 类型统计 " + "─" * 53 + "┐")
        for func_name in sorted(stats['log_auto_by_type'].keys()):
            count = stats['log_auto_by_type'][func_name]
            print(f"│  {func_name:<25} : {count:3d} 次" + " " * 43 + "│")
        print(f"│  {'─' * 35}" + " " * 39 + "│")
        print(f"│  {'总计':<25} : {stats['log_auto_total']:3d} 次" + " " * 43 + "│")
        print("└" + "─" * 78 + "┘\n")
        
        # 输出类型统计
        print("┌─ 📌 输出语句统计 " + "─" * 58 + "┐")
        for func_name in sorted(stats['output_by_type'].keys()):
            count = stats['output_by_type'][func_name]
            print(f"│  {func_name:<25} : {count:3d} 次" + " " * 43 + "│")
        print(f"│  {'─' * 35}" + " " * 39 + "│")
        print(f"│  {'总计':<25} : {stats['output_total']:3d} 次" + " " * 43 + "│")
        print("└" + "─" * 78 + "┘\n")
        
        # 覆盖率
        coverage = stats['coverage']
        rating = get_coverage_rating(coverage)
        
        print("┌─ 📈 覆盖率分析 " + "─" * 61 + "┐")
        print(f"│  log_auto() 覆盖率    : {coverage:5.1f}% ({stats['log_auto_only']}/{stats['output_total']})" + " " * (78 - 35 - len(f"{stats['log_auto_only']}/{stats['output_total']}")) + "│")
        print(f"│  非 log_auto() 比例   : {100-coverage:5.1f}% ({stats['output_total']-stats['log_auto_only']}/{stats['output_total']})" + " " * (78 - 35 - len(f"{stats['output_total']-stats['log_auto_only']}/{stats['output_total']}")) + "│")
        print(f"│  评级                 : {rating:<20}" + " " * 33 + "│")
        print("└" + "─" * 78 + "┘\n")
    
    def print_file_table(self, all_results, all_stats):
        """打印文件对比表格"""
        self.print_section("📁 文件对比表格")
        
        # 表头
        print("┌" + "─" * 78 + "┐")
        print(f"│ {'文件名':<28} │ {'输出':<6} │ {'log_auto':<8} │ {'覆盖率':<8} │ {'状态':<10} │")
        print("├" + "─" * 78 + "┤")
        
        # 每个文件
        for filename in sorted(all_results.keys()):
            result = all_results[filename]
            stats = all_stats[filename]
            
            output_count = stats['output_count']
            log_auto_count = stats['log_auto_count']
            coverage = stats['coverage']
            
            # 状态
            if filename == 'trace.py':
                status = "系统文件"
            elif output_count == 0:
                status = "✓ 完美"
            else:
                status = get_coverage_rating(coverage)
            
            coverage_str = f"{coverage:.1f}%" if output_count > 0 else "N/A"
            
            print(f"│ {filename:<28} │ {output_count:>6} │ {log_auto_count:>8} │ {coverage_str:>8} │ {status:<10} │")
        
        print("└" + "─" * 78 + "┘\n")
