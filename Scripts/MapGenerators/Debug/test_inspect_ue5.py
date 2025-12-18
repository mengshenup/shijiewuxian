"""
测试 inspect 模块在 UE5.7.0 中的兼容性
"""

import unreal
import inspect


def test_basic_inspect():
    """测试基本的 inspect 功能"""
    unreal.log("="*60)
    unreal.log("测试 1: 基本 inspect 功能")
    unreal.log("="*60)
    
    frame = inspect.currentframe()
    
    unreal.log(f"✓ 当前行号: {frame.f_lineno}")
    unreal.log(f"✓ 当前文件: {frame.f_code.co_filename}")
    unreal.log(f"✓ 当前函数: {frame.f_code.co_name}")
    unreal.log(f"✓ 第一行号: {frame.f_code.co_firstlineno}")


def test_caller_frame():
    """测试获取调用者栈帧"""
    unreal.log("\n" + "="*60)
    unreal.log("测试 2: 获取调用者信息")
    unreal.log("="*60)
    
    frame = inspect.currentframe().f_back
    
    unreal.log(f"✓ 调用者行号: {frame.f_lineno}")
    unreal.log(f"✓ 调用者函数: {frame.f_code.co_name}")


def test_auto_trace():
    """测试自动追踪功能"""
    unreal.log("\n" + "="*60)
    unreal.log("测试 3: 自动追踪功能")
    unreal.log("="*60)
    
    def log_auto(context=""):
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        module_name = filename.split('/')[-1].split('\\')[-1].replace('.py', '')
        line_num = frame.f_lineno
        func_name = frame.f_code.co_name
        
        marker = f"[TRACE:MODULE:{module_name}:FUNC:{func_name}:LINE:{line_num}]"
        if context:
            marker += f" {context}"
        
        unreal.log(marker)
    
    # 测试调用
    log_auto("测试点1")
    log_auto("测试点2")
    log_auto("测试点3")


def test_decorator():
    """测试装饰器功能"""
    unreal.log("\n" + "="*60)
    unreal.log("测试 4: 装饰器功能")
    unreal.log("="*60)
    
    def auto_trace(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            line_num = func.__code__.co_firstlineno
            
            unreal.log(f"[TRACE:ENTER:{func_name}:LINE:{line_num}]")
            result = func(*args, **kwargs)
            unreal.log(f"[TRACE:EXIT:{func_name}:LINE:{line_num}]")
            
            return result
        return wrapper
    
    @auto_trace
    def sample_function():
        unreal.log("  执行函数内容...")
        return "完成"
    
    # 测试调用
    result = sample_function()
    unreal.log(f"✓ 返回值: {result}")


def main():
    """运行所有测试"""
    unreal.log("\n" + "🧪 开始测试 inspect 模块在 UE5.7.0 中的兼容性\n")
    
    try:
        test_basic_inspect()
        test_caller_frame()
        test_auto_trace()
        test_decorator()
        
        unreal.log("\n" + "="*60)
        unreal.log("✅ 所有测试通过！inspect 模块完全兼容 UE5.7.0")
        unreal.log("="*60)
        
        return 0
        
    except Exception as e:
        unreal.log(f"\n❌ 测试失败: {str(e)}")
        import traceback
        unreal.log(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit(main())
