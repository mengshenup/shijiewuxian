"""
Test actor tracking fix
"""
import sys
import importlib.util

# Load trace_parser module directly
spec = importlib.util.spec_from_file_location(
    "trace_parser",
    "Scripts/MapGenerators/Tools/launch_generator/trace_parser.py"
)
trace_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace_parser)

TraceInfo = trace_parser.TraceInfo
parse_line = trace_parser.parse_line

# Create test trace info
trace_info = TraceInfo()

# Test lines from actual log
test_lines = [
    "[2025.12.18-08.43.46:757][  0]LogPython:     - Created: Floor",
    "[2025.12.18-08.43.46:836][  0]LogPython:     - Created transparent partition: Ceiling",
    "[2025.12.18-08.43.47:638][  0]LogPython:     - Directional light created: DirectionalLight_Sun",
    "[2025.12.18-08.43.47:694][  0]LogPython:     - Sky light created: SkyLight_Ambient",
    "[2025.12.18-08.43.47:751][  0]LogPython:     - Point light created: PointLight_Left",
    "[2025.12.18-08.43.47:386][  0]LogPython:   ✓ PlayerStart placed at <Struct 'Vector'>",
    "[2025.12.18-08.43.48:493][  0]LogPython: Total actors created: 14",
]

print("测试 Actor 追踪...")
print()

for line in test_lines:
    parse_line(line, trace_info)
    
print(f"✅ Actors 创建: {trace_info.actors_created}")
print(f"✅ 预期 Actors: {trace_info.expected_actors}")
print()

if trace_info.actors_created == 6:
    print("✅ 测试通过！正确统计了 6 个 actors")
else:
    print(f"❌ 测试失败！预期 6 个，实际 {trace_info.actors_created} 个")

if trace_info.expected_actors == 14:
    print("✅ 测试通过！正确解析了总数 14")
else:
    print(f"❌ 测试失败！预期 14，实际 {trace_info.expected_actors}")

print()
print("="*60)
print("测试完成！")
print("="*60)
