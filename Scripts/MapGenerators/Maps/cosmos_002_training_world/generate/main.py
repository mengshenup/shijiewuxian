"""
Main entry point for map generation
"""

import unreal
import sys
from trace import log_auto, log_checkpoint
from generator import TrainingMapGenerator


def main():
    """Main function - entry point for map generation"""
    log_checkpoint("SCRIPT_START")
    
    # Print start marker
    unreal.log("\n" + "="*60)
    unreal.log("STARTING MAP GENERATOR")
    unreal.log("="*60)
    print("\n" + "="*60)
    print("STARTING MAP GENERATOR")
    print("="*60)
    sys.stdout.flush()
    
    log_auto("创建生成器实例")
    
    try:
        # Create generator
        log_checkpoint("BEFORE_GENERATOR_INIT")
        generator = TrainingMapGenerator()
        log_checkpoint("AFTER_GENERATOR_INIT")
        
        # Generate map
        log_checkpoint("BEFORE_GENERATE_MAP")
        generator.generate_map()
        log_checkpoint("AFTER_GENERATE_MAP")
        
        # Success output
        log_auto("生成成功")
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print(f"Map Name: {generator.map_name}")
        print(f"Map Path: {generator.get_full_map_path()}")
        print("\nHow to use:")
        print("1. Open UE5 Editor")
        print("2. Navigate to Content Browser → Maps folder")
        print(f"3. Double-click to open: {generator.map_name}")
        print("4. Click Play button to test")
        print("="*60 + "\n")
        sys.stdout.flush()
        
        log_checkpoint("SCRIPT_SUCCESS")
        return 0
        
    except Exception as e:
        log_auto(f"错误: {str(e)}")
        log_checkpoint("SCRIPT_ERROR")
        
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        
        return 1


if __name__ == "__main__":
    exit(main())
