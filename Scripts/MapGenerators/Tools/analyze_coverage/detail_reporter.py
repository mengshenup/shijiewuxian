# -*- coding: utf-8 -*-
"""
详细报告模块
生成每个文件的详细分析报告
"""

from .output_detector import OutputDetector

class DetailReporter:
    """详细报告生成器"""
    
    def __init__(self):
        self.output_detector = OutputDetector()
    
    def print_file_detail(self, result, stats):
        """打印单个文件的详细信息"""
        filename = result['filename']
        
        print("\n" + "=" * 80)
        print(f"📄 文件: {filename}")
        print("=" * 80 + "\n")
        
        # 统计信息
        print("📊 统计:")
        for func_name in sorted(result['output_types'].keys()):
            count = len(result['output_types'][func_name])
            print(f"   {func_name:<20} : {count:3d} 次")
        
        for func_name in sorted(result['log_auto_types'].keys()):
            count = len(result['log_auto_types'][func_name])
            print(f"   {func_name:<20} : {count:3d} 次")
        
        if stats['output_count'] > 0:
            print(f"   {'─' * 30}")
            print(f"   文件覆盖率          : {stats['coverage']:.1f}%")
        print()
        
        # 输出语句详情
        self._print_output_details(result)
        
        # log_auto 详情
        self._print_log_auto_details(result)
    
    def _print_output_details(self, result):
        """打印输出语句详情"""
        for func_name in sorted(result['output_types'].keys()):
            calls = result['output_types'][func_name]
            if not calls:
                continue
            
            print(f"【{func_name}() 调用】({len(calls)} 次)")
            
            # 使用新的3分类方法
            categorized = self.output_detector.categorize_output_calls(calls, func_name)
            
            # 1. 可替换为 log_auto 的
            if categorized['replaceable']:
                print(f"   ✏️  可替换为 log_auto ({len(categorized['replaceable'])} 次):")
                for call in categorized['replaceable'][:5]:
                    print(f"      Line {call['line']:4d}: {call['content'][:55]}")
                    print(f"               建议: {call['suggestion']}")
                if len(categorized['replaceable']) > 5:
                    print(f"      ... 还有 {len(categorized['replaceable']) - 5} 个")
            
            # 2. 应该保留的
            if categorized['keep']:
                print(f"   ✅ 应该保留 ({len(categorized['keep'])} 次):")
                for call in categorized['keep'][:5]:
                    print(f"      Line {call['line']:4d}: {call['content'][:55]}")
                    print(f"               原因: {call['reason']}")
                if len(categorized['keep']) > 5:
                    print(f"      ... 还有 {len(categorized['keep']) - 5} 个")
            
            # 3. 不确定的（需要人工判断）
            if categorized['uncertain']:
                print(f"   ❓ 需要人工判断 ({len(categorized['uncertain'])} 次):")
                for call in categorized['uncertain'][:5]:
                    print(f"      Line {call['line']:4d}: {call['content'][:55]}")
                if len(categorized['uncertain']) > 5:
                    print(f"      ... 还有 {len(categorized['uncertain']) - 5} 个")
            
            print()
    
    def _print_log_auto_details(self, result):
        """打印 log_auto 详情"""
        for func_name in sorted(result['log_auto_types'].keys()):
            calls = result['log_auto_types'][func_name]
            if not calls:
                continue
            
            print(f"【{func_name}() 调用】({len(calls)} 次)")
            for call in calls[:10]:
                print(f"   Line {call['line']:4d}: {call['content'][:65]}")
            if len(calls) > 10:
                print(f"   ... 还有 {len(calls) - 10} 个")
            print()
