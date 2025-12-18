# UE5 Map Generation Standards

## Project Info
- **Engine**: UE5.7.0 (Source Build at D:\UnrealEngine570)
- **Project**: shijiewuxian
- **Python Plugin**: PythonScriptPlugin (enabled)

## Directory Structure

```
Scripts/MapGenerators/
├── Maps/
│   └── [map_name]/              # 小写+下划线，如 cosmos_002_training_world
│       ├── generate.py          # 主生成脚本
│       ├── README.md            # 地图说明
│       └── Debug/               # 调试工具（可选）
├── launch_generator.py          # 启动器
├── generate_map.bat             # 批处理
└── README.md
```

## Naming Rules

- **Map folder**: 小写+下划线 → `cosmos_002_training_world`
- **UE5 map file**: 首字母大写+下划线 → `Cosmos_002_Training_World.umap`
- **Script name**: 统一使用 `generate.py`

## Script Template

```python
import unreal

class MapGenerator:
    def __init__(self, map_name=None):
        self.map_name = map_name or "Map_Name"
        self.map_path = "/Game/Maps/"
        self.editor_level_lib = unreal.EditorLevelLibrary()
        self.editor_asset_lib = unreal.EditorAssetLibrary()
    
    def generate_map(self):
        world = self.create_new_level()
        self.place_actors(world)
        self.configure_game_mode(world)
        self.save_map(world)
    
    def create_new_level(self):
        full_path = f"{self.map_path}{self.map_name}"
        if self.editor_asset_lib.does_asset_exist(full_path):
            self.editor_level_lib.load_level(full_path)
            world = self.editor_level_lib.get_editor_world()
            self.clear_level_actors(world)
        else:
            world = self.editor_level_lib.new_level(full_path)
        return world
    
    def place_actors(self, world):
        # Implement actor placement
        pass
    
    def save_map(self, world):
        full_path = f"{self.map_path}{self.map_name}"
        unreal.EditorLoadingAndSavingUtils.save_map(world, full_path)

def main():
    generator = MapGenerator()
    generator.generate_map()
    return 0

if __name__ == "__main__":
    exit(main())
```

## Key API Usage

**Load Class**:
```python
class_obj = unreal.load_class(None, "/Script/ProjectName.ClassName")
```

**Spawn Actor**:
```python
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    actor_class, unreal.Vector(x, y, z), unreal.Rotator(p, y, r)
)
```

**Load Asset**:
```python
mesh = unreal.EditorAssetLibrary.load_asset("/Game/Path/To/Asset")
```

**Set Component**:
```python
component = actor.static_mesh_component
component.set_static_mesh(mesh)
component.set_material(0, material)
component.set_relative_scale3d(unreal.Vector(x, y, z))
```

## Execution

**Recommended**:
```bash
cd Scripts\MapGenerators
generate_map.bat [map_name]
```

**Direct**:
```bash
python launch_generator.py [map_name]
```

## C++ Integration

Python-generated maps are static. Remove dynamic spawning in GameMode:

```cpp
void AGameMode::BeginPlay()
{
    Super::BeginPlay();
    // Remove: SpawnTrainingRoom();
    // Remove: SpawnPlayerStartPoint();
    UE_LOG(LogTemp, Display, TEXT("Using static map"));
}
```

## Creating New Map

1. Create folder: `Scripts/MapGenerators/Maps/my_map/`
2. Create `generate.py` (copy from existing map)
3. Create `README.md`
4. Run: `generate_map.bat my_map`

## Reference

- Example: `Scripts/MapGenerators/Maps/cosmos_002_training_world/`
- File org: `Scripts/MapGenerators/FILE_ORGANIZATION.md`
