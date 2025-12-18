# -*- coding: utf-8 -*-
"""
主分析器模块
协调各个模块完成分析
"""

from .file_analyzer import FileAnalyzer
from .statistics import Statistics
from .reporter import Reporter
from .detail_reporter import DetailReporter

class TraceCoverageAnalyzer:
    """Trace 覆盖率分析器"""
    
    def __init__(self, generate_dir):
        self.generate_dir = generate_dir
        self.file_analyzer = FileAnalyzer()
        self.statistics = Statistics()
        self.reporter = Reporter()
        self.detail_reporter = DetailReporter()
        
        self.all_results = {}
        self.all_stats = {}
        self.total_stats = None
    
    def analyze_all(self):
        """分析所有文件"""
        print(f"📂 分析目录: {self.generate_dir}\n")
        
        # 分析所有文件
        self.all_results = self.file_analyzer.analyze_directory(self.generate_dir)
        
        # 计算每个文件的统计
        for filename, result in self.all_results.items():
            self.all_stats[filename] = self.statistics.calculate_file_stats(result)
        
        # 计算总体统计
        self.total_stats = self.statistics.calculate_totals(self.all_results)
    
    def print_summary(self):
        """打印总结报告"""
        if not self.total_stats:
            print("❌ 错误: 请先运行 analyze_all()")
            return
        
        self.reporter.print_summary(self.total_stats)
    
    def print_file_table(self):
        """打印文件对比表格"""
        if not self.all_results:
            print("❌ 错误: 请先运行 analyze_all()")
            return
        
        self.reporter.print_file_table(self.all_results, self.all_stats)
    
    def print_detailed_report(self):
        """打印详细报告"""
        if not self.all_results:
            print("❌ 错误: 请先运行 analyze_all()")
            return
        
        self.reporter.print_section("详细分析报告")
        
        for filename in sorted(self.all_results.keys()):
            result = self.all_results[filename]
            stats = self.all_stats[filename]
            
            # 跳过没有输出语句的文件
            if stats['output_count'] == 0 and stats['log_auto_count'] == 0:
                continue
            
            self.detail_reporter.print_file_detail(result, stats)
    
    def print_visualization(self):
        """打印可视化图表"""
        if not self.all_results:
            print("❌ 错误: 请先运行 analyze_all()")
            return
        
        self.reporter.print_section("覆盖率可视化")
        
        for filename in sorted(self.all_results.keys()):
            if filename == 'trace.py':
                continue
            
            stats = self.all_stats[filename]
            if stats['output_count'] == 0:
                continue
            
            coverage = stats['coverage']
            
            # 生成进度条
            bar_length = 50
            filled = int(bar_length * min(coverage, 100) / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"{filename:<30} [{bar}] {coverage:5.1f}%")
        
        print()
