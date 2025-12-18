"""
Training room geometry builder module
"""

import unreal
import sys
from trace import log_auto, log_step, log_checkpoint


class RoomBuilder:
    """Builds training room geometry"""
    
    def __init__(self, editor_asset_subsystem):
        log_auto("RoomBuilder初始化")
        self.editor_asset_subsystem = editor_asset_subsystem
        self.created_actors = []
    
    def build_training_room(self, world):
        """Create training room geometry"""
        log_auto("开始构建训练室")
        log_step(2, 6, "Creating training room geometry...")
        
        # Load assets
        log_auto("加载网格和材质")
        print("  Loading assets...")
        
        cube_mesh = self.editor_asset_subsystem.load_asset("/Game/LevelPrototyping/Meshes/SM_Cube")
        if cube_mesh:
            print("    ✓ Asset loaded: SM_Cube")
            log_auto("资源加载成功: SM_Cube")
        else:
            print("    ✗ Failed to load asset: SM_Cube")
            log_auto("资源加载失败: SM_Cube")
        
        plane_mesh = self.editor_asset_subsystem.load_asset("/Game/LevelPrototyping/Meshes/SM_Plane")
        if plane_mesh:
            print("    ✓ Asset loaded: SM_Plane")
            log_auto("资源加载成功: SM_Plane")
        else:
            print("    ✗ Failed to load asset: SM_Plane")
            log_auto("资源加载失败: SM_Plane")
        
        # Try to load materials - use TopDark for floor, Gray for walls
        floor_material = self.editor_asset_subsystem.load_asset("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark")
        if floor_material:
            print("    ✓ Asset loaded: MI_PrototypeGrid_TopDark (floor)")
            log_auto("资源加载成功: MI_PrototypeGrid_TopDark")
        else:
            print("    ✗ Failed to load asset: MI_PrototypeGrid_TopDark")
            log_auto("资源加载失败: MI_PrototypeGrid_TopDark")
            # Fallback to Gray
            floor_material = self.editor_asset_subsystem.load_asset("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray")
        
        wall_material = self.editor_asset_subsystem.load_asset("/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray")
        if wall_material:
            print("    ✓ Asset loaded: MI_PrototypeGrid_Gray (walls)")
            log_auto("资源加载成功: MI_PrototypeGrid_Gray")
        else:
            print("    ✗ Failed to load asset: MI_PrototypeGrid_Gray")
            log_auto("资源加载失败: MI_PrototypeGrid_Gray")
        
        base_material = self.editor_asset_subsystem.load_asset("/Game/LevelPrototyping/Materials/M_PrototypeGrid")
        if base_material:
            print("    ✓ Asset loaded: M_PrototypeGrid")
            log_auto("资源加载成功: M_PrototypeGrid")
        else:
            print("    ✗ Failed to load asset: M_PrototypeGrid")
            log_auto("资源加载失败: M_PrototypeGrid")
        
        # Verify all assets loaded
        log_auto("验证资源加载")
        if not all([cube_mesh, plane_mesh, floor_material, wall_material, base_material]):
            log_auto("错误：资源加载失败")
            print(f"  ERROR: Failed to load required assets")
            raise Exception("Failed to load required assets")
        
        log_auto("所有资源加载成功")
        
        # Create floor
        log_auto("创建地板")
        self.create_static_mesh("Floor", cube_mesh, floor_material,
                               unreal.Vector(0, 0, 0),
                               unreal.Rotator(0, 0, 0),
                               unreal.Vector(18.0, 8.0, 0.1))
        
        # Create ceiling
        log_auto("创建天花板")
        self.create_transparent_partition("Ceiling", plane_mesh, base_material,
                                         unreal.Vector(0, 0, 400),
                                         unreal.Rotator(0, 0, 0),
                                         unreal.Vector(18.0, 8.0, 1.0))
        
        # Create walls (UE5 coordinate system: X=Forward, Y=Right, Z=Up)
        log_auto("创建墙壁")
        # Front wall (X axis, facing backward)
        self.create_static_mesh("FrontWall", plane_mesh, wall_material,
                               unreal.Vector(900, 0, 200),
                               unreal.Rotator(0, 0, 0),
                               unreal.Vector(8.0, 4.0, 1.0))
        
        # Back wall (X axis, facing forward)
        self.create_static_mesh("BackWall", plane_mesh, wall_material,
                               unreal.Vector(-900, 0, 200),
                               unreal.Rotator(0, 180, 0),
                               unreal.Vector(8.0, 4.0, 1.0))
        
        # Left wall (Y axis, facing right)
        self.create_static_mesh("LeftOuterWall", plane_mesh, wall_material,
                               unreal.Vector(0, -400, 200),
                               unreal.Rotator(0, -90, 0),
                               unreal.Vector(18.0, 4.0, 1.0))
        
        # Right wall (Y axis, facing left)
        self.create_static_mesh("RightOuterWall", plane_mesh, wall_material,
                               unreal.Vector(0, 400, 200),
                               unreal.Rotator(0, 90, 0),
                               unreal.Vector(18.0, 4.0, 1.0))
        
        # Create partitions (Y axis, dividing rooms)
        log_auto("创建透明隔断")
        # Left partition (between left and center rooms)
        self.create_transparent_partition("LeftPartition", plane_mesh, base_material,
                                         unreal.Vector(0, -133, 200),
                                         unreal.Rotator(0, -90, 0),
                                         unreal.Vector(18.0, 4.0, 1.0))
        
        # Right partition (between center and right rooms)
        self.create_transparent_partition("RightPartition", plane_mesh, base_material,
                                         unreal.Vector(0, 133, 200),
                                         unreal.Rotator(0, 90, 0),
                                         unreal.Vector(18.0, 4.0, 1.0))
        
        log_auto("训练室构建完成")
        print(f"  ✓ Training room geometry created (3 rooms with transparent partitions)")
    
    def create_static_mesh(self, name, mesh, material, location, rotation, scale):
        """Create a static mesh actor"""
        log_auto(f"创建静态网格: {name}")
        
        # Load actor class
        actor_class = unreal.load_class(None, "/Script/Engine.StaticMeshActor")
        
        # Spawn actor
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class, location, rotation
        )
        
        if actor:
            log_auto(f"配置{name}")
            actor.set_actor_label(name)
            
            mesh_component = actor.static_mesh_component
            if mesh_component:
                mesh_component.set_static_mesh(mesh)
                mesh_component.set_material(0, material)
                mesh_component.set_relative_scale3d(scale)
                mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
                mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                mesh_component.set_collision_object_type(unreal.CollisionChannel.ECC_WORLD_STATIC)
                mesh_component.set_collision_profile_name("BlockAll")
            
            print(f"    - Created: {name}")
            self.created_actors.append(name)
        
        return actor
    
    def create_transparent_partition(self, name, mesh, base_material, location, rotation, scale):
        """Create a transparent partition"""
        log_auto(f"创建透明隔断: {name}")
        
        # Load actor class
        actor_class = unreal.load_class(None, "/Script/Engine.StaticMeshActor")
        
        # Spawn actor
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class, location, rotation
        )
        
        if actor:
            actor.set_actor_label(name)
            
            mesh_component = actor.static_mesh_component
            if mesh_component:
                mesh_component.set_static_mesh(mesh)
                mesh_component.set_relative_scale3d(scale)
                mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
                mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
                mesh_component.set_collision_object_type(unreal.CollisionChannel.ECC_WORLD_STATIC)
                mesh_component.set_collision_profile_name("BlockAll")
                
                # Apply base material directly (dynamic materials not supported in Python API)
                # The transparent effect needs to be configured in the base material asset itself
                mesh_component.set_material(0, base_material)
                log_auto(f"应用基础材质: {name}")
            
            print(f"    - Created transparent partition: {name}")
            self.created_actors.append(name)
        
        return actor
