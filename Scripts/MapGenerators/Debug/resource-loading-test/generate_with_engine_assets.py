"""
Map Generator Using Engine Assets
Uses built-in engine assets instead of project assets to avoid loading issues.

Usage:
    Command Line:
        "D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
          "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
          -ExecutePythonScript="Scripts/MapGenerators/Debug/resource-loading-test/generate_with_engine_assets.py" ^
          -stdout -unattended -nopause -nosplash -DDC-ForceMemoryCache
"""

import unreal


class EngineAssetMapGenerator:
    """Map generator using engine built-in assets"""
    
    def __init__(self):
        self.map_name = "Cosmos_002_Training_World"
        self.map_path = "/Game/Maps/"
        self.editor_level_lib = unreal.EditorLevelLibrary()
        self.editor_asset_lib = unreal.EditorAssetLibrary()
    
    def generate_map(self):
        """Main generation function"""
        print(f"\n{'='*60}")
        print(f"Generating map with ENGINE assets: {self.map_name}")
        print(f"{'='*60}\n")
        
        try:
            # 1. Create/load level
            world = self.create_new_level()
            
            # 2. Place simple geometry using engine assets
            self.place_simple_room(world)
            
            # 3. Place PlayerStart
            self.place_player_start(world)
            
            # 4. Setup lighting
            self.setup_lighting(world)
            
            # 5. Configure GameMode
            self.configure_game_mode(world)
            
            # 6. Save map
            self.save_map(world)
            
            print(f"\n{'='*60}")
            print("✓ Map generation completed!")
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"✗ Map generation failed: {str(e)}")
            print(f"{'='*60}")
            import traceback
            traceback.print_exc()
            raise
    
    def create_new_level(self):
        """Create or load level"""
        print("[1/6] Preparing level...")
        
        full_path = f"{self.map_path}{self.map_name}"
        
        # Try to load existing map
        if self.editor_asset_lib.does_asset_exist(full_path):
            print(f"  Loading existing map: {full_path}")
            success = self.editor_level_lib.load_level(full_path)
            if success:
                world = self.editor_level_lib.get_editor_world()
                self.clear_level_actors(world)
                print(f"  ✓ Map loaded and cleared")
            else:
                print(f"  Creating new map")
                world = self.editor_level_lib.new_level(full_path)
        else:
            print(f"  Creating new map: {full_path}")
            world = self.editor_level_lib.new_level(full_path)
        
        if world is None:
            raise Exception(f"Failed to create/load level")
        
        print(f"  ✓ Level ready")
        return world
    
    def clear_level_actors(self, world):
        """Clear all non-essential actors"""
        all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        
        skip_classes = ['WorldSettings', 'DefaultPhysicsVolume', 'LevelBounds', 'NavigationDataChunk']
        
        for actor in all_actors:
            if actor is None:
                continue
            
            class_name = actor.get_class().get_name()
            should_skip = any(skip in class_name for skip in skip_classes)
            
            if not should_skip:
                unreal.EditorLevelLibrary.destroy_actor(actor)
    
    def place_simple_room(self, world):
        """Place simple room geometry using engine cube"""
        print("[2/6] Creating room geometry with engine assets...")
        
        # Try to load engine cube mesh
        cube_paths = [
            "/Engine/BasicShapes/Cube",
            "/Engine/EngineMeshes/Cube",
        ]
        
        cube_mesh = None
        for path in cube_paths:
            if self.editor_asset_lib.does_asset_exist(path):
                cube_mesh = self.editor_asset_lib.load_asset(path)
                if cube_mesh:
                    print(f"  ✓ Loaded cube mesh from: {path}")
                    break
        
        if cube_mesh is None:
            print("  ⚠ No engine cube mesh found, creating empty actors as placeholders")
            self.create_placeholder_room()
            return
        
        # Create floor
        self.create_cube_actor("Floor", cube_mesh,
                              unreal.Vector(0, 0, -50),
                              unreal.Vector(18.0, 8.0, 0.1))
        
        # Create ceiling
        self.create_cube_actor("Ceiling", cube_mesh,
                              unreal.Vector(0, 0, 450),
                              unreal.Vector(18.0, 8.0, 0.1))
        
        # Create walls
        self.create_cube_actor("FrontWall", cube_mesh,
                              unreal.Vector(0, 400, 200),
                              unreal.Vector(18.0, 0.1, 4.0))
        
        self.create_cube_actor("BackWall", cube_mesh,
                              unreal.Vector(0, -400, 200),
                              unreal.Vector(18.0, 0.1, 4.0))
        
        self.create_cube_actor("LeftWall", cube_mesh,
                              unreal.Vector(-900, 0, 200),
                              unreal.Vector(0.1, 8.0, 4.0))
        
        self.create_cube_actor("RightWall", cube_mesh,
                              unreal.Vector(900, 0, 200),
                              unreal.Vector(0.1, 8.0, 4.0))
        
        print(f"  ✓ Room geometry created")
    
    def create_cube_actor(self, name, mesh, location, scale):
        """Create a static mesh actor with cube"""
        actor_class = unreal.load_class(None, "/Script/Engine.StaticMeshActor")
        
        actor = self.editor_level_lib.spawn_actor_from_class(
            actor_class,
            location,
            unreal.Rotator(0, 0, 0)
        )
        
        if actor:
            actor.set_actor_label(name)
            
            mesh_component = actor.static_mesh_component
            if mesh_component:
                mesh_component.set_static_mesh(mesh)
                mesh_component.set_relative_scale3d(scale)
                mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
            
            print(f"    - Created: {name}")
        
        return actor
    
    def create_placeholder_room(self):
        """Create placeholder empty actors if no meshes available"""
        print("  Creating placeholder actors...")
        
        actor_class = unreal.load_class(None, "/Script/Engine.Actor")
        
        placeholders = [
            ("Floor", unreal.Vector(0, 0, 0)),
            ("Ceiling", unreal.Vector(0, 0, 400)),
            ("FrontWall", unreal.Vector(0, 400, 200)),
            ("BackWall", unreal.Vector(0, -400, 200)),
            ("LeftWall", unreal.Vector(-900, 0, 200)),
            ("RightWall", unreal.Vector(900, 0, 200)),
        ]
        
        for name, location in placeholders:
            actor = self.editor_level_lib.spawn_actor_from_class(
                actor_class,
                location,
                unreal.Rotator(0, 0, 0)
            )
            if actor:
                actor.set_actor_label(name)
                print(f"    - Created placeholder: {name}")
    
    def place_player_start(self, world):
        """Place PlayerStart"""
        print("[3/6] Placing PlayerStart...")
        
        player_start_class = unreal.load_class(None, "/Script/Engine.PlayerStart")
        
        if player_start_class is None:
            raise Exception("Failed to load PlayerStart class")
        
        player_start = self.editor_level_lib.spawn_actor_from_class(
            player_start_class,
            unreal.Vector(0.0, 0.0, 100.0),
            unreal.Rotator(0.0, 0.0, 0.0)
        )
        
        if player_start:
            player_start.set_actor_label("PlayerStart_Center")
            print(f"  ✓ PlayerStart placed")
        else:
            raise Exception("Failed to spawn PlayerStart")
        
        return player_start
    
    def setup_lighting(self, world):
        """Setup basic lighting"""
        print("[4/6] Setting up lighting...")
        
        # Create directional light
        dir_light_class = unreal.load_class(None, "/Script/Engine.DirectionalLight")
        if dir_light_class:
            light = self.editor_level_lib.spawn_actor_from_class(
                dir_light_class,
                unreal.Vector(0, 0, 0),
                unreal.Rotator(-45, 45, 0)
            )
            if light:
                light.set_actor_label("DirectionalLight_Sun")
                print(f"  ✓ Directional light created")
        
        # Create sky light
        sky_light_class = unreal.load_class(None, "/Script/Engine.SkyLight")
        if sky_light_class:
            sky_light = self.editor_level_lib.spawn_actor_from_class(
                sky_light_class,
                unreal.Vector(0, 0, 500),
                unreal.Rotator(0, 0, 0)
            )
            if sky_light:
                sky_light.set_actor_label("SkyLight_Ambient")
                print(f"  ✓ Sky light created")
        
        print(f"  ✓ Lighting configured")
    
    def configure_game_mode(self, world):
        """Configure GameMode"""
        print("[5/6] Configuring GameMode...")
        
        world_settings = world.get_world_settings()
        if world_settings is None:
            print("  ⚠ Failed to get World Settings")
            return
        
        game_mode_class = unreal.load_class(None, "/Script/shijiewuxian.FPSTrainingGameMode")
        if game_mode_class is None:
            print("  ⚠ Failed to load FPSTrainingGameMode")
            return
        
        world_settings.set_editor_property("default_game_mode", game_mode_class)
        print(f"  ✓ GameMode configured")
    
    def save_map(self, world):
        """Save map"""
        print("[6/6] Saving map...")
        
        full_path = f"{self.map_path}{self.map_name}"
        
        success = unreal.EditorLoadingAndSavingUtils.save_map(world, full_path)
        
        if not success:
            raise Exception(f"Failed to save map")
        
        if self.editor_asset_lib.does_asset_exist(full_path):
            print(f"  ✓ Map saved: {full_path}")
        else:
            raise Exception("Map save verification failed")


def main():
    """Main function"""
    try:
        generator = EngineAssetMapGenerator()
        generator.generate_map()
        return 0
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
