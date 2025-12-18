"""
GameMode configuration module
"""

import unreal
import sys
from trace import log_auto, log_step, log_checkpoint


class GameModeConfigurator:
    """Configures GameMode for the map"""
    
    def __init__(self):
        log_auto("GameModeConfigurator初始化")
    
    def configure_game_mode(self, world):
        """Configure map's GameMode"""
        log_auto("开始配置GameMode")
        log_step(5, 6, "Configuring GameMode...")
        
        # Get World Settings
        log_auto("获取World设置")
        world_settings = world.get_world_settings()
        
        if world_settings is None:
            log_auto("警告：获取World设置失败")
            print("  WARNING: Failed to get World Settings")
            return
        
        # Load FPSTrainingGameMode class
        log_auto("加载FPSTrainingGameMode类")
        game_mode_class = unreal.load_class(
            None,
            "/Script/shijiewuxian.FPSTrainingGameMode"
        )
        
        if game_mode_class is None:
            log_auto("警告：加载FPSTrainingGameMode类失败")
            print("  WARNING: Failed to load FPSTrainingGameMode class")
            return
        
        # Set GameMode Override
        log_auto("设置GameMode覆盖")
        world_settings.set_editor_property("default_game_mode", game_mode_class)
        
        log_auto("GameMode配置完成")
        print(f"  ✓ GameMode set to: FPSTrainingGameMode")
