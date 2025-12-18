"""
Player start placement module
"""

import unreal
import sys
from trace import log_auto, log_step, log_checkpoint


class PlayerSpawner:
    """Handles PlayerStart placement"""
    
    def __init__(self):
        log_auto("PlayerSpawner初始化")
        self.created_actors = []
    
    def place_player_start(self, world):
        """Place PlayerStart actor"""
        log_auto("开始放置PlayerStart")
        log_step(3, 6, "Placing PlayerStart...")
        
        # Load PlayerStart class
        player_start_class = unreal.load_class(None, "/Script/Engine.PlayerStart")
        
        if player_start_class is None:
            log_auto("错误：加载PlayerStart类失败")
            raise Exception("Failed to load PlayerStart class")
        
        log_auto("PlayerStart类加载成功")
        
        # Define spawn location (back center, facing forward)
        # UE5 coords: X=Forward, Y=Right, Z=Up
        # Place at back (-X), center (Y=0), above floor (Z=90)
        location = unreal.Vector(-800.0, 0.0, 90.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)  # Facing forward (+X)
        
        # Spawn PlayerStart
        player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(
            player_start_class,
            location,
            rotation
        )
        
        if player_start is None:
            log_auto("错误：生成PlayerStart失败")
            raise Exception("Failed to spawn PlayerStart")
        
        log_auto("设置PlayerStart标签")
        player_start.set_actor_label("PlayerStart_Center")
        
        log_auto("PlayerStart放置成功")
        print(f"  ✓ PlayerStart placed at {location}")
        print(f"    Label: PlayerStart_Center")
        self.created_actors.append("PlayerStart_Center")
        
        return player_start
