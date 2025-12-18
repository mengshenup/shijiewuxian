"""
Lighting system setup module
"""

import unreal
import sys
from trace import log_auto, log_step, log_checkpoint


class LightingSystem:
    """Manages lighting setup"""
    
    def __init__(self):
        log_auto("LightingSystem初始化")
        self.created_actors = []
    
    def setup_lighting(self, world):
        """Setup complete lighting system"""
        log_auto("开始设置光照系统")
        log_step(4, 6, "Setting up lighting...")
        
        # Create sky sphere (sky background)
        log_auto("创建天空球")
        self.create_sky_sphere()
        
        # Create directional light (sun)
        log_auto("创建方向光")
        self.create_directional_light()
        
        # Create sky light (ambient)
        log_auto("创建天空光")
        self.create_sky_light()
        
        # Create point lights (one per room) - UE5 coords: X=Forward, Y=Right, Z=Up
        log_auto("创建点光源")
        self.create_point_light(unreal.Vector(0.0, -200.0, 350.0), "PointLight_Left")
        self.create_point_light(unreal.Vector(0.0, 0.0, 350.0), "PointLight_Center")
        self.create_point_light(unreal.Vector(0.0, 200.0, 350.0), "PointLight_Right")
        
        # Create post process volume for better visuals
        log_auto("创建后期处理体积")
        self.create_post_process_volume()
        
        log_auto("光照系统设置完成")
        print(f"  ✓ Lighting system configured (sky + sun + ambient + 3 room lights + post process)")
    
    def create_directional_light(self):
        """Create directional light (sun)"""
        directional_light_class = unreal.load_class(None, "/Script/Engine.DirectionalLight")
        
        if directional_light_class is None:
            log_auto("警告：加载DirectionalLight类失败")
            print("  WARNING: Failed to load DirectionalLight class")
            return None
        
        location = unreal.Vector(0.0, 0.0, 1000.0)
        rotation = unreal.Rotator(-45.0, 45.0, 0.0)  # 45度角，更自然的阳光
        
        light = unreal.EditorLevelLibrary.spawn_actor_from_class(
            directional_light_class, location, rotation
        )
        
        if light:
            log_auto("配置方向光")
            light.set_actor_label("DirectionalLight_Sun")
            
            light_component = light.get_component_by_class(unreal.DirectionalLightComponent)
            if light_component:
                light_component.set_intensity(5.0)  # 增加强度到5.0
                light_component.set_light_color(unreal.LinearColor(1.0, 0.95, 0.85, 1.0))
                light_component.set_cast_shadows(True)  # 确保投射阴影
            
            print(f"    - Directional light created: DirectionalLight_Sun (45° angle, intensity 5.0)")
            self.created_actors.append("DirectionalLight_Sun")
        
        return light
    
    def create_sky_light(self):
        """Create sky light for ambient lighting"""
        sky_light_class = unreal.load_class(None, "/Script/Engine.SkyLight")
        
        if sky_light_class is None:
            log_auto("警告：加载SkyLight类失败")
            print("  WARNING: Failed to load SkyLight class")
            return None
        
        location = unreal.Vector(0.0, 0.0, 500.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        
        sky_light = unreal.EditorLevelLibrary.spawn_actor_from_class(
            sky_light_class, location, rotation
        )
        
        if sky_light:
            log_auto("配置天空光")
            sky_light.set_actor_label("SkyLight_Ambient")
            
            light_component = sky_light.get_component_by_class(unreal.SkyLightComponent)
            if light_component:
                light_component.set_intensity(2.0)  # 增加强度到2.0
                light_component.set_light_color(unreal.LinearColor(0.8, 0.9, 1.0, 1.0))  # 淡蓝色天空光
            
            print(f"    - Sky light created: SkyLight_Ambient (intensity 2.0)")
            self.created_actors.append("SkyLight_Ambient")
        
        return sky_light
    
    def create_point_light(self, location, label):
        """Create point light"""
        point_light_class = unreal.load_class(None, "/Script/Engine.PointLight")
        
        if point_light_class is None:
            log_auto(f"警告：加载PointLight类失败 {label}")
            print(f"  WARNING: Failed to load PointLight class")
            return None
        
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        
        light = unreal.EditorLevelLibrary.spawn_actor_from_class(
            point_light_class, location, rotation
        )
        
        if light:
            log_auto(f"配置点光源: {label}")
            light.set_actor_label(label)
            
            light_component = light.get_component_by_class(unreal.PointLightComponent)
            if light_component:
                light_component.set_intensity(5000.0)  # 增加强度到5000.0
                light_component.set_attenuation_radius(1500.0)  # 增加半径到1500.0
                light_component.set_light_color(unreal.LinearColor(1.0, 0.95, 0.9, 1.0))
                light_component.set_cast_shadows(True)  # 确保投射阴影
            
            print(f"    - Point light created: {label} at {location} (intensity 5000.0)")
            self.created_actors.append(label)
        
        return light
    
    def create_sky_sphere(self):
        """Create sky sphere for sky background"""
        # Try to load BP_Sky_Sphere blueprint
        sky_sphere_class = unreal.load_class(None, "/Engine/EngineSky/BP_Sky_Sphere.BP_Sky_Sphere_C")
        
        if sky_sphere_class is None:
            log_auto("警告：加载BP_Sky_Sphere失败，尝试使用StaticMesh")
            print("  WARNING: Failed to load BP_Sky_Sphere, trying StaticMesh approach")
            # Fallback: create a simple sky dome using static mesh
            return self.create_simple_sky_dome()
        
        location = unreal.Vector(0.0, 0.0, 0.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        
        sky_sphere = unreal.EditorLevelLibrary.spawn_actor_from_class(
            sky_sphere_class, location, rotation
        )
        
        if sky_sphere:
            log_auto("配置天空球")
            sky_sphere.set_actor_label("BP_Sky_Sphere")
            
            print(f"    - Sky sphere created: BP_Sky_Sphere")
            self.created_actors.append("BP_Sky_Sphere")
        
        return sky_sphere
    
    def create_simple_sky_dome(self):
        """Create a simple sky dome using static mesh (fallback)"""
        # Load sphere mesh
        sphere_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Sphere")
        
        if sphere_mesh is None:
            log_auto("警告：无法创建天空球")
            print("  WARNING: Cannot create sky dome")
            return None
        
        # Create static mesh actor
        actor_class = unreal.load_class(None, "/Script/Engine.StaticMeshActor")
        location = unreal.Vector(0.0, 0.0, 0.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        
        sky_dome = unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class, location, rotation
        )
        
        if sky_dome:
            sky_dome.set_actor_label("SkyDome")
            
            mesh_component = sky_dome.static_mesh_component
            if mesh_component:
                mesh_component.set_static_mesh(sphere_mesh)
                mesh_component.set_relative_scale3d(unreal.Vector(1000.0, 1000.0, 1000.0))
                mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
                
                # Try to load a sky material
                sky_material = unreal.EditorAssetLibrary.load_asset("/Engine/EngineSky/M_Sky_Panning_Clouds2")
                if sky_material:
                    mesh_component.set_material(0, sky_material)
            
            print(f"    - Sky dome created: SkyDome (fallback)")
            self.created_actors.append("SkyDome")
        
        return sky_dome
    
    def create_post_process_volume(self):
        """Create post process volume for better visuals"""
        ppv_class = unreal.load_class(None, "/Script/Engine.PostProcessVolume")
        
        if ppv_class is None:
            log_auto("警告：加载PostProcessVolume类失败")
            print("  WARNING: Failed to load PostProcessVolume class")
            return None
        
        location = unreal.Vector(0.0, 0.0, 0.0)
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        
        ppv = unreal.EditorLevelLibrary.spawn_actor_from_class(
            ppv_class, location, rotation
        )
        
        if ppv:
            log_auto("配置后期处理体积")
            ppv.set_actor_label("PostProcessVolume_Global")
            
            # Set to unbound (affects entire level)
            ppv.set_editor_property("unbound", True)
            
            print(f"    - Post process volume created: PostProcessVolume_Global")
            self.created_actors.append("PostProcessVolume_Global")
        
        return ppv
