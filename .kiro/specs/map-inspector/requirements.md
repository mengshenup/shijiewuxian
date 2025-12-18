# 需求文档

## 简介

本文档定义了地图检查工具（Map Inspector）的需求，该工具允许开发者分析虚幻引擎5的地图文件（.umap），提取并显示地图中所有Actor和对象的信息。该工具将提供文本输出和高质量ASCII字符3D可视化功能，帮助开发者理解地图结构和内容。

## 术语表

- **地图检查工具（Map Inspector）**: 基于Python的工具，用于读取和分析UE5地图文件
- **UE5地图（UE5 Map）**: 存储在Content目录中的虚幻引擎5关卡文件，扩展名为.umap
- **Actor**: 放置在UE5关卡中的任何对象（例如：静态网格、灯光、相机、自定义Actor）
- **Actor信息（Actor Information）**: Actor的属性，包括类类型、位置、旋转、缩放和组件详情
- **StaticMeshComponent**: UE5组件类型，包含对静态网格资产的引用
- **静态网格（Static Mesh）**: UE5中的3D模型资产，包含顶点、三角形、法线和材质数据
- **网格数据（Mesh Data）**: 静态网格的几何信息，包括顶点位置、三角形索引、法线向量和边界框
- **顶点（Vertex）**: 3D空间中的点，定义网格的形状
- **三角形（Triangle）**: 由三个顶点索引定义的面，是网格的基本渲染单元
- **法线（Normal）**: 垂直于表面的向量，用于光照计算和背面剔除
- **切线（Tangent）**: 沿着表面的向量，与法线垂直，用于法线贴图计算
- **UV坐标（UV Coordinates）**: 2D纹理坐标，将3D顶点映射到2D纹理空间
- **顶点颜色（Vertex Color）**: 存储在顶点上的颜色数据，可用于着色和效果
- **材质属性（Material Properties）**: 材质的物理属性，如基础颜色、粗糙度、金属度、自发光等
- **纹理（Texture）**: 2D图像资产，应用到3D表面以提供视觉细节
- **RenderData**: UE5中存储网格渲染数据的结构，包含顶点、三角形和材质信息
- **3D可视化（3D Visualization）**: 使用ASCII字符在终端中显示3D空间中Actor位置和关系的图形化表示
- **投影矩阵（Projection Matrix）**: 将3D世界坐标转换为2D屏幕坐标的数学变换
- **Z-buffer（深度缓冲）**: 存储每个像素深度值的缓冲区，用于正确处理遮挡关系
- **UE5 Python API**: 虚幻引擎的Python脚本接口，用于编辑器自动化
- **EditorLevelLibrary**: UE5 Python模块，用于关卡/地图操作
- **EditorAssetLibrary**: UE5 Python模块，用于资产操作
- **单元测试（Unit Test）**: 测试单个函数或类的特定行为的测试
- **属性测试（Property-Based Test）**: 验证通用正确性属性在大量随机输入下都成立的测试
- **pytest**: Python测试框架
- **hypothesis**: Python属性测试库
- **调试模式（Debug Mode）**: 输出详细执行信息的运行模式，用于问题诊断
- **性能分析（Performance Profiling）**: 测量和分析程序各部分执行时间的过程
- **渲染管线（Rendering Pipeline）**: 从3D数据到最终ASCII字符输出的完整处理流程

## Requirements

### 需求 1

**用户故事：** 作为开发者，我想加载并检查项目中的任何地图文件，以便在不打开UE5编辑器的情况下了解地图中存在哪些Actor和对象。

#### 验收标准

1. WHEN 用户提供地图名称或路径 THEN 地图检查工具 SHALL 使用UE5 Python API加载指定的地图
2. WHEN 地图文件不存在 THEN 地图检查工具 SHALL 显示清晰的错误消息，指示未找到地图
3. WHEN 地图文件损坏或无效 THEN 地图检查工具 SHALL 优雅地处理错误并通知用户
4. THE 地图检查工具 SHALL 支持相对路径（例如："Cosmos_002_Training_World"）和完整资产路径（例如："/Game/Maps/Cosmos_002_Training_World"）
5. WHEN 地图成功加载 THEN 地图检查工具 SHALL 检索关卡中存在的所有Actor

