# DDC配置修复指南

## 问题描述

在UE5源码版本中使用命令行执行Python脚本时，可能遇到DDC（Derived Data Cache）错误：

```
Fatal error: [File:D:\UnrealEngine570\Engine\Source\Developer\DerivedDataCache\Private\DerivedDataBackends.cpp] [Line: 208] 
Unable to use default cache graph 'DerivedDataBackendGraph' because there are no readable or writable nodes available.
Add -DDC-ForceMemoryCache to the command line to bypass this if you need access to the editor settings to fix the cache configuration.
```

## 解决方案

### 方案1：使用编辑器内执行（推荐）

**优点：** 不需要修复DDC配置，100%可靠
**缺点：** 需要手动在编辑器中执行

1. 双击运行 `generate_map_editor.bat`
2. 等待编辑器加载
3. 按照屏幕提示在Python控制台执行代码

### 方案2：配置本地DDC路径

1. 打开 `Config/DefaultEngine.ini`
2. 添加或修改以下配置：

```ini
[InstalledDerivedDataBackendGraph]
MinimumDaysToKeepFile=7
Root=(Type=KeyLength, Length=120, Inner=AsyncPut)
AsyncPut=(Type=AsyncPut, Inner=Hierarchy)
Hierarchy=(Type=Hierarchical, Inner=Boot, Inner=Pak, Inner=EnginePak, Inner=Local, Inner=Shared)
Boot=(Type=Boot, Filename="%GAMEDIR%DerivedDataCache/Boot.ddc", MaxCacheSize=512)
Local=(Type=FileSystem, ReadOnly=false, Clean=false, Flush=false, PurgeTransient=true, DeleteUnused=true, UnusedFileAge=34, FoldersToClean=-1, Path="%ENGINEDIR%DerivedDataCache", EnvPathOverride=UE-LocalDataCachePath, EditorOverrideSetting=LocalDerivedDataCache)
Shared=(Type=FileSystem, ReadOnly=false, Clean=false, Flush=false, DeleteUnused=true, UnusedFileAge=10, FoldersToClean=-1, Path="%ENGINEDIR%/../../../LocalBuilds/DerivedDataCache", EnvPathOverride=UE-SharedDataCachePath, EditorOverrideSetting=SharedDerivedDataCache)
```

3. 保存文件
4. 重新运行 `generate_map_auto.bat`

### 方案3：使用内存缓存（临时方案）

批处理脚本已包含 `-DDC=ForceMemoryCache` 参数，但可能仍然失败。

如果失败，尝试修改 `generate_map_auto.bat`：

```batch
"%ENGINE_PATH%" "%PROJECT_PATH%" -ExecutePythonScript="%SCRIPT_PATH%" -ddc=noshared -stdout -unattended -nopause -nosplash
```

### 方案4：创建Editor Utility Widget（高级）

如果需要一键生成功能，可以创建Editor Utility Widget：

1. 在Content Browser中创建Editor Utility Widget
2. 添加按钮，绑定Python脚本执行
3. 保存为工具面板

## 验证DDC配置

在编辑器中：
1. Edit → Project Settings
2. 搜索 "Derived Data Cache"
3. 检查 "Local Derived Data Cache" 路径是否有效
4. 检查 "Shared Derived Data Cache" 路径是否有效

## 推荐工作流程

**开发阶段：** 使用方案1（编辑器内执行）
**生产阶段：** 修复DDC配置后使用命令行自动化

## 相关资源

- [UE5 DDC文档](https://docs.unrealengine.com/5.0/en-US/derived-data-cache/)
- [UE5 Python API文档](https://docs.unrealengine.com/5.0/en-US/PythonAPI/)
