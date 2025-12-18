# Training Map Generator - Design Document

## Overview

本设计文档描述如何使用Python脚本自动生成UE5训练地图。脚本将利用UE5.7.0的Python API创建地图文件，并自动放置所有必要的Actor和配置。

**引擎版本要求：**
- **Unreal Engine 5.7.0**（源码版本）
- Python 3.9+（UE5内置）
- Unreal Python API

**核心目标：**
- 通过Python脚本自动创建地图文件（.umap）
- 自动放置TrainingRoom Actor（3个房间结构）
- 自动配置PlayerStart和照明系统
- 移除GameMode中的动态生成代码
- 实现完全自动化的地图生成流程

**实现方式：**
- 使用UE5的Python API（`unreal`模块）
- 脚本可通过命令行或编辑器执行
- 生成的地图可在编辑器中直接打开和编辑
- 人类可以在生成后调整细节


## Map Layout (From Original Design)

### 3D空间布局

```
俯视图：

┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│  左侧房间     │  玩家房间     │  右侧房间     │
│  (对手房间1)  │  (中间)      │  (对手房间2)  │
│              │              │              │
│              │              │              │
│              │    玩家      │              │
│              │      ↑       │              │
│              │  PlayerStart │              │
│              │              │              │
└──────────────┴──────────────┴──────────────┘
               ↑              ↑
           透明隔板        透明隔板
           X=-300         X=+300
```

### 坐标系统

**房间尺寸：**
- 总宽度：1800 cm (18米) - 3个房间并排
- 总深度：800 cm (8米)
- 总高度：400 cm (4米)

**房间划分：**
- 左侧房间：X = -900 到 -300
- 中间房间：X = -300 到 +300
- 右侧房间：X = +300 到 +900

**关键位置：**
- TrainingRoom Actor位置：(0, 0, 0)
- PlayerStart位置：(0, 0, 100) - 中间房间，地板上方100cm
- 左侧透明墙：X = -300
- 右侧透明墙：X = +300


## Python Script Architecture

### Script Structure

```
Scripts/
└── generate_training_map.py    # 主脚本文件
```

### Core Components

#### 1. MapGenerator Class

主要的地图生成器类：

```python
import unreal

class TrainingMapGenerator:
    """训练地图生成器"""
    
    def __init__(self):
        self.map_name = "Cosmos_002_Training_World"
        self.map_path = "/Game/Maps/"
        self.editor_level_lib = unreal.EditorLevelLibrary()
        self.editor_asset_lib = unreal.EditorAssetLibrary()
        
    def generate_map(self):
        """主生成函数"""
        print(f"开始生成地图: {self.map_name}")
        
        # 1. 创建新关卡
        world = self.create_new_level()
        
        # 2. 放置TrainingRoom
        self.place_training_room(world)
        
        # 3. 放置PlayerStart
        self.place_player_start(world)
        
        # 4. 配置照明
        self.setup_lighting(world)
        
        # 5. 配置GameMode
        self.configure_game_mode(world)
        
        # 6. 保存地图
        self.save_map(world)
        
        print(f"地图生成完成: {self.get_full_map_path()}")
```

#### 2. Level Creation

创建新关卡：

```python
def create_new_level(self):
    """创建新的空白关卡"""
    full_path = self.get_full_map_path()
    
    # 检查地图是否已存在
    if self.editor_asset_lib.does_asset_exist(full_path):
        print(f"警告: 地图已存在 {full_path}")
        # 可以选择删除或跳过
        self.editor_asset_lib.delete_asset(full_path)
        print("已删除旧地图")
    
    # 创建新关卡
    world = self.editor_level_lib.new_level(full_path)
    
    if world is None:
        raise Exception(f"无法创建关卡: {full_path}")
    
    print(f"成功创建关卡: {full_path}")
    return world

def get_full_map_path(self):
    """获取完整地图路径"""
    return f"{self.map_path}{self.map_name}"
```

#### 3. TrainingRoom Placement

放置训练房间Actor：

```python
def place_training_room(self, world):
    """放置TrainingRoom Actor"""
    print("放置TrainingRoom Actor...")
    
    # 获取TrainingRoom类
    training_room_class = unreal.load_class(
        None, 
        "/Script/shijiewuxian.TrainingRoom"
    )
    
    if training_room_class is None:
        raise Exception("无法加载TrainingRoom类")
    
    # 生成Actor
    location = unreal.Vector(0.0, 0.0, 0.0)
    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    
    training_room = self.editor_level_lib.spawn_actor_from_class(
        training_room_class,
        location,
        rotation
    )
    
    if training_room is None:
        raise Exception("无法生成TrainingRoom Actor")
    
    # 设置Actor标签（便于识别）
    training_room.set_actor_label("TrainingRoom_Main")
    
    print(f"TrainingRoom已放置在: {location}")
    return training_room
```

#### 4. PlayerStart Placement

放置玩家出生点：

