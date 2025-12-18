"""
Main map generator orchestrator
"""

import unreal
import sys
from trace import log_auto, log_checkpoint
from level_manager import LevelManager
from room_builder import RoomBuilder
from player_spawner import PlayerSpawner
from lighting_system import LightingSystem
from game_mode_config import GameModeConfigurator
from map_saver import MapSaver


class TrainingMapGenerator:
    """Main generator that orchestrates all components"""
    
    def __init__(self, map_name=None):
        log_auto("TrainingMapGenerator初始化")
        
        self.map_name = map_name or "Cosmos_002_Training_World"
        self.map_path = "/Game/Maps/"
        
        log_auto("创建子系统管理器")
        
        # Create managers
        self.level_manager = LevelManager(self.map_name, self.map_path)
        self.room_builder = RoomBuilder(self.level_manager.editor_asset_subsystem)
        self.player_spawner = PlayerSpawner()
        self.lighting_system = LightingSystem()
        self.game_mode_config = GameModeConfigurator()
        self.map_saver = MapSaver(self.map_name, self.level_manager.editor_asset_subsystem)
        
        # Track all created actors
        self.created_actors = []
        
        log_auto("TrainingMapGenerator初始化完成")
    
    def generate_map(self):
        """Main generation function"""
        log_auto("开始生成地图")
        log_checkpoint("START_GENERATION")
        
        unreal.log(f"Starting map generation: {self.map_name}")
        print(f"\n{'='*60}")
        print(f"Starting map generation: {self.map_name}")
        print(f"{'='*60}\n")
        sys.stdout.flush()
        
        try:
            # Step 1: Create/load level
            log_checkpoint("BEFORE_CREATE_LEVEL")
            log_auto("步骤1: 创建/加载Level")
            world = self.level_manager.create_or_load_level()
            log_checkpoint("AFTER_CREATE_LEVEL")
            
            # Step 2: Build training room
            log_checkpoint("BEFORE_BUILD_ROOM")
            log_auto("步骤2: 构建训练室")
            self.room_builder.build_training_room(world)
            self.created_actors.extend(self.room_builder.created_actors)
            log_checkpoint("AFTER_BUILD_ROOM")
            
            # Step 3: Place PlayerStart
            log_checkpoint("BEFORE_PLACE_PLAYER")
            log_auto("步骤3: 放置PlayerStart")
            self.player_spawner.place_player_start(world)
            self.created_actors.extend(self.player_spawner.created_actors)
            log_checkpoint("AFTER_PLACE_PLAYER")
            
            # Step 4: Setup lighting
            log_checkpoint("BEFORE_SETUP_LIGHTING")
            log_auto("步骤4: 设置光照")
            self.lighting_system.setup_lighting(world)
            self.created_actors.extend(self.lighting_system.created_actors)
            log_checkpoint("AFTER_SETUP_LIGHTING")
            
            # Step 5: Configure GameMode
            log_checkpoint("BEFORE_CONFIG_GAMEMODE")
            log_auto("步骤5: 配置GameMode")
            self.game_mode_config.configure_game_mode(world)
            log_checkpoint("AFTER_CONFIG_GAMEMODE")
            
            # Step 6: Save map
            log_checkpoint("BEFORE_SAVE_MAP")
            log_auto("步骤6: 保存地图")
            full_path = self.get_full_map_path()
            self.map_saver.save_map(world, full_path)
            log_checkpoint("AFTER_SAVE_MAP")
            
            # Report statistics
            log_auto("报告统计信息")
            unreal.log("="*60)
            unreal.log("Map generation completed successfully!")
            unreal.log(f"Total actors created: {len(self.created_actors)}")
            for i, actor_name in enumerate(self.created_actors, 1):
                unreal.log(f"  {i}. {actor_name}")
            unreal.log("="*60)
            
            print(f"\n{'='*60}")
            print("Map generation completed successfully!")
            print(f"{'='*60}")
            print(f"Total actors created: {len(self.created_actors)}")
            print(f"Actor list:")
            for i, actor_name in enumerate(self.created_actors, 1):
                print(f"  {i}. {actor_name}")
            print(f"{'='*60}")
            sys.stdout.flush()
            
            log_checkpoint("GENERATION_COMPLETE")
            
        except Exception as e:
            log_auto(f"错误: {str(e)}")
            print(f"\n{'='*60}")
            print(f"ERROR: Map generation failed!")
            print(f"ERROR: {str(e)}")
            print(f"{'='*60}")
            raise
    
    def get_full_map_path(self):
        """Get full map asset path"""
        return f"{self.map_path}{self.map_name}"
