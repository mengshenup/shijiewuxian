"""
Map Structure Verification Script
验证 Cosmos_002_Training_World 地图结构是否完整

Usage (in UE5 Editor Console):
    import sys
    sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators/Debug/verify-map')
    import verify_map_structure
    verify_map_structure.verify()
"""

import unreal


def verify():
    """验证地图结构"""
    print("\n" + "="*60)
    print("地图结构验证工具")
    print("="*60 + "\n")
    
    # 加载地图
    map_path = "/Game/Maps/Cosmos_002_Training_World"
    editor_level_lib = unreal.EditorLevelLibrary()
    editor_asset_lib = unreal.EditorAssetLibrary()
    
    print("[1/3] 检查地图文件...")
    if not editor_asset_lib.does_asset_exist(map_path):
        print(f"  ❌ 地图文件不存在: {map_path}")
        print(f"  请先运行 generate_map.bat 生成地图")
        return False
    print(f"  ✅ 地图文件存在: {map_path}")
    
    # 加载地图
    print(f"\n[2/3] 加载地图...")
    success = editor_level_lib.load_level(map_path)
    if not success:
        print(f"  ❌ 无法加载地图")
        return False
    print(f"  ✅ 地图加载成功")
    
    # 获取所有Actor
    print(f"\n[3/3] 验证房间结构...")
    all_actors = editor_level_lib.get_all_level_actors()
    
    # 期望的Actor列表
    expected_actors = {
        # 房间几何体
        "Floor": "地板",
        "Ceiling": "天花板",
        "FrontWall": "前墙",
        "BackWall": "后墙",
        "LeftOuterWall": "左外墙",
        "RightOuterWall": "右外墙",
        "LeftPartition": "左透明隔板",
        "RightPartition": "右透明隔板",
        # 玩家出生点
        "PlayerStart_Center": "玩家出生点",
        # 照明
        "DirectionalLight_Sun": "太阳光",
        "SkyLight_Ambient": "环境光",
        "PointLight_Left": "左房间灯",
        "PointLight_Center": "中间房间灯",
        "PointLight_Right": "右房间灯",
    }
    
    # 查找Actor
    found_actors = {}
    for actor in all_actors:
        if actor is None:
            continue
        label = actor.get_actor_label()
        if label in expected_actors:
            found_actors[label] = actor
    
    # 报告结果
    print(f"\n{'='*60}")
    print("验证结果")
    print(f"{'='*60}\n")
    
    all_found = True
    
    # 房间几何体
    print("【房间几何体】")
    geometry_actors = [
        "Floor", "Ceiling", "FrontWall", "BackWall",
        "LeftOuterWall", "RightOuterWall", "LeftPartition", "RightPartition"
    ]
    for actor_name in geometry_actors:
        if actor_name in found_actors:
            actor = found_actors[actor_name]
            location = actor.get_actor_location()
            print(f"  ✅ {expected_actors[actor_name]:12s} ({actor_name})")
            print(f"     位置: ({location.x:.1f}, {location.y:.1f}, {location.z:.1f})")
            
            # 检查透明隔板的材质
            if "Partition" in actor_name:
                mesh_comp = actor.static_mesh_component
                if mesh_comp:
                    material = mesh_comp.get_material(0)
                    if material:
                        mat_name = material.get_name()
                        if "Dynamic" in mat_name or "Instance" in mat_name:
                            print(f"     材质: {mat_name} ✅ (动态透明材质)")
                        else:
                            print(f"     材质: {mat_name} ⚠️ (可能不是透明材质)")
        else:
            print(f"  ❌ {expected_actors[actor_name]:12s} ({actor_name}) - 未找到")
            all_found = False
    
    # 玩家出生点
    print(f"\n【玩家出生点】")
    if "PlayerStart_Center" in found_actors:
        actor = found_actors["PlayerStart_Center"]
        location = actor.get_actor_location()
        print(f"  ✅ {expected_actors['PlayerStart_Center']}")
        print(f"     位置: ({location.x:.1f}, {location.y:.1f}, {location.z:.1f})")
        if abs(location.x) < 10 and abs(location.y) < 10 and abs(location.z - 100) < 10:
            print(f"     ✅ 位置正确（中间房间，地板上方100cm）")
        else:
            print(f"     ⚠️ 位置可能不正确（期望: 0, 0, 100）")
    else:
        print(f"  ❌ {expected_actors['PlayerStart_Center']} - 未找到")
        all_found = False
    
    # 照明系统
    print(f"\n【照明系统】")
    lighting_actors = [
        "DirectionalLight_Sun", "SkyLight_Ambient",
        "PointLight_Left", "PointLight_Center", "PointLight_Right"
    ]
    for actor_name in lighting_actors:
        if actor_name in found_actors:
            actor = found_actors[actor_name]
            location = actor.get_actor_location()
            print(f"  ✅ {expected_actors[actor_name]:12s} ({actor_name})")
            print(f"     位置: ({location.x:.1f}, {location.y:.1f}, {location.z:.1f})")
        else:
            print(f"  ❌ {expected_actors[actor_name]:12s} ({actor_name}) - 未找到")
            all_found = False
    
    # 总结
    print(f"\n{'='*60}")
    if all_found:
        print("✅ 所有组件都已正确生成！")
        print("✅ 房间结构完整：地板、天花板、4个外墙、2个透明隔板")
        print("✅ 玩家出生点已放置")
        print("✅ 照明系统已配置")
        print("\n可以点击 Play 按钮测试游戏功能！")
    else:
        print("❌ 部分组件缺失")
        print("建议重新运行 generate_map.bat 生成地图")
    print(f"{'='*60}\n")
    
    return all_found


if __name__ == "__main__":
    verify()