### 需求 2

**用户故事：** 作为开发者，我想查看地图中每个Actor的基本信息，以便快速了解地图的组成。

#### 验收标准

1. WHEN 地图检查工具检索Actor THEN 系统 SHALL 为每个Actor提取Actor的类名
2. WHEN 地图检查工具检索Actor THEN 系统 SHALL 为每个Actor提取Actor的显示名称或标签
3. WHEN 地图检查工具检索Actor THEN 系统 SHALL 为每个Actor提取Actor的世界位置（X、Y、Z坐标）
4. WHEN 地图检查工具检索Actor THEN 系统 SHALL 为每个Actor提取Actor的旋转（Pitch、Yaw、Roll）
5. WHEN 地图检查工具检索Actor THEN 系统 SHALL 为每个Actor提取Actor的缩放（X、Y、Z）
6. THE 地图检查工具 SHALL 将基本信息（名称、类型、位置、旋转、缩放）输出为篇1，便于复制粘贴

### 需求 2.1

**用户故事：** 作为开发者，我想查看Actor的详细信息，以便深入了解Actor的组件和属性配置。

#### 验收标准

1. WHEN Actor有组件 THEN 地图检查工具 SHALL 列出附加到该Actor的所有组件
2. WHEN Actor有StaticMeshComponent THEN 地图检查工具 SHALL 提取该组件引用的静态网格资产路径
3. WHEN Actor有StaticMeshComponent且网格资产可访问 THEN 地图检查工具 SHALL 使用UE5 Python API访问StaticMesh对象
4. WHEN 访问StaticMesh对象 THEN 地图检查工具 SHALL 通过RenderData获取默认质量级别的网格数据（不使用最低质量LOD）
5. WHEN 提取网格数据 THEN 地图检查工具 SHALL 获取所有顶点的位置坐标（X, Y, Z）
6. WHEN 提取网格数据 THEN 地图检查工具 SHALL 获取所有顶点的法线向量（用于光照计算和背面剔除）
7. WHEN 提取网格数据 THEN 地图检查工具 SHALL 获取所有顶点的切线和副切线向量（用于法线贴图和表面细节计算）
8. WHEN 提取网格数据 THEN 地图检查工具 SHALL 获取所有顶点的UV纹理坐标（用于纹理映射和表面细节）
9. WHEN 提取网格数据 THEN 地图检查工具 SHALL 获取顶点颜色数据（如果存在）
10. WHEN 提取网格数据 THEN 地图检查工具 SHALL 获取三角形索引数组（每三个索引定义一个三角形面）
11. WHEN 提取网格数据 THEN 地图检查工具 SHALL 获取网格的边界框信息（Bounding Box）
12. WHEN Actor有材质 THEN 地图检查工具 SHALL 提取应用到网格的材质属性（基础颜色、粗糙度、金属度、自发光等）
13. WHEN 材质有纹理 THEN 地图检查工具 SHALL 提取纹理资产引用（BaseColor、Normal、Roughness等）
14. WHEN 纹理资产可访问 THEN 地图检查工具 SHALL 提取纹理的像素数据用于字符选择
15. WHEN Actor有自定义属性 THEN 地图检查工具 SHALL 尝试提取并显示相关的自定义属性
16. THE 地图检查工具 SHALL 将详细信息（组件列表、网格数据、材质信息、纹理信息、自定义属性）输出为篇2，与篇1分开
17. THE 地图检查工具 SHALL 在篇2中为每个Actor提供清晰的分组和标识

### 需求 3

**用户故事：** 作为开发者，我想以清晰可读的格式显示Actor信息，以便轻松查看和分析地图内容。

#### 验收标准

