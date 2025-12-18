# -*- coding: utf-8 -*-
"""
输出语句检测模块
检测所有可能的输出语句（不做过滤）
"""

import re
from .config import OUTPUT_KEYWORDS, LOG_AUTO_PREFIX

class OutputDetector:
    """输出语句检测器"""
    
    def __init__(self):
        pass
    
    def detect_all_outputs(self, all_calls):
        """
        检测所有输出语句
        
        Args:
            all_calls: {func_name: [call_info, ...]}
        
        Returns:
            dict: {
                'log_auto_types': {func_name: [call_info, ...]},
                'output_types': {func_name: [call_info, ...]},
                'other_types': {func_name: [call_info, ...]}
            }
        """
        log_auto_types = {}
        output_types = {}
        other_types = {}
        
        for func_name, calls in all_calls.items():
            if self._is_log_auto_type(func_name):
                log_auto_types[func_name] = calls
            elif self._is_output_statement(func_name):
                output_types[func_name] = calls
            else:
                other_types[func_name] = calls
        
        return {
            'log_auto_types': log_auto_types,
            'output_types': output_types,
            'other_types': other_types
        }
    
    def _is_log_auto_type(self, func_name):
        """判断是否是 log_auto 类型（以 log_ 开头）"""
        return func_name.startswith(LOG_AUTO_PREFIX)
    
    def _is_output_statement(self, func_name):
        """判断是否是输出语句"""
        # 特殊处理：明确的输出函数
        if func_name in ['print', 'unreal.log']:
            return True
        
        # 检查是否匹配任何输出关键词（必须完全匹配或以 . 开头）
        for keyword in OUTPUT_KEYWORDS:
            # 移除括号
            keyword_name = keyword.replace('(', '')
            if func_name == keyword_name:
                return True
        
        return False
    
    def categorize_output_calls(self, output_calls, func_name):
        """
        分类输出调用 - 分为3类
        
        Args:
            output_calls: 输出调用列表
            func_name: 函数名（print, unreal.log 等）
        
        Returns:
            dict: {
                'replaceable': [...],    # 可替换为 log_auto（调试输出）
                'keep': [...],           # 应该保留（异常处理、用户输出）
                'uncertain': [...]       # 不确定（需要人工判断）
            }
        """
        replaceable = []
        keep = []
        uncertain = []
        
        for call in output_calls:
            content = call['content']
            content_lower = content.lower()
            
            # 1. 应该保留的（异常处理、用户输出）
            if self._should_keep(content, content_lower):
                keep.append({**call, 'reason': self._get_keep_reason(content, content_lower)})
            
            # 2. 可以替换的（调试输出）
            elif self._can_replace(content, content_lower):
                suggestion = self._generate_replacement_suggestion(call, func_name)
                replaceable.append({**call, 'suggestion': suggestion})
            
            # 3. 不确定的（需要人工判断）
            else:
                uncertain.append({**call, 'reason': '需要人工判断'})
        
        return {
            'replaceable': replaceable,
            'keep': keep,
            'uncertain': uncertain
        }
    
    def _should_keep(self, content, content_lower):
        """判断是否应该保留"""
        # 异常处理关键词
        exception_keywords = ['error', 'warning', 'exception', 'failed', 'traceback']
        if any(kw in content_lower for kw in exception_keywords):
            return True
        
        # 用户输出标记
        user_markers = ['✓', '✗', '○', '△', 'SUCCESS', 'FAILED']
        if any(marker in content for marker in user_markers):
            return True
        
        # 分隔线（用户界面）
        if '=' * 10 in content or '-' * 10 in content:
            return True
        
        # 使用说明
        if any(kw in content_lower for kw in ['how to use', 'usage', 'instructions']):
            return True
        
        return False
    
    def _get_keep_reason(self, content, content_lower):
        """获取保留原因"""
        if any(kw in content_lower for kw in ['error', 'exception', 'traceback']):
            return '异常处理'
        elif any(kw in content_lower for kw in ['warning', 'failed']):
            return '警告信息'
        elif any(marker in content for marker in ['✓', 'SUCCESS']):
            return '成功提示'
        elif '=' * 10 in content or '-' * 10 in content:
            return '界面分隔'
        elif 'how to use' in content_lower:
            return '使用说明'
        else:
            return '用户输出'
    
    def _can_replace(self, content, content_lower):
        """判断是否可以替换为 log_auto"""
        # 调试信息关键词
        debug_keywords = [
            'loading', 'creating', 'setting', 'configuring',
            'starting', 'finishing', 'processing', 'initializing',
            'spawning', 'placing', 'building', 'saving'
        ]
        
        # 如果包含调试关键词，可以替换
        if any(kw in content_lower for kw in debug_keywords):
            return True
        
        # 如果是简单的状态输出，可以替换
        if content_lower.strip().startswith(('step', '步骤', 'phase', '阶段')):
            return True
        
        return False
    
    def _generate_replacement_suggestion(self, call, func_name):
        """生成替换建议"""
        content = call['content']
        line = call['line']
        
        # 提取输出的消息内容
        # 例如: print("Loading mesh...") -> "Loading mesh..."
        # 例如: print(f"Created: {name}") -> f"Created: {name}"
        
        # 简单提取：去掉 print( 和 unreal.log( 前缀
        if func_name == 'print':
            # 提取 print(...) 中的内容
            match = re.search(r'print\((.*)\)', content)
            if match:
                message = match.group(1).strip()
                return f"log_auto({message})"
        elif func_name == 'unreal.log':
            # 提取 unreal.log(...) 中的内容
            match = re.search(r'unreal\.log\((.*)\)', content)
            if match:
                message = match.group(1).strip()
                return f"log_auto({message})"
        
        return f"log_auto(\"...\")"
