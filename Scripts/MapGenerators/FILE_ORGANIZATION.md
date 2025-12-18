# 文件组织规范

## 目录结构

```
Scripts/MapGenerators/
├── Maps/                                   # 所有地图文件夹
│   ├── cosmos_002_training_world/          # 地图1
│   │   ├── generate.py                     # ⭐ 主生成脚本
│   │   ├── README.md                       # 地图说明
│   │   ├── BUG_FIXES.md                    # BUG修复记录
│   │   ├── DEBUGGING_SUMMARY.md            # 调试总结
│   │   ├── QUICK_FIX_GUIDE.md              # 快速指南
│   │   ├── ROOM_STRUCTURE_VISUALIZATION.md # 结构可视化
│   │   ├── FINAL_SUMMARY.md                # 最终总结
│   │   ├── last_run.log                    # 最后一次运行日志
│   │   └── Debug/                          # 调试工具
│   │       └── verify/
│   │           ├── verify_structure.py     # 验证脚本
│   │           └── notes.txt
│   └── another_map/                        # 地图2
│       ├── generate.py
│       └── README.md
├── Tools/                                  # 共享工具（未来）
│   ├── run_generator.py                    # 通用启动器
│   └── common_utils.py                     # 共享工具函数
├── Debug/                                  # 全局调试文件
│   ├── ddc-workaround/
│   ├── remote-execution/
│   └── ...
├── launch_generator.py                     # ⭐ 主启动脚本
├── generate_map.bat                        # ⭐ 批处理启动器
├── README.md                               # 总体说明
├── STATUS.md                               # 项目状态
└── FILE_ORGANIZATION.md                    # 本文件
```

## 命名规范

### 地图文件夹
- **格式**: 小写字母 + 下划线
- **示例**: `cosmos_002_training_world`, `aim_trainer_basic`, `parkour_course_01`
- **规则**: 
  - 只使用小写字母、数字和下划线
  - 不使用空格或特殊字符
  - 使用描述性名称

### UE5地图文件
- **格式**: 首字母大写 + 下划线
- **示例**: `Cosmos_002_Training_World.umap`
- **转换**: `cosmos_002_training_world` → `Cosmos_002_Training_World`

### Python脚本
- **主脚本**: 统一命名为 `generate.py`
- **验证脚本**: `verify_structure.py`, `verify_lighting.py` 等
- **工具脚本**: 描述性名称，例如 `common_utils.py`

### 文档文件
- **README**: 地图概述和快速开始
- **BUG_FIXES**: BUG修复记录
- **DEBUGGING_SUMMARY**: 技术细节和调试过程
- **QUICK_FIX_GUIDE**: 快速测试和验证指南
- **ROOM_STRUCTURE_VISUALIZATION**: 结构可视化（如适用）
- **FINAL_SUMMARY**: 完整总结

## 使用方法

### 生成地图

**方法1: 使用批处理（推荐）**
```bash
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```

**方法2: 直接使用Python**
```bash
cd Scripts\MapGenerators
python launch_generator.py cosmos_002_training_world
```

**方法3: 使用默认地图**
```bash
cd Scripts\MapGenerators
generate_map.bat
# 默认生成 cosmos_002_training_world
```

### 添加新地图

1. **创建地图文件夹**
   ```bash
   mkdir Scripts\MapGenerators\Maps\my_new_map
   ```

2. **创建generate.py**
   - 复制现有地图的 `generate.py` 作为模板
   - 修改地图名称和生成逻辑

3. **创建README.md**
   ```markdown
   # My New Map
   
   ## 地图概述
   ...
   
   ## 组件清单
   ...
   ```

4. **生成地图**
   ```bash
   generate_map.bat my_new_map
   ```

## 文件职责

### 主启动脚本
- **launch_generator.py**: 
  - 接受地图名称参数
  - 构建UE5命令行
  - 监控输出和超时
  - 自动重试机制
  - 生成压缩日志

### 地图生成脚本
- **Maps/[map_name]/generate.py**:
  - 定义地图名称
  - 创建地图几何体
  - 放置Actor
  - 配置照明
  - 设置GameMode
  - 保存地图

### 验证脚本
- **Maps/[map_name]/Debug/verify/verify_structure.py**:
  - 检查地图文件是否存在
  - 验证所有Actor是否正确生成
  - 检查Actor位置和属性
  - 输出验证报告

## 日志文件

### 位置
- **地图专属日志**: `Maps/[map_name]/last_run.log`
- **全局日志**: 不保存（使用地图专属日志）

### 内容
- 压缩摘要（关键事件和错误）
- 不包含完整输出（节省空间）
- 每次运行覆盖

## 调试文件

### 地图专属调试
- **位置**: `Maps/[map_name]/Debug/`
- **内容**: 该地图特定的调试工具和测试脚本

### 全局调试
- **位置**: `Debug/`
- **内容**: 通用调试工具、实验性代码、历史测试

## 文档组织

### 地图级文档
放在 `Maps/[map_name]/` 下：
- README.md - 必需
- BUG_FIXES.md - 如有BUG修复
- DEBUGGING_SUMMARY.md - 如有复杂调试
- QUICK_FIX_GUIDE.md - 快速参考
- 其他特定文档

### 项目级文档
放在 `Scripts/MapGenerators/` 下：
- README.md - 总体说明
- FILE_ORGANIZATION.md - 本文件
- STATUS.md - 项目状态

## 迁移指南

### 从旧结构迁移

**旧结构**:
```
Scripts/MapGenerators/
├── generate_cosmos_002_training_world.py
├── BUG_FIXES.md
├── DEBUGGING_SUMMARY.md
└── ...
```

**新结构**:
```
Scripts/MapGenerators/
├── Maps/
│   └── cosmos_002_training_world/
│       ├── generate.py
│       ├── README.md
│       ├── BUG_FIXES.md
│       └── ...
└── launch_generator.py
```

**迁移步骤**:
1. 创建 `Maps/[map_name]/` 文件夹
2. 移动 `generate_*.py` → `Maps/[map_name]/generate.py`
3. 移动相关文档到 `Maps/[map_name]/`
4. 更新 `launch_generator.py` 以支持新路径
5. 测试生成功能

## 优势

### 清晰的组织
- ✅ 每个地图有独立文件夹
- ✅ 文档和代码在一起
- ✅ 调试工具就近放置

### 易于扩展
- ✅ 添加新地图只需创建新文件夹
- ✅ 不影响现有地图
- ✅ 共享工具可复用

### 易于维护
- ✅ 地图相关文件集中管理
- ✅ 日志文件不混乱
- ✅ 清晰的命名规范

## 示例

### 生成 Cosmos 002 Training World
```bash
cd Scripts\MapGenerators
generate_map.bat cosmos_002_training_world
```

### 验证地图结构
在UE5编辑器Python控制台：
```python
import sys
sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators/Maps/cosmos_002_training_world/Debug/verify')
import verify_structure
verify_structure.verify()
```

### 查看日志
```bash
type Scripts\MapGenerators\Maps\cosmos_002_training_world\last_run.log
```

## 总结

新的文件组织结构：
- 📁 按地图分组
- 📝 文档就近放置
- 🔧 调试工具独立
- 🚀 易于扩展和维护