```python
def place_player_start(self, world):
    """放置PlayerStart"""
    print("放置PlayerStart...")
    
    # 获取PlayerStart类
    player_start_class = unreal.load_class(
        None,
        "/Script/Engine.PlayerStart"
    )
    
    if player_start_class is None:
        raise Exception("无法加载PlayerStart类")
    
    # 生成PlayerStart
    location = unreal.Vector(0.0, 0.0, 100.0)  # 中间房间，地板上方100cm
    rotation = unreal.Rotator(0.0, 0.0, 0.0)   # 面向+Y方向
    
    player_start = self.editor_level_lib.spawn_actor_from_class(
        player_start_class,
        location,
        rotation
    )
    
    if player_start is None:
        raise Exception("无法生成PlayerStart")
    
    player_start.set_actor_label("PlayerStart_Center")
    
    print(f"PlayerStart已放置在: {location}")
    return player_start
```

#### 5. Lighting Setup

配置照明系统：

```python
def setup_lighting(self, world):
    """配置照明系统"""
    print("配置照明系统...")
    
    # 1. 创建定向光（太阳光）
    self.create_directional_light()
    
    # 2. 创建点光源（每个房间一个）
    self.create_point_light(unreal.Vector(-600.0, 0.0, 350.0), "PointLight_Left")
    self.create_point_light(unreal.Vector(0.0, 0.0, 350.0), "PointLight_Center")
    self.create_point_light(unreal.Vector(600.0, 0.0, 350.0), "PointLight_Right")
    
    print("照明系统配置完成")

def create_directional_light(self):
    """创建定向光"""
    directional_light_class = unreal.load_class(
        None,
        "/Script/Engine.DirectionalLight"
    )
    
    location = unreal.Vector(0.0, 0.0, 0.0)
    rotation = unreal.Rotator(-45.0, 45.0, 0.0)
    
    light = self.editor_level_lib.spawn_actor_from_class(
        directional_light_class,
        location,
        rotation
    )
    
    if light:
        light.set_actor_label("DirectionalLight_Sun")
        
        # 设置光照属性
        light_component = light.get_component_by_class(
            unreal.DirectionalLightComponent
        )
        if light_component:
            light_component.set_intensity(3.0)
            light_component.set_light_color(unreal.LinearColor(1.0, 1.0, 1.0, 1.0))
        
        print(f"定向光已创建: {light.get_actor_label()}")
    
    return light

def create_point_light(self, location, label):
    """创建点光源"""
    point_light_class = unreal.load_class(
        None,
        "/Script/Engine.PointLight"
    )
    
    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    
    light = self.editor_level_lib.spawn_actor_from_class(
        point_light_class,
        location,
        rotation
    )
    
    if light:
        light.set_actor_label(label)
        
        # 设置光照属性
        light_component = light.get_component_by_class(
            unreal.PointLightComponent
        )
        if light_component:
            light_component.set_intensity(2000.0)
            light_component.set_attenuation_radius(1000.0)
            light_component.set_light_color(
                unreal.LinearColor(1.0, 0.95, 0.9, 1.0)  # 暖白色
            )
        
        print(f"点光源已创建: {label} at {location}")
    
    return light
```

#### 6. GameMode Configuration

配置地图的GameMode：

```python
def configure_game_mode(self, world):
    """配置地图的GameMode"""
    print("配置GameMode...")
    
    # 获取World Settings
    world_settings = world.get_world_settings()
    
    if world_settings is None:
        print("警告: 无法获取World Settings")
        return
    
    # 加载FPSTrainingGameMode类
    game_mode_class = unreal.load_class(
        None,
        "/Script/shijiewuxian.FPSTrainingGameMode"
    )
    
    if game_mode_class is None:
        print("警告: 无法加载FPSTrainingGameMode类")
        return
    
    # 设置GameMode Override
    world_settings.set_editor_property(
        "default_game_mode",
        game_mode_class
    )
    
    print(f"GameMode已设置为: FPSTrainingGameMode")
```

#### 7. Map Saving

保存地图：

```python
def save_map(self, world):
    """保存地图"""
    print("保存地图...")
    
    full_path = self.get_full_map_path()
    
    # 保存当前关卡
    success = unreal.EditorLoadingAndSavingUtils.save_map(
        world,
        full_path
    )
    
    if not success:
        raise Exception(f"无法保存地图: {full_path}")
    
    # 验证文件是否存在
    if self.editor_asset_lib.does_asset_exist(full_path):
        print(f"✓ 地图已成功保存: {full_path}")
    else:
        raise Exception(f"地图保存失败: 文件不存在")
```

#### 8. Main Execution

主执行函数：

```python
def main():
    """主函数"""
    try:
        generator = TrainingMapGenerator()
        generator.generate_map()
        
        print("\n" + "="*60)
        print("地图生成成功！")
        print("="*60)
        print(f"地图名称: {generator.map_name}")
        print(f"地图路径: {generator.get_full_map_path()}")
        print("\n使用方法:")
        print("1. 在Content Browser中导航到 /Game/Maps/")
        print(f"2. 双击打开 {generator.map_name}")
        print("3. 点击Play按钮测试")
        print("="*60)
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()

# 执行脚本
if __name__ == "__main__":
    main()
```


