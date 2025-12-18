# -*- coding: utf-8 -*-
"""
统计模块
计算覆盖率统计信息
"""

from .config import TRACE_SYSTEM_CALLS

class Statistics:
    """统计计算器"""
    
    def __init__(self):
        pass
    
    def calculate_totals(self, all_results):
        """
        计算总体统计
        
        Returns:
            dict: {
                'log_auto_total': int,
                'output_total': int,
                'log_auto_by_type': {...},
                'output_by_type': {...},
                'coverage': float
            }
        """
        log_auto_by_type = {}
        output_by_type = {}
        
        # 统计每种类型的调用次数
        for filename, result in all_results.items():
            # log_auto 类型
            for func_name, calls in result['log_auto_types'].items():
                if func_name not in log_auto_by_type:
                    log_auto_by_type[func_name] = 0
                log_auto_by_type[func_name] += len(calls)
            
            # 输出类型
            for func_name, calls in result['output_types'].items():
                if func_name not in output_by_type:
                    output_by_type[func_name] = 0
                output_by_type[func_name] += len(calls)
        
        # 排除 trace.py 的系统调用
        actual_log_auto = self._exclude_system_calls(log_auto_by_type, TRACE_SYSTEM_CALLS)
        actual_output = self._exclude_system_calls(output_by_type, TRACE_SYSTEM_CALLS)
        
        # 计算总数
        log_auto_total = sum(actual_log_auto.values())
        output_total = sum(actual_output.values())
        
        # 计算覆盖率（只用 log_auto，不包括其他 log_ 类型）
        log_auto_only = actual_log_auto.get('log_auto', 0)
        coverage = (log_auto_only / output_total * 100) if output_total > 0 else 0
        
        return {
            'log_auto_total': log_auto_total,
            'output_total': output_total,
            'log_auto_by_type': actual_log_auto,
            'output_by_type': actual_output,
            'log_auto_only': log_auto_only,
            'coverage': coverage
        }
    
    def _exclude_system_calls(self, counts, system_calls):
        """排除系统调用"""
        result = {}
        for func_name, count in counts.items():
            if func_name in system_calls:
                result[func_name] = max(0, count - system_calls[func_name])
            else:
                result[func_name] = count
        return result
    
    def calculate_file_stats(self, file_result):
        """
        计算单个文件的统计
        
        Returns:
            dict: {
                'log_auto_count': int,
                'output_count': int,
                'coverage': float
            }
        """
        log_auto_count = sum(len(calls) for calls in file_result['log_auto_types'].values())
        output_count = sum(len(calls) for calls in file_result['output_types'].values())
        
        coverage = (log_auto_count / output_count * 100) if output_count > 0 else 0
        
        return {
            'log_auto_count': log_auto_count,
            'output_count': output_count,
            'coverage': coverage
        }