1. THE 地图检查工具 SHALL 以结构化文本格式输出Actor信息
2. WHEN 显示Actor信息 THEN 系统 SHALL 按Actor分组信息，并有清晰的视觉分隔
3. WHEN 显示Actor信息 THEN 系统 SHALL 为不同类型的信息包含章节标题（例如："变换"、"组件"）
4. THE 地图检查工具 SHALL 显示地图中找到的Actor总数摘要
5. WHEN 存在多个相同类的Actor THEN 系统 SHALL 按类类型显示Actor计数
6. THE 地图检查工具 SHALL 将输出保存到指定输出目录中的文本文件

### 需求 4

**用户故事：** 作为开发者，我想以极致高质量的ASCII字符3D方式可视化地图，以便在终端中直观理解Actor的空间布局和关系。

#### 验收标准

1. THE 地图检查工具 SHALL 提供高质量ASCII字符3D可视化功能
2. WHEN 启用3D可视化 THEN 系统 SHALL 在终端中显示交互式3D字符图（使用真正的3D渲染管线生成ASCII艺术）
3. WHEN 生成3D字符图 THEN 系统 SHALL 仅渲染具有StaticMeshComponent且网格数据可访问的Actor
4. WHEN 生成3D字符图 THEN 系统 SHALL 从UE5提取Actor的完整网格数据（顶点位置、法线向量、切线向量、UV坐标、顶点颜色、三角形索引）
5. WHEN 生成3D字符图 THEN 系统 SHALL 从UE5提取Actor的材质数据（基础颜色、粗糙度、金属度、自发光、纹理引用）
6. WHEN 生成3D字符图 THEN 系统 SHALL 从UE5提取纹理的像素数据（如果材质包含纹理）
7. WHEN 生成3D字符图 THEN 系统 SHALL 使用提取的网格顶点数据和Actor的变换矩阵（位置、旋转、缩放）计算世界空间中的顶点位置
8. WHEN 生成3D字符图 THEN 系统 SHALL 使用等距投影矩阵（isometric projection matrix）将3D世界坐标转换为2D屏幕坐标
9. WHEN 生成3D字符图 THEN 系统 SHALL 使用深度缓冲（Z-buffer）算法正确处理遮挡关系，确保近处物体遮挡远处物体
10. WHEN 生成3D字符图 THEN 系统 SHALL 将2D屏幕坐标映射到字符网格坐标
11. WHEN 选择ASCII字符 THEN 系统 SHALL 使用顶点法线计算表面朝向，根据朝向选择字符方向（如：╱ ╲ │ ─ ╔ ╗ ╚ ╝）
12. WHEN 选择ASCII字符 THEN 系统 SHALL 使用材质粗糙度属性选择字符密度（光滑表面用█，粗糙表面用▓▒░）
13. WHEN 选择ASCII字符 THEN 系统 SHALL 使用材质金属度属性影响字符亮度和反射效果
14. WHEN 选择ASCII字符 THEN 系统 SHALL 使用纹理数据（如果可用）在UV坐标处采样，根据纹理亮度和细节选择字符
15. WHEN 选择ASCII字符 THEN 系统 SHALL 使用顶点颜色数据（如果存在）影响ANSI颜色选择
16. WHEN 选择ASCII字符 THEN 系统 SHALL 使用材质自发光属性为发光表面选择特殊高亮字符（如：★ ☆ ◆ ◇）
17. WHEN 选择ASCII字符 THEN 系统 SHALL 使用深度值（Z-buffer）影响字符亮度，远处物体使用较暗的字符
18. WHEN 生成3D字符图 THEN 系统 SHALL 支持ANSI颜色，基于材质颜色、顶点颜色和Actor类型选择颜色
19. WHEN 显示3D字符图 THEN 系统 SHALL 正确渲染立体几何体的三个可见面（基于视角和法线计算哪些三角形面可见）
20. WHEN 生成多视角显示 THEN 系统 SHALL 对每个视角使用不同的投影矩阵，确保三视图的投影方向正确对应UE5坐标系
21. WHEN 显示3D字符图 THEN 系统 SHALL 渲染光照效果和光照范围（如果场景中有灯光Actor）
22. WHEN 显示3D字符图 THEN 系统 SHALL 在字符图中清晰标注Actor名称、类型和距离信息
23. WHEN 用户进行交互操作（旋转、缩放、平移）THEN 系统 SHALL 更新投影矩阵并实时重新计算3D投影和渲染字符图
24. THE 地图检查工具 SHALL 提供多视角分屏显示（主视图、俯视图、侧视图），每个视图使用独立的投影矩阵
25. THE 地图检查工具 SHALL 提供小地图显示当前视角位置
26. THE 地图检查工具 SHALL 提供层级树面板显示Actor的层级结构
27. THE 地图检查工具 SHALL 提供选中对象的详细信息面板
28. THE 地图检查工具 SHALL 提供碰撞体积可视化显示
29. THE 地图检查工具 SHALL 提供统计信息面板（Actor数量、三角面数、内存使用等）
30. THE 地图检查工具 SHALL 提供过滤器面板，允许通过复选框控制显示的Actor类型
31. THE 地图检查工具 SHALL 提供书签系统，保存常用视角和投影参数
32. THE 地图检查工具 SHALL 支持选中高亮显示（用边框标记选中的Actor）
33. THE 地图检查工具 SHALL 支持动态Actor标记（用特殊符号标记可交互或动态的Actor）
34. WHEN 使用3D可视化 THEN 系统 SHALL 将当前3D字符图的视图保存为文本文件到输出目录
35. WHEN 未安装所需的依赖库 THEN 系统 SHALL 显示带有安装说明的有用消息

