"""
Unit tests for result_analyzer.py status icon mapping
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from result_analyzer import get_status_icon, STATUS_ICONS


def test_get_status_icon_valid_statuses():
    """
    Test get_status_icon for all valid status values
    Validates: Requirements 1.2, 1.3, 1.4, 1.5
    """
    print("Testing status icon mapping for valid statuses...")
    
    # Test all valid statuses
    test_cases = [
        ("success", "✅"),
        ("warning", "⚠️"),
        ("error", "❌"),
        ("info", "ℹ️"),
    ]
    
    for status, expected_icon in test_cases:
        icon = get_status_icon(status)
        assert icon == expected_icon, f"Failed for status '{status}': expected '{expected_icon}', got '{icon}'"
        assert icon != "", f"Icon should not be empty for valid status '{status}'"
    
    print("✓ Valid status icon mapping passed")


def test_get_status_icon_invalid_status():
    """
    Test get_status_icon for invalid status values
    Validates: Requirements 1.2, 1.3, 1.4, 1.5
    """
    print("Testing status icon mapping for invalid statuses...")
    
    # Test invalid statuses (should return default icon)
    invalid_statuses = [
        "invalid",
        "unknown",
        "",
        None,
        123,
    ]
    
    for status in invalid_statuses:
        icon = get_status_icon(status)
        # Should return default info icon
        assert icon == "ℹ️", f"Failed for invalid status '{status}': expected default icon 'ℹ️', got '{icon}'"
    
    print("✓ Invalid status handling passed")


def test_status_icons_completeness():
    """
    Property 5: Status icon mapping completeness
    Validates: Requirements 1.2, 1.3, 1.4, 1.5
    """
    print("Testing STATUS_ICONS dictionary completeness...")
    
    # All valid statuses should be in the dictionary
    required_statuses = ["success", "warning", "error", "info"]
    
    for status in required_statuses:
        assert status in STATUS_ICONS, f"Missing status '{status}' in STATUS_ICONS"
        assert STATUS_ICONS[status] != "", f"Empty icon for status '{status}'"
        assert len(STATUS_ICONS[status]) > 0, f"Icon should not be empty for status '{status}'"
    
    print("✓ STATUS_ICONS completeness passed")


def test_status_icons_uniqueness():
    """
    Test that each status has a unique icon
    """
    print("Testing status icon uniqueness...")
    
    icons = list(STATUS_ICONS.values())
    unique_icons = set(icons)
    
    assert len(icons) == len(unique_icons), "Status icons should be unique"
    
    print("✓ Status icon uniqueness passed")


def run_all_tests():
    """Run all result_analyzer tests"""
    print("\n" + "="*60)
    print("Running result_analyzer Unit Tests")
    print("="*60 + "\n")
    
    try:
        test_get_status_icon_valid_statuses()
        test_get_status_icon_invalid_status()
        test_status_icons_completeness()
        test_status_icons_uniqueness()
        
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


# Additional tests for print_trace_history
from result_analyzer import print_trace_history
from trace_parser import TraceInfo
import io
from contextlib import redirect_stdout


def test_print_trace_history_with_status_column():
    """
    Test that print_trace_history includes status column
    Validates: Requirements 3.1
    """
    print("Testing trace history table with status column...")
    
    # Create mock trace info
    trace_info = TraceInfo()
    trace_info.module_history = [
        {'module': 'test_module', 'line': 10, 'timestamp': 100, 'context': '测试成功', 'status': 'success'},
        {'module': 'test_module', 'line': 20, 'timestamp': 200, 'context': '测试错误', 'status': 'error'},
    ]
    
    # Capture output
    f = io.StringIO()
    with redirect_stdout(f):
        print_trace_history(trace_info)
    
    output = f.getvalue()
    
    # Check that output contains status column header
    assert "状态" in output, "Output should contain '状态' column header"
    
    # Check that output contains status icons
    assert "✅" in output, "Output should contain success icon"
    assert "❌" in output, "Output should contain error icon"
    
    print("✓ Status column in table passed")


def test_print_trace_history_header():
    """
    Test that table header includes "状态" label
    Validates: Requirements 3.5
    """
    print("Testing table header includes '状态' label...")
    
    trace_info = TraceInfo()
    trace_info.module_history = [
        {'module': 'test', 'line': 10, 'timestamp': 100, 'context': '测试', 'status': 'info'},
    ]
    
    f = io.StringIO()
    with redirect_stdout(f):
        print_trace_history(trace_info)
    
    output = f.getvalue()
    lines = output.split('\n')
    
    # Find header line (contains "序号", "模块", etc.)
    header_line = None
    for line in lines:
        if "序号" in line and "模块" in line:
            header_line = line
            break
    
    assert header_line is not None, "Could not find header line"
    assert "状态" in header_line, "Header should contain '状态' label"
    
    print("✓ Table header test passed")


def test_print_trace_history_backward_compatibility():
    """
    Test that old trace data without status field works correctly
    Validates: Requirements 5.4
    """
    print("Testing backward compatibility (old data without status)...")
    
    trace_info = TraceInfo()
    # Old format: no 'status' field
    trace_info.module_history = [
        {'module': 'test', 'line': 10, 'timestamp': 100, 'context': '资源加载成功'},  # Should infer 'success'
        {'module': 'test', 'line': 20, 'timestamp': 200, 'context': '错误：加载失败'},  # Should infer 'error'
    ]
    
    f = io.StringIO()
    with redirect_stdout(f):
        print_trace_history(trace_info)
    
    output = f.getvalue()
    
    # Should not crash and should infer statuses
    assert "✅" in output, "Should infer success status from context"
    assert "❌" in output, "Should infer error status from context"
    
    print("✓ Backward compatibility passed")


def test_print_trace_history_empty():
    """
    Test that empty history is handled gracefully
    """
    print("Testing empty history handling...")
    
    trace_info = TraceInfo()
    trace_info.module_history = []
    
    f = io.StringIO()
    with redirect_stdout(f):
        print_trace_history(trace_info)
    
    output = f.getvalue()
    
    # Should show "(无)" message
    assert "(无)" in output, "Should show '(无)' for empty history"
    
    print("✓ Empty history handling passed")


def run_table_tests():
    """Run all table display tests"""
    print("\n" + "="*60)
    print("Running Table Display Tests")
    print("="*60 + "\n")
    
    try:
        test_print_trace_history_with_status_column()
        test_print_trace_history_header()
        test_print_trace_history_backward_compatibility()
        test_print_trace_history_empty()
        
        print("\n" + "="*60)
        print("✓ ALL TABLE TESTS PASSED")
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


# Update main to run all test suites
if __name__ == "__main__":
    success1 = run_all_tests()
    success2 = run_table_tests()
    sys.exit(0 if (success1 and success2) else 1)
