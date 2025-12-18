# -*- coding: utf-8 -*-
"""
文件分析模块
分析单个文件的输出语句
"""

from pathlib import Path
from .ast_parser import ASTParser
from .output_detector import OutputDetector

class FileAnalyzer:
    """文件分析器"""
    
    def __init__(self):
        self.ast_parser = ASTParser()
        self.output_detector = OutputDetector()
    
    def analyze_file(self, filepath):
        """
        分析单个文件
        
        Returns:
            dict: {
                'filename': str,
                'total_lines': int,
                'all_calls': {...},
                'log_auto_types': {...},
                'output_types': {...},
                'other_types': {...}
            }
        """
        filename = filepath.name
        
        try:
            # 读取文件
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # 解析 AST
            all_calls = self.ast_parser.parse_file(source_code, str(filepath))
            
            # 检测输出语句
            detected = self.output_detector.detect_all_outputs(all_calls)
            
            return {
                'filename': filename,
                'total_lines': len(source_code.splitlines()),
                'all_calls': all_calls,
                'log_auto_types': detected['log_auto_types'],
                'output_types': detected['output_types'],
                'other_types': detected['other_types']
            }
        
        except Exception as e:
            print(f"❌ 错误: 分析 {filename} 失败: {e}")
            return {
                'filename': filename,
                'total_lines': 0,
                'all_calls': {},
                'log_auto_types': {},
                'output_types': {},
                'other_types': {}
            }
    
    def analyze_directory(self, directory):
        """
        分析目录中的所有 Python 文件
        
        Returns:
            dict: {filename: file_result, ...}
        """
        results = {}
        
        for py_file in Path(directory).glob('*.py'):
            if py_file.name != '__init__.py':
                results[py_file.name] = self.analyze_file(py_file)
        
        return results
