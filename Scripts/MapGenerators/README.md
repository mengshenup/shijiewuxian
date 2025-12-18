# Map Generators

Python脚本自动生成UE5地图，完全自动化，带错误检测和超时控制。

## 快速开始

**双击运行：**
```
generate_map.bat
或
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```

就这么简单！脚本会自动：
- 启动UE5引擎
- 执行Python地图生成脚本
- 监控输出，检测成功或错误
- 3分钟超时保护
- 自动停止并报告结果

**执行时间：** 首次约2-3分钟（需要加载引擎）

## 可用地图

### Cosmos 002 Training World
**路径**: `Maps/cosmos_002_training_world/`
**地图文件**: `Content/Maps/Cosmos_002_Training_World.umap`
**状态**: ✅ 已完成并测试
**组件数**: 14个Actor (8个几何体 + 1个玩家出生点 + 5个光源)

详细信息请查看: `Maps/cosmos_002_training_world/README.md`

### 添加新地图
1. 在 `Maps/` 下创建新文件夹（小写+下划线）
2. 创建 `generate.py` 脚本
3. 创建 `README.md` 文档
4. 运行 `python launch_generator.py [map_name]`

## 工作原理

1. **generate_map.bat** - 简单启动器，调用Python
2. **launch_generator.py** - Python启动器，负责：
   - 启动UE5命令行
   - 实时监控输出
   - 检测成功/错误关键词
   - 超时控制（3分钟）
   - 自动停止进程
3. **run_generator.py** - 包装器，加载主生成脚本
4. **generate_cosmos_002_training_world.py** - 主地图生成逻辑

## 特性

✅ **完全自动化** - 无需人工干预
✅ **错误检测** - 自动检测并报告错误
✅ **超时保护** - 3分钟后自动停止
✅ **实时反馈** - 显示进度和关键信息
✅ **智能过滤** - 忽略Zen服务器警告等噪音

## 故障排除

**问题：** Failed to load TrainingRoom class  
**解决：** 确保C++代码已编译。运行：
```
D:\UnrealEngine570\Engine\Build\BatchFiles\Build.bat shijiewuxianEditor Win64 Development "D:\001xm\shijiewuxian\shijiewuxian.uproject"
```

**问题：** 超时  
**解决：** 首次运行需要加载引擎，可能需要更长时间。检查是否有其他UE5实例在运行。

**问题：** Python not found  
**解决：** 确保Python已安装并在PATH中。

## 📚 文档索引

### 快速参考
- **FINAL_SUMMARY.md** - 📋 完整的调试总结和下一步操作
- **QUICK_FIX_GUIDE.md** - 🚀 快速测试和验证指南
- **ROOM_STRUCTURE_VISUALIZATION.md** - 📐 房间结构详细可视化

### 技术文档
- **BUG_FIXES.md** - 🔧 详细的BUG报告和修复方案
- **DEBUGGING_SUMMARY.md** - 🔍 完整的调试过程和技术细节
- **STATUS.md** - 📊 项目状态和历史记录

### 调试工具
- **Debug/verify-map/** - 地图验证脚本

---

## 技术细节

**引擎：** Unreal Engine 5.7.0 (Source Build)  
**Python插件：** PythonScriptPlugin  
**执行方式：** `-ExecCmds="py script.py"` 命令行自动化

**核心文件：**
- `generate_map.bat` - 启动器（调用Python）
- `launch_generator.py` - Python进程管理器
- `run_generator.py` - 脚本包装器
- `generate_cosmos_002_training_world.py` - 地图生成逻辑 ⭐ 已修复

**开发文档：**
- `Debug/` - 所有测试和实验性代码
- `Tools/` - 辅助工具
- `.kiro/steering/file-organization.md` - 文件组织规范
- `.kiro/steering/python-map-generation.md` - Python地图生成指南
