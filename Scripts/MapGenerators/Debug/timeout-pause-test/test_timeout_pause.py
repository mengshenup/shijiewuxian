"""
Test timeout pause logic during shader compilation
"""
import sys
import time
sys.path.insert(0, 'Tools')

# Import only the OutputMonitor class directly
import importlib.util
import os
# Go up two levels from Debug/timeout-pause-test to Scripts/MapGenerators
script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
monitor_path = os.path.join(script_dir, "Tools/launch_generator/output_monitor.py")
spec = importlib.util.spec_from_file_location("output_monitor", monitor_path)
output_monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(output_monitor)

OutputMonitor = output_monitor.OutputMonitor

def test_timeout_pause():
    """Test that timeout is paused during shader compilation"""
    m = OutputMonitor()
    
    print("测试1: 初始状态")
    print(f"  is_compiling={m.is_compiling}, timeout_paused={m.timeout_paused}, has_output={m.has_output}")
    print(f"  silence_duration={m.get_silence_duration()}")
    assert m.is_compiling == False
    assert m.timeout_paused == False
    assert m.has_output == False
    assert m.get_silence_duration() == 0
    print("  ✓ 通过\n")
    
    print("测试2: 添加普通输出")
    m.add_line("LogTemp: 普通日志")
    print(f"  is_compiling={m.is_compiling}, timeout_paused={m.timeout_paused}, has_output={m.has_output}")
    time.sleep(0.1)
    silence = m.get_silence_duration()
    print(f"  silence_duration={silence:.2f}")
    assert m.is_compiling == False
    assert m.timeout_paused == False
    assert m.has_output == True
    assert silence > 0  # Should have some silence
    print("  ✓ 通过\n")
    
    print("测试3: 添加编译开始")
    m.add_line("LogShaderCompilers: Compiling 1000 shaders")
    print(f"  is_compiling={m.is_compiling}, timeout_paused={m.timeout_paused}")
    silence = m.get_silence_duration()
    print(f"  silence_duration={silence}")
    assert m.is_compiling == True
    assert m.timeout_paused == True
    assert silence == 0  # Should return 0 when paused
    print("  ✓ 通过\n")
    
    print("测试4: 编译期间等待（应该保持暂停）")
    time.sleep(0.2)
    silence = m.get_silence_duration()
    print(f"  silence_duration={silence}")
    assert m.is_compiling == True
    assert m.timeout_paused == True
    assert silence == 0  # Should still return 0
    print("  ✓ 通过\n")
    
    print("测试5: 添加错误日志（不应结束编译）")
    m.add_line("LogWindows: Error: appError called")
    print(f"  is_compiling={m.is_compiling}, timeout_paused={m.timeout_paused}")
    silence = m.get_silence_duration()
    print(f"  silence_duration={silence}")
    assert m.is_compiling == True  # Should still be compiling
    assert m.timeout_paused == True  # Should still be paused
    assert silence == 0  # Should still return 0
    print("  ✓ 通过\n")
    
    print("测试6: 添加编译结束")
    m.add_line("LogPython: Script completed")
    print(f"  is_compiling={m.is_compiling}, timeout_paused={m.timeout_paused}")
    time.sleep(0.1)
    silence = m.get_silence_duration()
    print(f"  silence_duration={silence:.2f}")
    assert m.is_compiling == False
    assert m.timeout_paused == False
    assert silence > 0  # Should have silence again
    print("  ✓ 通过\n")
    
    print("="*60)
    print("所有测试通过！✅")
    print("="*60)

if __name__ == "__main__":
    test_timeout_pause()
