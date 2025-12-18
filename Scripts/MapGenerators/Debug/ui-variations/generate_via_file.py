"""
Generate map via file-based communication with running editor
Creates a .py file that the editor can execute via "py" console command
"""

import os
import time


def create_execution_script():
    """Create a temporary Python script for editor to execute"""
    
    script_content = """
# Auto-generated map generation script
# Execute this in UE5 Editor Python console with: py "path/to/this/file"

import sys
sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators')

print("="*60)
print("Starting map generation...")
print("="*60)

try:
    import generate_cosmos_002_training_world
    result = generate_cosmos_002_training_world.main()
    
    if result == 0:
        print("\\n" + "="*60)
        print("SUCCESS! Map generated successfully!")
        print("="*60)
    else:
        print("\\n" + "="*60)
        print("FAILED! Check errors above")
        print("="*60)
        
except Exception as e:
    print("\\n" + "="*60)
    print(f"ERROR: {str(e)}")
    print("="*60)
    import traceback
    traceback.print_exc()
"""
    
    # Save to temp location
    temp_file = "Scripts/MapGenerators/_temp_generate_map.py"
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return os.path.abspath(temp_file)


def main():
    print("\n" + "="*60)
    print("Map Generation Helper")
    print("="*60 + "\n")
    
    script_path = create_execution_script()
    
    print(f"✓ Created execution script: {script_path}")
    print("\n" + "-"*60)
    print("INSTRUCTIONS:")
    print("-"*60)
    print("\n在UE5编辑器中执行以下步骤：\n")
    print("1. 按 ` (反引号) 键打开控制台")
    print("   或者: Window → Developer Tools → Output Log → Cmd 标签\n")
    print("2. 输入以下命令并按回车：\n")
    print(f'   py "{script_path}"\n')
    print("3. 等待脚本执行完成\n")
    print("4. 检查 Content/Maps 文件夹中的地图文件\n")
    print("-"*60)
    print("\n或者，在Python控制台中执行：\n")
    print("   import sys")
    print("   sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators')")
    print("   import generate_cosmos_002_training_world")
    print("   generate_cosmos_002_training_world.main()")
    print("\n" + "="*60 + "\n")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
