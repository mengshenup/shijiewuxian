"""
Test script to verify all modules can be imported correctly
"""

import sys
from pathlib import Path

# Add Tools/launch_generator to path
tools_dir = Path(__file__).parent / "Tools" / "launch_generator"
sys.path.insert(0, str(tools_dir))

print("="*60)
print("  测试模块导入")
print("="*60)

# Test each module
modules = [
    'config',
    'path_setup',
    'output_monitor',
    'summary_generator',
    'log_saver',
    'timeout_monitor',
    'trace_parser',
    'result_analyzer',
    'process_runner',
    'main'
]

failed = []
succeeded = []

for module_name in modules:
    try:
        module = __import__(module_name)
        succeeded.append(module_name)
        print(f"✓ {module_name:20s} - 导入成功")
    except Exception as e:
        failed.append((module_name, str(e)))
        print(f"✗ {module_name:20s} - 导入失败: {e}")

print("\n" + "="*60)
print(f"  测试结果")
print("="*60)
print(f"成功: {len(succeeded)}/{len(modules)}")
print(f"失败: {len(failed)}/{len(modules)}")

if failed:
    print("\n失败的模块:")
    for module_name, error in failed:
        print(f"  - {module_name}: {error}")
    sys.exit(1)
else:
    print("\n✓ 所有模块导入成功！")
    
    # Test config values
    import config
    print("\n配置信息:")
    print(f"  MAP_NAME: {config.MAP_NAME}")
    print(f"  DEBUG_MODE: {config.DEBUG_MODE}")
    print(f"  TIMEOUT_SECONDS: {config.TIMEOUT_SECONDS}")
    print(f"  MAX_ATTEMPTS: {config.MAX_ATTEMPTS}")
    
    sys.exit(0)
