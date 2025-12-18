"""
Map saving module
"""

import unreal
import sys
from pathlib import Path
from trace import log_auto, log_step, log_checkpoint


class MapSaver:
    """Handles map saving operations"""
    
    def __init__(self, map_name, editor_asset_subsystem):
        log_auto("MapSaver初始化")
        self.map_name = map_name
        self.editor_asset_subsystem = editor_asset_subsystem
    
    def save_map(self, world, full_path):
        """Save map and show file size comparison"""
        log_auto("开始保存地图")
        log_step(6, 6, "Saving map...")
        
        # Get absolute path to project Content folder
        import os
        project_dir = unreal.SystemLibrary.get_project_directory()
        map_file_path = Path(project_dir) / "Content" / "Maps" / f"{self.map_name}.umap"
        
        # Get old file size before saving
        log_auto("检查现有地图文件")
        old_size = 0
        old_exists = map_file_path.exists()
        if old_exists:
            old_size = map_file_path.stat().st_size
            print(f"  Previous map size: {old_size:,} bytes ({old_size/1024:.2f} KB)")
        
        # Save current level
        log_auto("保存地图文件")
        success = unreal.EditorLoadingAndSavingUtils.save_map(world, full_path)
        
        if not success:
            log_auto("错误：保存地图失败")
            raise Exception(f"Failed to save map: {full_path}")
        
        log_auto("验证地图保存")
        
        # Verify file exists in asset system
        exists = self.editor_asset_subsystem.does_asset_exist(full_path)
        
        if exists:
            log_auto("地图文件验证成功")
            
            # Get new file size from disk
            if map_file_path.exists():
                new_size = map_file_path.stat().st_size
                size_diff = new_size - old_size
                
                log_auto("计算文件大小变化")
                print(f"  ✓ Map saved successfully: {full_path}")
                print(f"  New map size: {new_size:,} bytes ({new_size/1024:.2f} KB)")
                
                if old_size > 0:
                    if size_diff > 0:
                        print(f"  Size change: +{size_diff:,} bytes (+{size_diff/1024:.2f} KB, {(size_diff/old_size)*100:.1f}% larger)")
                    elif size_diff < 0:
                        print(f"  Size change: {size_diff:,} bytes ({size_diff/1024:.2f} KB, {abs(size_diff/old_size)*100:.1f}% smaller)")
                    else:
                        print(f"  Size change: No change")
                
                sys.stdout.flush()
            else:
                # File verified in asset system but not found on disk yet (may be delayed write)
                log_auto("地图在资产系统中验证成功")
                print(f"  ✓ Map saved successfully: {full_path}")
                print(f"  Note: File write may be delayed by UE5 asset system")
                sys.stdout.flush()
        else:
            log_auto("错误：地图保存验证失败")
            raise Exception(f"Map save failed: File does not exist")