## GameMode Modification

### Remove Dynamic Generation

需要修改 `FPSTrainingGameMode.cpp`，移除动态生成代码：

```cpp
void AFPSTrainingGameMode::BeginPlay()
{
    Super::BeginPlay();
    
    // ===== 注释掉动态生成代码 =====
    // 现在使用Python脚本生成的静态地图
    
    // SpawnTrainingRoom();      // 已移除 - 房间在地图中预先放置
    // SpawnPlayerStartPoint();  // 已移除 - PlayerStart在地图中预先放置
    // SetupLighting();          // 已移除 - 灯光在地图中预先放置
    
    UE_LOG(LogTemp, Display, TEXT("FPSTrainingGameMode initialized (using static map)"));
}
```

**或者添加条件判断：**

```cpp
void AFPSTrainingGameMode::BeginPlay()
{
    Super::BeginPlay();
    
    // 检查地图中是否已有TrainingRoom
    TArray<AActor*> FoundActors;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ATrainingRoom::StaticClass(), FoundActors);
    
    if (FoundActors.Num() == 0)
    {
        // 地图中没有TrainingRoom，使用动态生成
        UE_LOG(LogTemp, Warning, TEXT("No TrainingRoom found in map, spawning dynamically"));
        SpawnTrainingRoom();
        SpawnPlayerStartPoint();
        SetupLighting();
    }
    else
    {
        // 地图中已有TrainingRoom，使用静态布局
        UE_LOG(LogTemp, Display, TEXT("Using pre-placed TrainingRoom from map"));
    }
    
    UE_LOG(LogTemp, Display, TEXT("FPSTrainingGameMode initialized"));
}
```


## Script Execution Methods

### Method 1: Command Line (Recommended for Automation)

```bash
# Windows
"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" ^
  "D:\001xm\shijiewuxian\shijiewuxian.uproject" ^
  -ExecutePythonScript="Scripts/generate_training_map.py" ^
  -stdout -unattended -nopause -nosplash
```

### Method 2: Editor Python Console

1. 打开UE5编辑器
2. 打开 `Window` → `Developer Tools` → `Output Log`
3. 切换到 `Python` 标签
4. 执行：
```python
import sys
sys.path.append('D:/001xm/shijiewuxian/Scripts')
import generate_training_map
generate_training_map.main()
```

### Method 3: Editor Utility Widget (Optional)

创建一个按钮来执行脚本：

```python
# 在Editor Utility Widget中
import unreal

@unreal.uclass()
class MapGeneratorWidget(unreal.EditorUtilityWidget):
    
    @unreal.ufunction(override=True)
    def on_generate_button_clicked(self):
        import generate_training_map
        generate_training_map.main()
```


## Testing Checklist

生成地图后，验证以下内容：

### 地图文件
- [ ] 地图文件存在于 `/Game/Maps/Cosmos_002_Training_World.umap`
- [ ] 地图可以在Content Browser中看到
- [ ] 地图可以双击打开

### TrainingRoom
- [ ] TrainingRoom Actor存在于地图中
- [ ] 位置在 (0, 0, 0)
- [ ] 包含所有组件（地板、天花板、墙壁、隔板）
- [ ] 房间尺寸正确（1800x800x400 cm）

### PlayerStart
- [ ] PlayerStart存在于地图中
- [ ] 位置在 (0, 0, 100)
- [ ] 在中间房间的中心

### 照明
- [ ] 1个定向光存在
- [ ] 3个点光源存在（左、中、右房间各一个）
- [ ] 光照强度和颜色正确
- [ ] 房间有充足的照明

### GameMode
- [ ] World Settings中GameMode设置为FPSTrainingGameMode
- [ ] 点击Play时使用正确的GameMode
- [ ] 玩家在PlayerStart位置生成

### 功能测试
- [ ] 点击Play可以进入游戏
- [ ] 玩家可以移动
- [ ] 玩家不能穿过墙壁和隔板
- [ ] 可以通过透明隔板看到相邻房间


## Error Handling

脚本应处理以下错误情况：

1. **类加载失败**
   - TrainingRoom类不存在
   - 提示：确保C++代码已编译

2. **地图已存在**
   - 提示用户确认是否覆盖
   - 或自动备份旧地图

3. **Actor生成失败**
   - 检查类路径是否正确
   - 检查坐标是否有效

4. **保存失败**
   - 检查磁盘空间
   - 检查文件权限

5. **Python API不可用**
   - 检查UE5是否启用了Python插件
   - 提示：Edit → Plugins → Python Editor Script Plugin


## Next Steps

完成地图生成后的后续工作：

1. **测试地图**
   - 在编辑器中打开地图
   - 验证所有Actor正确放置
   - 测试游戏功能

2. **设置为默认地图**
   - Edit → Project Settings → Maps & Modes
   - 设置 Editor Startup Map 和 Game Default Map

3. **优化和调整**
   - 调整光照参数
   - 添加后处理效果
   - 优化性能

4. **版本控制**
   - 将生成的.umap文件提交到Git
   - 将Python脚本提交到Git
   - 文档化生成流程
