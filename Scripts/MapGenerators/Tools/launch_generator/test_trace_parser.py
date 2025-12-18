"""
Unit tests for trace_parser.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trace_parser import TraceInfo, _parse_trace_marker, infer_status_from_context


def test_parse_new_format_with_status():
    """
    Test parsing new TRACE format with status field
    Validates: Requirements 5.1
    """
    print("Testing new format parsing (with status)...")
    
    trace_info = TraceInfo()
    
    # Test line with new format: [TRACE:module:line:timestamp:status] context
    test_lines = [
        "LogPython: [TRACE:room_builder:30:2450:success] 资源加载成功",
        "LogPython: [TRACE:level_manager:45:3000:error] 错误：加载失败",
        "LogPython: [TRACE:lighting_system:60:3500:warning] 警告：光源未找到",
        "LogPython: [TRACE:main:10:100:info] 开始处理",
    ]
    
    expected_results = [
        {'module': 'room_builder', 'line': 30, 'timestamp': 2450, 'status': 'success', 'context': '资源加载成功'},
        {'module': 'level_manager', 'line': 45, 'timestamp': 3000, 'status': 'error', 'context': '错误：加载失败'},
        {'module': 'lighting_system', 'line': 60, 'timestamp': 3500, 'status': 'warning', 'context': '警告：光源未找到'},
        {'module': 'main', 'line': 10, 'timestamp': 100, 'status': 'info', 'context': '开始处理'},
    ]
    
    for line, expected in zip(test_lines, expected_results):
        _parse_trace_marker(line, trace_info)
    
    # Verify all entries were parsed
    assert len(trace_info.module_history) == 4, f"Expected 4 entries, got {len(trace_info.module_history)}"
    
    # Verify each entry
    for i, expected in enumerate(expected_results):
        entry = trace_info.module_history[i]
        assert entry['module'] == expected['module'], f"Entry {i}: module mismatch"
        assert entry['line'] == expected['line'], f"Entry {i}: line mismatch"
        assert entry['timestamp'] == expected['timestamp'], f"Entry {i}: timestamp mismatch"
        assert entry['status'] == expected['status'], f"Entry {i}: status mismatch - expected '{expected['status']}', got '{entry['status']}'"
        assert entry['context'] == expected['context'], f"Entry {i}: context mismatch"
    
    print("✓ New format parsing passed")


def test_parse_old_format_without_status():
    """
    Test parsing old TRACE format without status field (backward compatibility)
    Validates: Requirements 5.2
    """
    print("Testing old format parsing (without status, should infer)...")
    
    trace_info = TraceInfo()
    
    # Test lines with old format: [TRACE:module:line:timestamp] context
    test_lines = [
        "LogPython: [TRACE:room_builder:30:2450] 资源加载成功",
        "LogPython: [TRACE:level_manager:45:3000] 错误：加载失败",
        "LogPython: [TRACE:lighting_system:60:3500] 警告：光源未找到",
        "LogPython: [TRACE:main:10:100] 开始处理",
    ]
    
    expected_statuses = ['success', 'error', 'warning', 'info']
    
    for line in test_lines:
        _parse_trace_marker(line, trace_info)
    
    # Verify all entries were parsed
    assert len(trace_info.module_history) == 4, f"Expected 4 entries, got {len(trace_info.module_history)}"
    
    # Verify status was inferred correctly
    for i, expected_status in enumerate(expected_statuses):
        entry = trace_info.module_history[i]
        assert 'status' in entry, f"Entry {i}: missing status field"
        assert entry['status'] == expected_status, f"Entry {i}: expected status '{expected_status}', got '{entry['status']}'"
    
    print("✓ Old format parsing with inference passed")


def test_parse_invalid_format():
    """
    Test handling of invalid TRACE format
    Validates: Requirements 5.5
    """
    print("Testing invalid format handling...")
    
    trace_info = TraceInfo()
    
    # Test lines with invalid formats (should be skipped gracefully)
    invalid_lines = [
        "LogPython: [TRACE:invalid]",  # Too few parts
        "LogPython: [TRACE:module:notanumber:2450:success]",  # Invalid line number
        "LogPython: Some other log message",  # No TRACE marker
        "LogPython: [TRACE:module:30]",  # Too few parts (only 2)
    ]
    
    for line in invalid_lines:
        try:
            _parse_trace_marker(line, trace_info)
        except Exception as e:
            # Should not raise exception, should handle gracefully
            assert False, f"Parser raised exception for invalid line: {e}"
    
    # Should have parsed 0 valid entries
    assert len(trace_info.module_history) == 0, f"Expected 0 entries, got {len(trace_info.module_history)}"
    
    print("✓ Invalid format handling passed")


def test_infer_status_from_context():
    """
    Test status inference from context
    """
    print("Testing status inference from context...")
    
    test_cases = [
        ("资源加载成功", "success"),
        ("错误：无法连接", "error"),
        ("警告：文件未找到", "warning"),
        ("开始处理数据", "info"),
        ("", "info"),  # Empty context
        (None, "info"),  # None context
    ]
    
    for context, expected_status in test_cases:
        status = infer_status_from_context(context)
        assert status == expected_status, f"Failed for '{context}': expected '{expected_status}', got '{status}'"
    
    print("✓ Status inference passed")


def test_mixed_old_and_new_formats():
    """
    Test parsing mixed old and new formats in same log
    """
    print("Testing mixed format parsing...")
    
    trace_info = TraceInfo()
    
    # Mix of old and new formats
    test_lines = [
        "LogPython: [TRACE:module1:10:100:success] 新格式成功",
        "LogPython: [TRACE:module2:20:200] 旧格式成功",
        "LogPython: [TRACE:module3:30:300:error] 新格式错误",
        "LogPython: [TRACE:module4:40:400] 旧格式错误：失败",
    ]
    
    for line in test_lines:
        _parse_trace_marker(line, trace_info)
    
    assert len(trace_info.module_history) == 4, f"Expected 4 entries, got {len(trace_info.module_history)}"
    
    # Verify statuses
    assert trace_info.module_history[0]['status'] == 'success'
    assert trace_info.module_history[1]['status'] == 'success'  # Inferred from "成功"
    assert trace_info.module_history[2]['status'] == 'error'
    assert trace_info.module_history[3]['status'] == 'error'  # Inferred from "错误"
    
    print("✓ Mixed format parsing passed")


def run_all_tests():
    """Run all trace_parser tests"""
    print("\n" + "="*60)
    print("Running trace_parser Unit Tests")
    print("="*60 + "\n")
    
    try:
        test_parse_new_format_with_status()
        test_parse_old_format_without_status()
        test_parse_invalid_format()
        test_infer_status_from_context()
        test_mixed_old_and_new_formats()
        
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


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
