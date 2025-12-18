"""
Level creation and management module
"""

import unreal
import sys
from trace import log_auto, log_step, log_checkpoint


class LevelManager:
    """Manages level creation and loading"""
    
    def __init__(self, map_name, map_path="/Game/Maps/"):
        log_auto("LevelManager初始化")
        self.map_name = map_name
        self.map_path = map_path
        
        # Get UE5 subsystems
        self.level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        self.unreal_editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        self.editor_asset_subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    
    def create_or_load_level(self):
        """Create new level or load existing one"""
        log_auto("开始准备Level")
        log_step(1, 6, "Preparing level...")
        
        full_path = self.get_full_map_path()
        
        # Check if map exists
        exists = self.editor_asset_subsystem.does_asset_exist(full_path)
        
        if exists:
            log_auto("地图已存在，加载中")
            unreal.log(f"Map exists, loading: {full_path}")
            print(f"  Map exists, loading: {full_path}")
            sys.stdout.flush()
            
            # Load existing map
            success = self.level_editor_subsystem.load_level(full_path)
            
            if not success:
                log_auto("错误：加载地图失败")
                raise Exception(f"Failed to load existing map: {full_path}")
            
            log_auto("获取World引用")
            unreal.log("Getting world reference...")
            print(f"  Getting world reference...")
            sys.stdout.flush()
            
            # Get world reference
            world = self.unreal_editor_subsystem.get_editor_world()
            
            if not world:
                log_auto("错误：获取World失败")
                raise Exception(f"Failed to get world reference: {full_path}")
            
            log_auto("地图加载成功")
            unreal.log("Map loaded, will regenerate actors")
            print(f"  ✓ Map loaded, will regenerate actors")
            sys.stdout.flush()
            
            # Clear old actors before regenerating
            log_auto("清理旧的Actors")
            self.clear_level_actors()
            unreal.log("Old actors cleared")
            print(f"  ✓ Old actors cleared")
            sys.stdout.flush()
        else:
            log_auto("创建新地图")
            unreal.log(f"Creating new map: {full_path}")
            print(f"  Creating new map: {full_path}")
            sys.stdout.flush()
            
            # Create new level
            success = self.level_editor_subsystem.new_level(full_path)
            
            if not success:
                log_auto("错误：创建Level失败")
                raise Exception(f"Failed to create level: {full_path}")
            
            # Get world reference after creating new level
            log_auto("获取新World引用")
            world = self.unreal_editor_subsystem.get_editor_world()
            
            if not world:
                log_auto("错误：获取新World失败")
                raise Exception(f"Failed to get world reference after creating: {full_path}")
        
        log_auto("Level准备完成")
        unreal.log(f"Level ready: {full_path}")
        print(f"  ✓ Level ready: {full_path}")
        sys.stdout.flush()
        
        return world
    
    def get_full_map_path(self):
        """Get full map asset path"""
        return f"{self.map_path}{self.map_name}"
    
    def clear_level_actors(self):
        """Clear all non-essential actors from the level"""
        all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        
        # Skip essential system actors
        skip_classes = ['WorldSettings', 'DefaultPhysicsVolume', 'LevelBounds', 'NavigationDataChunk']
        
        cleared_count = 0
        for actor in all_actors:
            if actor is None:
                continue
            
            class_name = actor.get_class().get_name()
            should_skip = any(skip in class_name for skip in skip_classes)
            
            if not should_skip:
                unreal.EditorLevelLibrary.destroy_actor(actor)
                cleared_count += 1
        
        log_auto(f"已清理 {cleared_count} 个旧Actors")
        unreal.log(f"Cleared {cleared_count} old actors")
        print(f"    Cleared {cleared_count} old actors")
        sys.stdout.flush()
