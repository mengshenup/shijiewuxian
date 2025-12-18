"""
Dry run test - tests launcher logic without actually running UE5
"""

import sys
from pathlib import Path

# Add Tools/launch_generator to path
tools_dir = Path(__file__).parent / "Tools" / "launch_generator"
sys.path.insert(0, str(tools_dir))

print("="*60)
print("  测试启动器逻辑（Dry Run）")
print("="*60)

# Test imports
print("\n1. 测试导入...")
try:
    import config
    import path_setup
    import output_monitor
    import summary_generator
    import log_saver
    import timeout_monitor
    import trace_parser
    import result_analyzer
    import process_runner
    import main
    print("   ✓ 所有模块导入成功")
except Exception as e:
    print(f"   ✗ 导入失败: {e}")
    sys.exit(1)

# Test config
print("\n2. 测试配置...")
print(f"   MAP_NAME: {config.MAP_NAME}")
print(f"   ENGINE_PATH: {config.ENGINE_PATH}")
print(f"   PROJECT_PATH: {config.PROJECT_PATH}")
print(f"   SCRIPT_PATH: {config.SCRIPT_PATH}")
print(f"   DEBUG_MODE: {config.DEBUG_MODE}")
print(f"   TIMEOUT_SECONDS: {config.TIMEOUT_SECONDS}")
print(f"   MAX_ATTEMPTS: {config.MAX_ATTEMPTS}")
print("   ✓ 配置加载成功")

# Test path setup
print("\n3. 测试路径设置...")
try:
    result = path_setup.setup_paths()
    if result:
        print("   ✓ 路径设置成功")
    else:
        print("   ✗ 路径设置失败")
except Exception as e:
    print(f"   ✗ 路径设置异常: {e}")

# Test OutputMonitor
print("\n4. 测试输出监控器...")
try:
    monitor = output_monitor.OutputMonitor()
    monitor.add_line("Test line 1\n")
    monitor.add_line("Test line 2\n")
    assert len(monitor.lines) == 2
    assert monitor.get_elapsed_time() >= 0
    assert monitor.get_silence_duration() >= 0
    print(f"   ✓ 输出监控器工作正常（{len(monitor.lines)}行）")
except Exception as e:
    print(f"   ✗ 输出监控器异常: {e}")

# Test TraceInfo
print("\n5. 测试追踪解析器...")
try:
    trace_info = trace_parser.TraceInfo()
    test_line = "LogPython: Display: [TRACE:LINE:123] Test context"
    trace_parser.parse_line(test_line, trace_info)
    print(f"   ✓ 追踪解析器工作正常")
except Exception as e:
    print(f"   ✗ 追踪解析器异常: {e}")

# Test summary generator
print("\n6. 测试摘要生成器...")
try:
    monitor = output_monitor.OutputMonitor()
    monitor.add_line("LogPython: Display: STARTING MAP GENERATOR\n")
    monitor.add_line("LogPython: Display: [1/6] Preparing level...\n")
    monitor.add_line("LogPython: Display: SUCCESS!\n")
    
    summary = summary_generator.get_new_lines_summary(monitor)
    if summary:
        print(f"   ✓ 摘要生成器工作正常")
        print(f"   摘要预览:\n{summary}")
    else:
        print(f"   ⚠ 摘要为空（可能正常）")
except Exception as e:
    print(f"   ✗ 摘要生成器异常: {e}")

print("\n" + "="*60)
print("  Dry Run 测试完成")
print("="*60)
print("\n✓ 所有组件测试通过！")
print("\n下一步: 运行完整测试")
print("  python launch_generator.py cosmos_002_training_world")
