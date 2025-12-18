# 增量编译优化状态

## 当前状态

### ✅ 已完成
1. **C++ 编译已跳过**
   - 添加了 `-NoCompile` 参数
   - 修改 Python 脚本时不会触发 C++ 编译
   - 启动时间从 2-3 分钟降到 < 30 秒

2. **DerivedDataCache 目录已创建**
   - 路径：`DerivedDataCache/`
   - 权限：完全控制

3. **Zen Server 配置已优化**
   - `Config/DefaultEngine.ini` 已配置强制 IPv4
   - `bEnableIPv6=false` 已添加

### ⚠️ 临时方案
**当前使用 `-DDC-ForceMemoryCache`**
- 原因：Zen Server IPv6 连接问题
- 效果：
  - ✅ UE5 可以正常启动
  - ✅ C++ 编译已跳过
  - ❌ 每次都要重新编译 Shader（5-15 分钟）

---

## 问题根源

### Zen Server IPv6 问题

**现象：**
```
UE5 尝试连接：http://[::1]:8558 (IPv6)
Zen Server 监听：http://127.0.0.1:8558 (IPv4)
结果：连接失败
```

**日志证据：**
```
LogZenServiceInstance: Warning: Unable to reach Unreal Zen Storage Server HTTP service at http://[::1]:8558
LogDerivedDataCache: Display: ZenLocal: Unable to reach ZenServer HTTP service at [::1]
```

---

## 后续优化方案

### 方案 1：修复 Zen Server IPv6 问题（推荐）

**目标：** 让 Zen Server 同时监听 IPv4 和 IPv6

**步骤：**
1. 检查 Windows 网络配置
2. 确保 IPv6 回环地址 `::1` 可用
3. 或者修改 UE5 源码，强制使用 IPv4

**预期效果：**
- 第一次运行：5-15 分钟（编译 Shader）
- 第二次运行：< 30 秒（使用缓存）

### 方案 2：使用本地文件系统缓存（备选）

**目标：** 不使用 Zen Server，直接使用文件系统缓存

**步骤：**
1. 修改启动参数：`-ddc=nozenlocalfallback`
2. 确保 `DerivedDataCache/` 目录可写

**预期效果：**
- 第一次运行：5-15 分钟（编译 Shader）
- 第二次运行：< 1 分钟（使用文件缓存，比 Zen 慢）

### 方案 3：接受现状（最简单）

**目标：** 继续使用 `-DDC-ForceMemoryCache`

**优点：**
- 无需额外配置
- UE5 可以正常启动
- C++ 编译已跳过（主要目标已达成）

**缺点：**
- 每次都要编译 Shader（5-15 分钟）

---

## 当前配置文件

### 启动参数
**文件：** `Scripts/MapGenerators/Tools/launch_generator/process_runner.py`
```python
cmd = [
    ENGINE_PATH,
    PROJECT_PATH,
    f'-ExecCmds={exec_cmd}',
    '-stdout',
    '-unattended',
    '-nopause',
    '-nosplash',
    '-NoCompile',                     # Skip C++ compilation
    '-DDC-ForceMemoryCache'           # Temporary workaround
]
```

### Zen 配置
**文件：** `Config/DefaultEngine.ini`
```ini
[Zen]
HostName=127.0.0.1
Port=8558
PreferIPv4=true
bEnableIPv6=false
```

---

## 测试结果

### 当前性能
```
运行 generate_map.bat：
  → UE5 启动：< 5 秒
  → C++ 编译：跳过 ✅
  → Shader 编译：5-15 分钟 ⏱️
  → Python 执行：< 5 秒
  → 地图生成：成功 ✅
  → 总时间：5-15 分钟
```

### 优化后预期（修复 Zen Server）
```
第一次运行：
  → 总时间：5-15 分钟（编译 Shader）

第二次运行：
  → 总时间：< 30 秒（使用缓存）🚀
```

---

## 下一步行动

### 选项 A：修复 Zen Server（推荐）
1. 研究 UE5.7.0 源码中的 Zen Server 连接逻辑
2. 找到强制使用 IPv4 的方法
3. 或者修复 IPv6 回环地址问题

### 选项 B：使用文件系统缓存
1. 测试 `-ddc=nozenlocalfallback` 参数
2. 验证文件缓存是否工作

### 选项 C：接受现状
1. 继续使用当前配置
2. 每次运行等待 5-15 分钟

---

## 相关文件

- 启动脚本：`Scripts/MapGenerators/generate_map.bat`
- Python 启动器：`Scripts/MapGenerators/launch_generator.py`
- 进程管理器：`Scripts/MapGenerators/Tools/launch_generator/process_runner.py`
- 引擎配置：`Config/DefaultEngine.ini`
- DDC 目录：`DerivedDataCache/`

---

**最后更新：** 2025-12-18 18:47
**状态：** C++ 编译已优化 ✅ | Shader 缓存待优化 ⏱️
