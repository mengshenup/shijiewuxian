"""
Test the level_manager fix
"""
import sys
sys.path.insert(0, 'Maps/cosmos_002_training_world/generate')

# Read the file and check the fix
with open('Scripts/MapGenerators/Maps/cosmos_002_training_world/generate/level_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
print("检查修复...")
print()

# Check if the fix is present
if 'success = self.level_editor_subsystem.new_level(full_path)' in content:
    print("✅ 修复1: new_level() 返回值正确赋值给 success")
else:
    print("❌ 修复1: 未找到")

if 'world = self.unreal_editor_subsystem.get_editor_world()' in content:
    count = content.count('world = self.unreal_editor_subsystem.get_editor_world()')
    print(f"✅ 修复2: get_editor_world() 调用了 {count} 次（应该是2次：加载和创建）")
else:
    print("❌ 修复2: 未找到")

if 'if not world:' in content:
    count = content.count('if not world:')
    print(f"✅ 修复3: World 验证检查了 {count} 次")
else:
    print("❌ 修复3: 未找到")

print()
print("="*60)
print("修复验证完成！")
print("="*60)
