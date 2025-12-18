# -*- coding: utf-8 -*-
"""
AST 解析模块
使用 Python AST 解析代码，提取所有函数调用
"""

import ast

class ASTParser:
    """AST 解析器"""
    
    def __init__(self):
        pass
    
    def parse_file(self, source_code, filename):
        """
        解析文件，返回所有函数调用
        
        Returns:
            dict: {func_name: [{'line': line_num, 'content': code_line}, ...]}
        """
        try:
            tree = ast.parse(source_code, filename=filename)
            return self._extract_calls(tree, source_code)
        except SyntaxError as e:
            print(f"⚠️  语法错误: {filename} - {e}")
            return {}
    
    def _extract_calls(self, tree, source_code):
        """从 AST 提取所有函数调用"""
        lines = source_code.splitlines()
        calls = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node.func)
                if func_name:
                    if func_name not in calls:
                        calls[func_name] = []
                    
                    line_num = node.lineno
                    if 1 <= line_num <= len(lines):
                        content = lines[line_num - 1].strip()
                        calls[func_name].append({
                            'line': line_num,
                            'content': content
                        })
        
        return calls
    
    def _get_function_name(self, node):
        """从 AST 节点获取函数名"""
        if isinstance(node, ast.Name):
            # 简单函数调用: func()
            return node.id
        elif isinstance(node, ast.Attribute):
            # 属性调用: obj.func()
            parts = []
            current = node
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return '.'.join(reversed(parts))
        return None