### 需求 5

**用户故事：** 作为开发者，我想通过交互式选项界面按类型或名称过滤Actor，以便专注于感兴趣的特定Actor。

#### 验收标准

1. THE 地图检查工具 SHALL 提供交互式选项配置界面，允许用户输入命令来修改过滤选项
2. THE 地图检查工具 SHALL 将过滤选项保存到本地配置文件中，以便在后续运行中保持设置
3. THE 地图检查工具 SHALL 默认不应用任何过滤器，显示所有Actor
4. WHEN 用户设置类过滤器 THEN 系统 SHALL 仅显示与指定类匹配的Actor
5. WHEN 用户设置名称过滤器 THEN 系统 SHALL 仅显示名称与模式匹配的Actor
6. WHEN 用户设置多个过滤器 THEN 系统 SHALL 使用AND逻辑应用所有过滤器
7. THE 地图检查工具 SHALL 提供命令来查看当前过滤选项
8. THE 地图检查工具 SHALL 提供命令来重置过滤选项为默认值（不过滤）

### 需求 6

**用户故事：** 作为开发者，我想让工具遵循项目的标准目录结构和执行方式，以便与现有工具保持一致性。

#### 验收标准

1. THE 地图检查工具 SHALL 位于Scripts/MapGenerators/Tools/目录中，遵循项目组织标准
2. THE 地图检查工具 SHALL 提供批处理文件包装器，以便在Windows上轻松执行
3. WHEN 执行 THEN 系统 SHALL 使用与地图生成器工具相同的UE5 Python环境（UE5.7.0源码版本）
4. THE 地图检查工具 SHALL 将结果输出到指定的输出目录（例如：Scripts/MapGenerators/Output/）
5. THE 地图检查工具 SHALL 遵循项目的文件组织标准，使用Debug文件夹存放实验性功能
6. THE 地图检查工具 SHALL 能够检查由地图生成器创建的地图文件

### 需求 7

**用户故事：** 作为开发者，我想要全面的错误处理和日志记录，以便在检查地图时排查问题。

#### 验收标准

