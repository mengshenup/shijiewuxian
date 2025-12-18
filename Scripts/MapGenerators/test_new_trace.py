"""
Test new auto-trace system
Tests the new log_auto() function without needing UE5
"""

import sys
from pathlib import Path

# Add generate folder to path
generate_folder = Path(__file__).parent / "Maps/cosmos_002_training_world/generate"
sys.path.insert(0, str(generate_folder))

# Mock unreal module (since we're testing outside UE5)
class MockUnreal:
    @staticmethod
    def log(message):
        print(f"[UNREAL.LOG] {message}")

sys.modules['unreal'] = MockUnreal()

# Now import trace module
from trace import log_auto, log_step, log_checkpoint
import time


def test_log_auto():
    """Test log_auto() function"""
    print("\n" + "="*60)
    print("测试 1: log_auto() 自动追踪")
    print("="*60)
    
    log_auto("测试开始")
    time.sleep(0.01)  # 模拟一些工作
    log_auto("加载资源")
    time.sleep(0.02)
    log_auto("创建对象")
    time.sleep(0.01)
    log_auto("测试完成")
    
    print("✓ log_auto() 测试通过")


def test_log_step():
    """Test log_step() function"""
    print("\n" + "="*60)
    print("测试 2: log_step() 进度追踪")
    print("="*60)
    
    log_step(1, 3, "第一步")
    time.sleep(0.01)
    log_step(2, 3, "第二步")
    time.sleep(0.01)
    log_step(3, 3, "第三步")
    
    print("✓ log_step() 测试通过")


def test_log_checkpoint():
    """Test log_checkpoint() function"""
    print("\n" + "="*60)
    print("测试 3: log_checkpoint() 检查点")
    print("="*60)
    
    log_auto("开始处理")
    time.sleep(0.01)
    log_checkpoint("PROCESSING_START")
    time.sleep(0.02)
    log_auto("处理中")
    time.sleep(0.01)
    log_checkpoint("PROCESSING_COMPLETE")
    
    print("✓ log_checkpoint() 测试通过")


def test_nested_functions():
    """Test nested function calls"""
    print("\n" + "="*60)
    print("测试 4: 嵌套函数调用")
    print("="*60)
    
    def outer_function():
        log_auto("外层函数开始")
        time.sleep(0.01)
        inner_function()
        log_auto("外层函数结束")
    
    def inner_function():
        log_auto("内层函数开始")
        time.sleep(0.01)
        log_auto("内层函数结束")
    
    outer_function()
    
    print("✓ 嵌套函数测试通过")


def main():
    """Run all tests"""
    print("\n🧪 开始测试新的自动追踪系统\n")
    
    try:
        test_log_auto()
        test_log_step()
        test_log_checkpoint()
        test_nested_functions()
        
        print("\n" + "="*60)
        print("✅ 所有测试通过！")
        print("="*60)
        print("\n📝 输出格式说明:")
        print("  [TRACE:模块名:行号:时间戳] 说明")
        print("\n示例:")
        print("  [TRACE:test_new_trace:45:1234] 测试开始")
        print("  ├─ 模块名: test_new_trace")
        print("  ├─ 行号: 45 (自动获取)")
        print("  ├─ 时间戳: 1234ms (从脚本启动开始)")
        print("  └─ 说明: 测试开始")
        print("\n✨ 无需硬编码行号，代码改变后自动更新！")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
