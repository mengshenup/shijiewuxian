"""
End-to-end test for status indicator feature
Tests the complete flow: trace -> parse -> display
"""

import sys
import os

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Add Tools/launch_generator to path (go up to MapGenerators, then to Tools)
tools_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'Tools', 'launch_generator'))
sys.path.insert(0, tools_path)

# Mock unreal module
class MockUnreal:
    @staticmethod
    def log(msg):
        print(f"[UE5 LOG] {msg}")
    
    @staticmethod
    def log_warning(msg):
        print(f"[UE5 WARNING] {msg}")

sys.modules['unreal'] = MockUnreal()

# Import modules
from trace import log_auto
from trace_parser import TraceInfo, _parse_trace_marker
from result_analyzer import print_trace_history
import io
from contextlib import redirect_stdout


def test_end_to_end_flow():
    """
    Test complete flow: generate traces -> parse -> display
    """
    print("\n" + "="*60)
    print("End-to-End Test: Complete Status Indicator Flow")
    print("="*60 + "\n")
    
    print("Step 1: Generate TRACE markers with log_auto()...")
    print("-" * 60)
    
    # Capture trace output
    trace_output = io.StringIO()
    with redirect_stdout(trace_output):
        log_auto("LevelManager初始化")
        log_auto("开始准备Level")
        log_auto("资源加载成功: SM_Cube")
        log_auto("资源加载失败: SM_Plane")
        log_auto("警告：可选组件未找到")
        log_auto("地图生成完成")
    
    trace_lines = trace_output.getvalue().split('\n')
    # Filter only TRACE lines without "[UE5 LOG]" prefix (to avoid duplicates)
    trace_lines = [l for l in trace_lines if l and '[TRACE:' in l and '[UE5 LOG]' not in l]
    
    print(f"Generated {len(trace_lines)} TRACE markers")
    
    print("\nStep 2: Parse TRACE markers...")
    print("-" * 60)
    
    # Parse traces
    trace_info = TraceInfo()
    for line in trace_lines:
        _parse_trace_marker(f"LogPython: {line}", trace_info)
    
    print(f"Parsed {len(trace_info.module_history)} trace entries")
    
    # Verify parsing
    assert len(trace_info.module_history) == 6, f"Expected 6 entries, got {len(trace_info.module_history)}"
    
    # Verify statuses were inferred correctly
    expected_statuses = ['success', 'info', 'success', 'error', 'warning', 'success']
    for i, expected_status in enumerate(expected_statuses):
        actual_status = trace_info.module_history[i]['status']
        assert actual_status == expected_status, f"Entry {i}: expected '{expected_status}', got '{actual_status}'"
    
    print("✓ All statuses inferred correctly")
    
    print("\nStep 3: Display execution history with status column...")
    print("-" * 60)
    
    # Display history
    display_output = io.StringIO()
    with redirect_stdout(display_output):
        print_trace_history(trace_info)
    
    output = display_output.getvalue()
    print(output)
    
    # Verify output contains status column
    assert "状态" in output, "Output should contain '状态' column header"
    assert "✅" in output, "Output should contain success icon"
    assert "❌" in output, "Output should contain error icon"
    assert "⚠️" in output, "Output should contain warning icon"
    assert "ℹ️" in output, "Output should contain info icon"
    
    print("\n" + "="*60)
    print("✓ END-TO-END TEST PASSED")
    print("="*60 + "\n")
    
    print("Summary:")
    print("  - TRACE markers generated with status")
    print("  - Status correctly inferred from context")
    print("  - Execution history displayed with status icons")
    print("  - All status types (✅ ⚠️ ❌ ℹ️) working correctly")
    
    return True


def test_backward_compatibility_e2e():
    """
    Test backward compatibility with old TRACE format
    """
    print("\n" + "="*60)
    print("End-to-End Test: Backward Compatibility")
    print("="*60 + "\n")
    
    print("Simulating old TRACE format (without status field)...")
    print("-" * 60)
    
    # Simulate old format traces
    old_format_lines = [
        "LogPython: [TRACE:level_manager:15:100] LevelManager初始化",
        "LogPython: [TRACE:room_builder:30:200] 资源加载成功",
        "LogPython: [TRACE:room_builder:35:300] 错误：加载失败",
    ]
    
    # Parse old format
    trace_info = TraceInfo()
    for line in old_format_lines:
        _parse_trace_marker(line, trace_info)
    
    print(f"Parsed {len(trace_info.module_history)} old format entries")
    
    # Verify statuses were inferred
    assert len(trace_info.module_history) == 3
    assert trace_info.module_history[0]['status'] == 'success'  # "初始化"
    assert trace_info.module_history[1]['status'] == 'success'  # "成功"
    assert trace_info.module_history[2]['status'] == 'error'    # "错误"
    
    print("✓ Old format parsed and statuses inferred correctly")
    
    # Display
    display_output = io.StringIO()
    with redirect_stdout(display_output):
        print_trace_history(trace_info)
    
    output = display_output.getvalue()
    print("\nDisplayed output:")
    print(output)
    
    assert "✅" in output
    assert "❌" in output
    
    print("\n" + "="*60)
    print("✓ BACKWARD COMPATIBILITY TEST PASSED")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success1 = test_end_to_end_flow()
        success2 = test_backward_compatibility_e2e()
        
        if success1 and success2:
            print("\n" + "="*60)
            print("✓✓✓ ALL END-TO-END TESTS PASSED ✓✓✓")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
