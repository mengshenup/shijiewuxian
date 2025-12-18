"""
Property-based tests for trace.py status inference
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock unreal module for testing
class MockUnreal:
    @staticmethod
    def log(msg):
        pass
    
    @staticmethod
    def log_warning(msg):
        pass

sys.modules['unreal'] = MockUnreal()

# Now import trace module
from trace import infer_status, ERROR_KEYWORDS, WARNING_KEYWORDS, SUCCESS_KEYWORDS


def test_infer_status_success_keywords():
    """
    Property 1: Status inference consistency for success keywords
    Validates: Requirements 4.1
    """
    print("Testing success keyword inference...")
    
    for keyword in SUCCESS_KEYWORDS:
        context = f"测试{keyword}操作"
        status = infer_status(context)
        assert status == "success", f"Failed for keyword '{keyword}': got '{status}'"
    
    print("✓ Success keyword inference passed")


def test_infer_status_error_keywords():
    """
    Property 1: Status inference consistency for error keywords
    Validates: Requirements 4.3
    """
    print("Testing error keyword inference...")
    
    for keyword in ERROR_KEYWORDS:
        context = f"测试{keyword}操作"
        status = infer_status(context)
        assert status == "error", f"Failed for keyword '{keyword}': got '{status}'"
    
    print("✓ Error keyword inference passed")


def test_infer_status_warning_keywords():
    """
    Property 1: Status inference consistency for warning keywords
    Validates: Requirements 4.2
    """
    print("Testing warning keyword inference...")
    
    for keyword in WARNING_KEYWORDS:
        context = f"测试{keyword}操作"
        status = infer_status(context)
        assert status == "warning", f"Failed for keyword '{keyword}': got '{status}'"
    
    print("✓ Warning keyword inference passed")


def test_infer_status_error_priority():
    """
    Property 2: Error keywords have priority over success keywords
    Validates: Requirements 4.8
    """
    print("Testing error keyword priority...")
    
    # Test cases where both error and success keywords are present
    test_cases = [
        ("资源加载失败", "error"),  # Contains both "失败" (error) and "加载" (neutral)
        ("创建失败", "error"),       # Contains both "失败" (error) and "创建" (success)
        ("保存错误", "error"),       # Contains both "错误" (error) and "保存" (success)
    ]
    
    for context, expected in test_cases:
        status = infer_status(context)
        assert status == expected, f"Failed for '{context}': expected '{expected}', got '{status}'"
    
    print("✓ Error keyword priority passed")


def test_infer_status_default():
    """
    Property 4: Default status inference for no keywords
    Validates: Requirements 4.4
    """
    print("Testing default status inference...")
    
    # Test cases with no special keywords
    test_cases = [
        "开始处理",
        "正在加载",
        "检查状态",
        "获取数据",
        "",  # Empty string
    ]
    
    for context in test_cases:
        status = infer_status(context)
        assert status == "info", f"Failed for '{context}': expected 'info', got '{status}'"
    
    print("✓ Default status inference passed")


def test_infer_status_chinese_support():
    """
    Property 9: Chinese keyword support
    Validates: Requirements 4.6
    """
    print("Testing Chinese keyword support...")
    
    # Test various Chinese contexts
    test_cases = [
        ("资源加载成功", "success"),
        ("地图生成完成", "success"),
        ("错误：无法连接", "error"),
        ("警告：文件未找到", "warning"),
        ("开始初始化系统", "success"),  # Contains "初始化"
    ]
    
    for context, expected in test_cases:
        status = infer_status(context)
        assert status == expected, f"Failed for '{context}': expected '{expected}', got '{status}'"
    
    print("✓ Chinese keyword support passed")


def test_infer_status_edge_cases():
    """
    Additional edge case tests
    """
    print("Testing edge cases...")
    
    # None input
    status = infer_status(None)
    assert status == "info", f"Failed for None: got '{status}'"
    
    # Empty string
    status = infer_status("")
    assert status == "info", f"Failed for empty string: got '{status}'"
    
    # Multiple keywords with priority
    status = infer_status("警告：创建成功但有问题")
    assert status == "warning", f"Failed for mixed keywords: got '{status}'"
    
    status = infer_status("错误：警告信息")
    assert status == "error", f"Failed for error+warning: got '{status}'"
    
    print("✓ Edge cases passed")


def run_all_tests():
    """Run all property tests"""
    print("\n" + "="*60)
    print("Running infer_status Property Tests")
    print("="*60 + "\n")
    
    try:
        test_infer_status_success_keywords()
        test_infer_status_error_keywords()
        test_infer_status_warning_keywords()
        test_infer_status_error_priority()
        test_infer_status_default()
        test_infer_status_chinese_support()
        test_infer_status_edge_cases()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED")
        print("="*60 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# Additional tests for log_auto function
from trace import log_auto, VALID_STATUSES
import re


def test_log_auto_explicit_status_priority():
    """
    Property 3: Explicit status parameter has priority over inferred status
    Validates: Requirements 2.6, 4.5
    """
    print("Testing explicit status priority...")
    
    # Capture output by redirecting stdout
    import io
    from contextlib import redirect_stdout
    
    # Test case: context suggests success, but explicit status is error
    f = io.StringIO()
    with redirect_stdout(f):
        log_auto("资源加载成功", status="error")
    
    output = f.getvalue()
    
    # Check that output contains "error" status, not "success"
    assert ":error]" in output, f"Expected ':error]' in output, got: {output}"
    assert ":success]" not in output, f"Should not contain ':success]', got: {output}"
    
    print("✓ Explicit status priority passed")


def test_log_auto_status_persistence():
    """
    Property 8: Status is persisted in TRACE marker
    Validates: Requirements 2.1, 2.5
    """
    print("Testing status persistence in TRACE marker...")
    
    import io
    from contextlib import redirect_stdout
    
    # Test all valid statuses
    for status in VALID_STATUSES:
        f = io.StringIO()
        with redirect_stdout(f):
            log_auto(f"测试{status}状态", status=status)
        
        output = f.getvalue()
        
        # Check that TRACE marker contains the status
        assert f":{status}]" in output, f"Expected ':{status}]' in output, got: {output}"
        
        # Check format: [TRACE:module:line:timestamp:status] context
        pattern = r'\[TRACE:\w+:\d+:\d+:' + status + r'\]'
        assert re.search(pattern, output), f"TRACE format incorrect for status '{status}': {output}"
    
    print("✓ Status persistence passed")


def test_log_auto_invalid_status_handling():
    """
    Property 10: Invalid status defaults to 'info' with warning
    Validates: Requirements 2.3
    """
    print("Testing invalid status handling...")
    
    import io
    from contextlib import redirect_stdout
    
    # Test invalid status
    f = io.StringIO()
    with redirect_stdout(f):
        log_auto("测试无效状态", status="invalid_status")
    
    output = f.getvalue()
    
    # Should default to 'info'
    assert ":info]" in output, f"Expected ':info]' in output, got: {output}"
    
    # Should contain warning
    assert "WARNING" in output or "Invalid status" in output, f"Expected warning in output, got: {output}"
    
    print("✓ Invalid status handling passed")


def test_log_auto_inferred_status():
    """
    Test that log_auto correctly infers status when not explicitly provided
    Validates: Requirements 2.2
    """
    print("Testing automatic status inference in log_auto...")
    
    import io
    from contextlib import redirect_stdout
    
    test_cases = [
        ("资源加载成功", "success"),
        ("错误：无法连接", "error"),
        ("警告：文件未找到", "warning"),
        ("开始处理数据", "info"),
    ]
    
    for context, expected_status in test_cases:
        f = io.StringIO()
        with redirect_stdout(f):
            log_auto(context)  # No explicit status
        
        output = f.getvalue()
        assert f":{expected_status}]" in output, f"Expected ':{expected_status}]' for '{context}', got: {output}"
    
    print("✓ Automatic status inference passed")


def test_log_auto_trace_format():
    """
    Test that log_auto outputs correct TRACE format with status
    """
    print("Testing TRACE format with status...")
    
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        log_auto("测试格式", status="success")
    
    output = f.getvalue()
    
    # Check format: [TRACE:module:line:timestamp:status] context
    pattern = r'\[TRACE:\w+:\d+:\d+:success\] 测试格式'
    assert re.search(pattern, output), f"TRACE format incorrect: {output}"
    
    print("✓ TRACE format passed")


def run_log_auto_tests():
    """Run all log_auto tests"""
    print("\n" + "="*60)
    print("Running log_auto Property Tests")
    print("="*60 + "\n")
    
    try:
        test_log_auto_explicit_status_priority()
        test_log_auto_status_persistence()
        test_log_auto_invalid_status_handling()
        test_log_auto_inferred_status()
        test_log_auto_trace_format()
        
        print("\n" + "="*60)
        print("✓ ALL LOG_AUTO TESTS PASSED")
        print("="*60 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# Update main to run both test suites
if __name__ == "__main__":
    success1 = run_all_tests()
    success2 = run_log_auto_tests()
    sys.exit(0 if (success1 and success2) else 1)