1. WHEN 发生任何错误 THEN 地图检查工具 SHALL 记录错误，并提供足够的详细信息用于调试
2. WHEN UE5编辑器不可用 THEN 系统 SHALL 显示清晰的消息，指示编辑器必须正在运行或可访问
3. WHEN Python依赖项缺失 THEN 系统 SHALL 列出缺失的依赖项及安装说明
4. THE 地图检查工具 SHALL 通过命令行标志提供详细日志模式，用于详细的执行信息
5. WHEN 执行成功完成 THEN 系统 SHALL 显示成功消息及输出文件位置

### 需求 8

**用户故事：** 作为开发者，我想要完整的测试覆盖，以便确保工具的正确性和可靠性。

#### 验收标准

1. THE 地图检查工具 SHALL 包含单元测试，验证核心功能的正确性
2. THE 地图检查工具 SHALL 包含属性测试（Property-Based Tests），验证通用正确性属性
3. THE 地图检查工具 SHALL 将生产就绪的测试文件放置在与源文件相同的目录中，使用.test.py后缀命名
4. WHEN 测试文件与源文件同名 THEN 测试文件 SHALL 使用格式：源文件名.test.py（例如：mesh_extractor.py → mesh_extractor.test.py）
5. THE 地图检查工具 SHALL 使用pytest作为测试框架
6. THE 地图检查工具 SHALL 使用hypothesis作为属性测试库
7. THE 地图检查工具 SHALL 为每个属性测试配置至少100次迭代
8. THE 地图检查工具 SHALL 在每个属性测试中使用注释标注对应的设计文档中的正确性属性编号
9. THE 地图检查工具 SHALL 遵循项目的文件组织标准，将实验性测试脚本按任务组织在Debug/子目录中，每个任务使用独立的子目录
10. THE 地图检查工具的测试任务子目录 SHALL 使用小写加连字符的命名格式（如：Debug/test-mesh-extraction/、Debug/test-rendering-pipeline/）
11. THE 地图检查工具的每个测试任务子目录 SHALL 包含notes.txt文件，说明测试的内容和结果
12. THE 地图检查工具 SHALL 仅将通过验证的测试文件移到主目录，使用.test.py后缀

### 需求 9

**用户故事：** 作为Kiro，我想要自动化的调试方法和工具，以便快速定位和解决代码问题。

#### 验收标准

1. THE 地图检查工具 SHALL 包含自动化调试脚本，供Kiro用于分析和诊断问题
2. WHEN 发生错误 THEN Kiro SHALL 自动收集错误上下文（堆栈跟踪、变量状态、输入数据）
3. WHEN 发生错误 THEN Kiro SHALL 自动分析错误原因，生成诊断报告
4. WHEN 发生错误 THEN Kiro SHALL 提供修复建议，包括可能的代码修改方案
5. THE 地图检查工具 SHALL 提供自动化测试运行脚本，供Kiro识别失败的测试用例
6. WHEN 测试失败 THEN Kiro SHALL 分析失败原因，定位到具体的代码行
7. THE 地图检查工具 SHALL 提供自动化验证脚本，供Kiro通过重新运行测试确认问题已解决
8. THE 地图检查工具 SHALL 生成调试日志，记录Kiro的问题分析和修复过程
9. THE 地图检查工具 SHALL 将调试脚本和工具按任务组织在Debug/子目录中，每个任务使用独立的子目录
10. THE 地图检查工具的调试任务子目录 SHALL 使用小写加连字符的命名格式（如：Debug/debug-rendering/、Debug/fix-mesh-extraction/）
11. THE 地图检查工具的每个调试任务子目录 SHALL 包含notes.txt文件，记录问题描述、分析过程和解决方案
12. THE 地图检查工具 SHALL 将调试日志和诊断报告保存到Debug/task-name/目录中
13. THE 地图检查工具 SHALL 在notes.txt中记录尝试的调试方法、失败的方案和最终的解决方案
14. THE 地图检查工具 SHALL 仅将验证通过的修复代码移到主目录
15. THE 地图检查工具 SHALL 在Debug/README.txt中维护所有调试任务的概览

