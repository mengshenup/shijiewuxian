"""
Launcher with smart monitoring - checks output every 5s, auto-stops after 30s silence
Outputs compressed summary to save tokens
"""

import subprocess
import sys
import time
import threading
from pathlib import Path
from datetime import datetime
import os

# 确保工作目录正确
try:
    # 处理 __file__ 可能不存在的情况（例如通过 exec() 运行）
    if '__file__' in globals():
        script_dir = Path(__file__).parent.absolute()
    else:
        # 如果 __file__ 不存在，使用当前工作目录推断
        script_dir = Path.cwd() / 'Scripts' / 'MapGenerators'
    
    project_root = script_dir.parent.parent
    os.chdir(project_root)
    sys.path.insert(0, str(script_dir))
    print(f"[DEBUG] Working directory: {os.getcwd()}")
    print(f"[DEBUG] Script directory: {script_dir}")
except Exception as e:
    print(f"[ERROR] Path setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

ENGINE_PATH = r"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
PROJECT_PATH = r"D:\001xm\shijiewuxian\shijiewuxian.uproject"

# 从命令行参数获取地图名称，默认为 cosmos_002_training_world
MAP_NAME = sys.argv[1] if len(sys.argv) > 1 else "cosmos_002_training_world"
SCRIPT_PATH = f"D:/001xm/shijiewuxian/Scripts/MapGenerators/Maps/{MAP_NAME}/generate.py"

# 将地图名称转换为UE5格式（首字母大写）
def to_ue5_map_name(map_name):
    """将 cosmos_002_training_world 转换为 Cosmos_002_Training_World"""
    parts = map_name.split('_')
    return '_'.join(word.capitalize() for word in parts)

UE5_MAP_NAME = to_ue5_map_name(MAP_NAME)
MAP_PATH = Path(f"Content/Maps/{UE5_MAP_NAME}.umap")

# 调试开关：设置为True显示全部输出，False只显示压缩摘要
DEBUG_MODE = True  # 设置为True查看完整错误信息

class OutputMonitor:
    def __init__(self, log_file=None, full_log_file=None):
        self.lines = []
        self.last_output_time = time.time()
        self.is_running = True
        self.start_time = time.time()
        self.last_summarized_index = 0  # 记录上次总结到哪一行
        self.log_file = log_file  # 压缩摘要日志文件路径
        self.full_log_file = full_log_file  # 完整日志文件路径
        self.summary_log = []  # 存储所有摘要输出
        
    def add_line(self, line):
        self.lines.append(line)
        self.last_output_time = time.time()
    
    def get_new_lines_summary(self):
        """获取未总结的新行的压缩摘要"""
        new_lines = self.lines[self.last_summarized_index:]
        if not new_lines:
            return None
        
        # 更新已总结的索引
        self.last_summarized_index = len(self.lines)
        
        # 智能压缩：提取关键信息并计数
        keyword_counts = {}
        important_messages = []
        error_details = []  # 存储详细错误信息
        
        for line in new_lines:
            # 提取关键词并计数（基于真实日志分析 - 完整版）
            
            # 编译相关 (Compiling: 2次, LogShaderCompilers: 7次)
            if 'Compiling' in line or 'LogShaderCompilers' in line:
                keyword_counts['编译'] = keyword_counts.get('编译', 0) + 1
            
            # 着色器 (Shader: 7次, Shading: 6次)
            if 'Shader' in line or 'Shading' in line:
                keyword_counts['着色器'] = keyword_counts.get('着色器', 0) + 1
            
            # 加载相关 (Loading: 13次, Loaded: 29次, LogStreaming: 26次)
            if 'Loading' in line or 'Loaded' in line or 'LogStreaming' in line:
                keyword_counts['加载'] = keyword_counts.get('加载', 0) + 1
            
            # 保存相关
            if 'Saving' in line or 'Saved' in line:
                keyword_counts['保存'] = keyword_counts.get('保存', 0) + 1
            
            # 构建相关 (Building: 1次)
            if 'Building' in line or 'Build' in line:
                keyword_counts['构建'] = keyword_counts.get('构建', 0) + 1
            
            # 材质 (Material: 18次)
            if 'Material' in line:
                keyword_counts['材质'] = keyword_counts.get('材质', 0) + 1
            
            # 纹理 (Texture: 16次)
            if 'Texture' in line:
                keyword_counts['纹理'] = keyword_counts.get('纹理', 0) + 1
            
            # 音频 (Audio: 22次, LogAudio: 26次)
            if 'Audio' in line or 'LogAudio' in line:
                keyword_counts['音频'] = keyword_counts.get('音频', 0) + 1
            
            # 初始化 (Initializing: 4次)
            if 'Initializing' in line or 'Initialize' in line:
                keyword_counts['初始化'] = keyword_counts.get('初始化', 0) + 1
            
            # 挂载 (Mounted: 13次, Pak: 13次)
            if 'Mounted' in line or 'Pak' in line or 'LogPakFile' in line:
                keyword_counts['挂载'] = keyword_counts.get('挂载', 0) + 1
            
            # 处理/生成 (Processing, Generating, Creating: 4次)
            if 'Processing' in line or 'Generating' in line or 'Creating' in line:
                keyword_counts['处理'] = keyword_counts.get('处理', 0) + 1
            
            # 注册 (Registered: 6次)
            if 'Registered' in line or 'Register' in line:
                keyword_counts['注册'] = keyword_counts.get('注册', 0) + 1
            
            # 插件 (Plugins: 6次)
            if 'Plugin' in line:
                keyword_counts['插件'] = keyword_counts.get('插件', 0) + 1
            
            # 动画 (Animation: 6次)
            if 'Animation' in line or 'Anim' in line:
                keyword_counts['动画'] = keyword_counts.get('动画', 0) + 1
            
            # 配置 (LogConfig: 10次)
            if 'Config' in line or 'LogConfig' in line:
                keyword_counts['配置'] = keyword_counts.get('配置', 0) + 1
            
            # 网络 (LogUdpMessaging: 8次)
            if 'Messaging' in line or 'Network' in line:
                keyword_counts['网络'] = keyword_counts.get('网络', 0) + 1
            
            # 警告 (Warning: 11次)
            if 'Warning' in line:
                keyword_counts['警告'] = keyword_counts.get('警告', 0) + 1
            
            # 错误 (ERROR: 2次, Failed: 6次) - 记录详细信息（去重）
            if 'ERROR' in line or 'Failed' in line or 'Error' in line:
                keyword_counts['错误'] = keyword_counts.get('错误', 0) + 1
                # 提取错误详情（取前150个字符）并去重
                error_msg = line.strip()[:150]
                if error_msg not in error_details:
                    error_details.append(error_msg)
            
            # 刷新 (Flushing: 12次)
            if 'Flushing' in line or 'Flush' in line:
                keyword_counts['刷新'] = keyword_counts.get('刷新', 0) + 1
            
            # 元数据 (Metadata: 27次)
            if 'Metadata' in line:
                keyword_counts['元数据'] = keyword_counts.get('元数据', 0) + 1
            
            # 设备/驱动 (Device: 19次, Driver: 7次)
            if 'Device' in line or 'Driver' in line:
                keyword_counts['设备'] = keyword_counts.get('设备', 0) + 1
            
            # 重要消息（立即显示）
            if 'SUCCESS' in line:
                important_messages.append('✓成功')
            elif 'ERROR' in line and 'LogPython' in line:
                important_messages.append('✗错误')
            elif 'STARTING MAP GENERATOR' in line:
                important_messages.append('✓脚本启动')
            elif '[1/6]' in line:
                important_messages.append('✓准备Level')
            elif '[2/6]' in line:
                important_messages.append('✓放置TrainingRoom')
            elif '[3/6]' in line:
                important_messages.append('✓放置PlayerStart')
            elif '[4/6]' in line:
                important_messages.append('✓设置照明')
            elif '[5/6]' in line:
                important_messages.append('✓配置GameMode')
            elif '[6/6]' in line:
                important_messages.append('✓保存地图')
        
        # 构建摘要 - 使用排版模式
        summary_lines = []
        
        # 1. 优先显示重要消息（独立一行）
        if important_messages:
            summary_lines.append('  ' + ' | '.join(important_messages))
        
        # 2. 显示关键词计数（分类显示）
        if keyword_counts:
            # 按重要性分组
            high_priority = []  # 错误、警告
            medium_priority = []  # 编译、加载、保存
            low_priority = []  # 其他
            
            for keyword, count in keyword_counts.items():
                display = f"{keyword}×{count}" if count > 1 else keyword
                
                if keyword in ['错误', '警告']:
                    high_priority.append(display)
                elif keyword in ['编译', '着色器', '加载', '保存', '构建']:
                    medium_priority.append(display)
                else:
                    low_priority.append(display)
            
            # 组合显示
            parts = []
            if high_priority:
                parts.append('⚠ ' + ' | '.join(high_priority))
            if medium_priority:
                parts.append(' | '.join(medium_priority))
            if low_priority and len(low_priority) <= 5:  # 只显示前5个次要信息
                parts.append(' | '.join(low_priority[:5]))
            
            if parts:
                summary_lines.append('  ' + ' '.join(parts))
        
        # 3. 显示错误详情（独立行，红色标记）
        if error_details:
            for error in error_details[:3]:  # 最多显示3个错误
                summary_lines.append(f"  ✗ {error}")
        
        # 4. 如果没有任何信息，显示行数
        if not summary_lines:
            summary_lines.append(f"  {len(new_lines)}行日志")
        
        result = '\n'.join(summary_lines)
        
        # 保存到摘要日志
        if result:
            self.summary_log.append(f"[{datetime.now().strftime('%H:%M:%S')}]")
            self.summary_log.append(result)
        
        return result
    
    def get_compressed_summary(self):
        """智能压缩总结输出"""
        summary = []
        
        # 基本统计
        total_lines = len(self.lines)
        elapsed = time.time() - self.start_time
        summary.append(f"执行时间: {elapsed:.1f}秒")
        summary.append(f"总输出行数: {total_lines}")
        
        # 分析关键步骤
        steps_completed = []
        errors = []
        
        for line in self.lines:
            # Python脚本执行步骤
            if 'STARTING MAP GENERATOR' in line:
                steps_completed.append("✓ 脚本启动")
            elif '[1/6] Preparing level' in line:
                steps_completed.append("✓ [1/6] 准备Level")
            elif '[2/6] Placing TrainingRoom' in line:
                steps_completed.append("✓ [2/6] 放置TrainingRoom")
            elif '[3/6] Placing PlayerStart' in line:
                steps_completed.append("✓ [3/6] 放置PlayerStart")
            elif '[4/6] Setting up lighting' in line:
                steps_completed.append("✓ [4/6] 设置照明")
            elif '[5/6] Configuring GameMode' in line:
                steps_completed.append("✓ [5/6] 配置GameMode")
            elif '[6/6] Saving map' in line:
                steps_completed.append("✓ [6/6] 保存地图")
            elif 'Map generation completed successfully' in line:
                steps_completed.append("✓ 地图生成完成")
            elif 'SUCCESS!' in line and 'LogPython' in line:
                steps_completed.append("✓ 脚本执行成功")
            
            # 错误检测
            if 'ERROR' in line or 'Exception' in line or 'Failed to load' in line:
                if 'LogPython' in line or 'TrainingRoom' in line or 'PlayerStart' in line:
                    errors.append(line.strip())
        
        # 输出步骤
        if steps_completed:
            summary.append(f"\n完成步骤 ({len(steps_completed)}):")
            for step in steps_completed:
                summary.append(f"  {step}")
        
        # 输出错误
        if errors:
            summary.append(f"\n检测到错误 ({len(errors)}):")
            for error in errors[:5]:  # 最多显示5个错误
                summary.append(f"  {error[:100]}")  # 每个错误最多100字符
        
        result = "\n".join(summary)
        
        # 保存完整摘要到日志
        self.summary_log.append("\n" + "="*60)
        self.summary_log.append("  执行摘要 (压缩)")
        self.summary_log.append("="*60)
        self.summary_log.append(result)
        self.summary_log.append("="*60)
        
        return result
    
    def save_logs(self):
        """保存压缩摘要日志和完整日志到文件"""
        # 保存压缩摘要
        if self.log_file:
            try:
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    # 只写入压缩摘要
                    f.write("="*60 + "\n")
                    f.write("  压缩摘要日志\n")
                    f.write("="*60 + "\n\n")
                    f.write('\n'.join(self.summary_log))
                    f.write("\n")
                
                print(f"\n✓ 压缩摘要已保存到: {self.log_file}")
            except Exception as e:
                print(f"\n⚠ 保存压缩摘要失败: {e}")
        
        # 保存完整日志
        if self.full_log_file:
            try:
                with open(self.full_log_file, 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("  完整输出日志\n")
                    f.write("="*60 + "\n\n")
                    for line in self.lines:
                        f.write(line)
                    f.write("\n")
                
                print(f"✓ 完整日志已保存到: {self.full_log_file}")
            except Exception as e:
                print(f"⚠ 保存完整日志失败: {e}")

def monitor_timeout(monitor, timeout=30, process=None):
    """Monitor thread - checks for timeout every 5 seconds"""
    while monitor.is_running:
        time.sleep(5)
        elapsed = time.time() - monitor.last_output_time
        
        # 显示新输出的摘要（静默模式）
        if not DEBUG_MODE:
            summary = monitor.get_new_lines_summary()
            if summary:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
                print(summary)
        
        # 检查超时
        if elapsed > timeout:
            print(f"\n[监控] {timeout}秒无新输出，自动停止...")
            print(f"  总输出行数: {len(monitor.lines)}")
            # 显示最后第二行（避免显示无关的USB错误）
            if len(monitor.lines) >= 2:
                print(f"  最后第二行: {monitor.lines[-2][:100]}")
            elif len(monitor.lines) == 1:
                print(f"  最后一行: {monitor.lines[-1][:100]}")
            else:
                print(f"  (无输出)")
            monitor.is_running = False
            
            # 终止进程
            if process and process.poll() is None:
                print(f"  正在终止 UE5 进程...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                    print(f"  ✓ 进程已终止")
                except:
                    process.kill()
                    print(f"  ✓ 进程已强制终止")
            break

def main():
    print("\n" + "="*60)
    print("  地图生成器 (智能监控 + 自动重试)")
    print("="*60)
    print(f"地图名称: {MAP_NAME}")
    print(f"脚本路径: {SCRIPT_PATH}")
    print(f"目标地图: {UE5_MAP_NAME}.umap")
    print("监控策略: 每5秒检查，10秒无输出自动停止")
    print("输出策略: 静默运行，最后输出压缩摘要")
    print("自动重试: 如果编译未完成，自动重新运行")
    print("="*60 + "\n")
    
    max_attempts = 5  # 最多尝试5次
    attempt = 1
    retry_count = 0  # 实际重试次数（不包括第一次）
    
    while attempt <= max_attempts:
        print(f"\n{'='*60}")
        if attempt == 1:
            print(f"  首次尝试")
        else:
            print(f"  重试 {retry_count}/{max_attempts - 1}")
        print(f"{'='*60}\n")
        
        result, reason = run_generation_attempt(attempt)
        
        if result == 0:
            # 成功
            print(f"\n{'='*60}")
            print(f"✓ 地图生成成功！")
            if retry_count > 0:
                print(f"  (经过 {retry_count} 次重试)")
            print(f"{'='*60}")
            return 0
        elif result == 2:
            # 需要重试（编译未完成）
            if attempt >= max_attempts:
                print(f"\n{'='*60}")
                print(f"✗ 达到最大重试次数 ({max_attempts})，放弃")
                print(f"  原因: {reason}")
                print(f"  建议: 在编辑器中手动运行脚本")
                print(f"{'='*60}")
                return 1
            
            print(f"\n⚠ 需要重试")
            print(f"  原因: {reason}")
            print(f"  等待 3 秒后重试...")
            attempt += 1
            retry_count += 1
            time.sleep(3)  # 等待3秒再重试
        else:
            # 真正的错误（不应该重试）
            print(f"\n{'='*60}")
            print(f"✗ 生成失败 (错误码: {result})")
            print(f"  原因: {reason}")
            print(f"  这不是编译问题，重试无效")
            print(f"{'='*60}")
            return result
    
    # 不应该到达这里
    print(f"\n✗ 未知错误")
    return 1

def run_generation_attempt(attempt_num):
    """运行一次生成尝试
    
    Returns:
        tuple: (result_code, reason_message)
            result_code: 0=成功, 1=失败, 2=需要重试
            reason_message: 详细原因说明
    """
    cmd = [
        ENGINE_PATH,
        PROJECT_PATH,
        f'-ExecCmds=py {SCRIPT_PATH}',
        '-stdout',
        '-unattended',
        '-nopause',
        '-nosplash',
        '-ddc=InstalledNoZenLocalFallback',
        '-NoZenAutoLaunch'  # 禁用 Zen 服务器自动启动，避免 30 秒超时等待
    ]
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 启动UE5...")
    if DEBUG_MODE:
        print("(调试模式: 显示全部输出)\n")
    else:
        print("(静默运行中，请等待...)\n")
    sys.stdout.flush()
    
    # 创建日志文件路径
    log_file = Path(f"Scripts/MapGenerators/Maps/{MAP_NAME}/last_run.log")  # 压缩摘要
    full_log_file = Path(f"Scripts/MapGenerators/ue5_full_log.txt")  # 完整日志
    monitor = OutputMonitor(log_file=log_file, full_log_file=full_log_file)
    
    # 记录执行前的地图文件大小（用于对比）
    old_size = 0
    old_mtime = None
    if MAP_PATH.exists():
        old_stat = MAP_PATH.stat()
        old_size = old_stat.st_size
        old_mtime = old_stat.st_mtime
    
    # Run process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    # Start timeout monitor thread (传入 process 以便终止)
    monitor_thread = threading.Thread(target=monitor_timeout, args=(monitor, 10, process))
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Read output and detect key events
    compilation_detected = False
    script_started = False
    script_error = False
    error_messages = []
    last_function = None  # 追踪最后执行的函数
    last_trace_line = None  # 最后的TRACE行号
    last_checkpoint = None  # 最后的检查点
    
    # Track progress: count created actors
    actors_created = 0
    expected_actors = 0  # Will be extracted from script output
    progress_steps = {
        '[1/6]': False,
        '[2/6]': False,
        '[3/6]': False,
        '[4/6]': False,
        '[5/6]': False,
        '[6/6]': False
    }
    
    try:
        for line in process.stdout:
            if not monitor.is_running:
                process.terminate()
                break
            monitor.add_line(line)
            
            # 检测新的TRACE标记
            if 'LogPython' in line and '[TRACE:' in line:
                # 提取TRACE信息
                if '[TRACE:LINE:' in line:
                    try:
                        line_num_str = line.split('[TRACE:LINE:')[1].split(']')[0]
                        last_trace_line = int(line_num_str)
                    except:
                        pass
                elif '[TRACE:CHECKPOINT:' in line:
                    try:
                        checkpoint_str = line.split('[TRACE:CHECKPOINT:')[1].split(']')[0]
                        parts = checkpoint_str.split()
                        if len(parts) >= 2:
                            last_checkpoint = parts[1]  # 检查点名称
                            last_trace_line = int(parts[0])  # 行号
                    except:
                        pass
                elif '[TRACE:ENTER:' in line or '[TRACE:EXIT:' in line:
                    try:
                        # 提取函数名和行号
                        if '[TRACE:ENTER:' in line:
                            parts = line.split('[TRACE:ENTER:')[1].split(']')
                        else:
                            parts = line.split('[TRACE:EXIT:')[1].split(']')
                        
                        if len(parts) >= 2:
                            last_trace_line = int(parts[0])
                            last_function = parts[1].strip()
                    except:
                        pass
            
            # 检测脚本启动
            if 'STARTING MAP GENERATOR' in line:
                script_started = True
            
            # 检测编译活动
            if 'Compiling' in line or 'Building' in line or 'Shader' in line:
                compilation_detected = True
            
            # 检测脚本错误
            if 'LogPython' in line and ('ERROR' in line or 'Exception' in line):
                script_error = True
                error_messages.append(line.strip())
            
            # 追踪UE5引擎状态（表明脚本已完成）
            if 'LogAssetRegistry' in line and 'cache written' in line:
                last_function = "UE5引擎 - 保存资产注册表缓存（脚本已完成）"
            elif 'LogContentValidation' in line and 'Starting to validate' in line:
                last_function = "UE5引擎 - 验证资产（脚本已完成，正在清理）"
            elif 'LogRenderer' in line and 'Warning' in line:
                last_function = "UE5引擎 - 渲染器警告（脚本已完成，正在退出）"
            
            # 追踪进度步骤（从 unreal.log() 输出，格式为 LogPython: Display: [1/6] ...）
            if 'LogPython' in line:
                for step in progress_steps:
                    if step in line:
                        progress_steps[step] = True
                        # 实时显示进度
                        if not DEBUG_MODE:
                            completed = sum(1 for v in progress_steps.values() if v)
                            print(f"  进度: {step} ({completed}/6)")
                            sys.stdout.flush()
                
                # 追踪最后执行的函数/步骤（通过行号）
                # 格式: LogPython: Warning: D:/path/generate.py:105: DeprecationWarning: ...
                if 'generate.py:' in line:
                    try:
                        # 提取行号
                        line_num_str = line.split('generate.py:')[1].split(':')[0]
                        line_num = int(line_num_str)
                        
                        # 根据行号判断执行位置（基于generate.py的代码结构）
                        if line_num >= 28 and line_num <= 29:
                            last_function = f"__init__() - 初始化 (行{line_num})"
                        elif line_num >= 90 and line_num <= 125:
                            if line_num <= 95:
                                last_function = f"create_new_level() - 开始准备Level (行{line_num})"
                            elif line_num <= 105:
                                last_function = f"create_new_level() - 加载地图 (行{line_num})"
                            elif line_num <= 115:
                                last_function = f"create_new_level() - 获取World引用 (行{line_num})"
                            else:
                                last_function = f"create_new_level() - Level准备完成 (行{line_num})"
                        elif line_num >= 180 and line_num <= 250:
                            last_function = f"place_training_room() - 创建训练室 (行{line_num})"
                        elif line_num >= 300 and line_num <= 350:
                            last_function = f"place_player_start() - 放置PlayerStart (行{line_num})"
                        elif line_num >= 360 and line_num <= 450:
                            last_function = f"setup_lighting() - 设置照明 (行{line_num})"
                        elif line_num >= 460 and line_num <= 490:
                            last_function = f"configure_game_mode() - 配置GameMode (行{line_num})"
                        elif line_num >= 495 and line_num <= 540:
                            last_function = f"save_map() - 保存地图 (行{line_num})"
                        else:
                            last_function = f"generate.py 行{line_num}"
                    except:
                        pass
                
                # 追踪最后执行的函数/步骤（通过文本内容）
                if 'Preparing level' in line:
                    last_function = "create_new_level() - 准备Level"
                elif 'Map exists, loading' in line:
                    last_function = "create_new_level() - 加载现有地图"
                elif 'Getting world reference' in line:
                    last_function = "create_new_level() - 获取World引用"
                elif 'Map loaded, will regenerate' in line:
                    last_function = "create_new_level() - 地图加载完成"
                elif 'Level ready' in line:
                    last_function = "create_new_level() - Level准备完成"
                elif 'Creating training room' in line:
                    last_function = "place_training_room() - 开始创建训练室"
                elif 'Loading cube mesh' in line:
                    last_function = "place_training_room() - 加载Cube网格"
                elif 'Loading plane mesh' in line:
                    last_function = "place_training_room() - 加载Plane网格"
                elif 'Loading floor material' in line:
                    last_function = "place_training_room() - 加载地板材质"
                elif 'Loading wall material' in line:
                    last_function = "place_training_room() - 加载墙壁材质"
                elif 'Loading transparent glass material' in line:
                    last_function = "place_training_room() - 加载透明玻璃材质"
                elif 'Training room geometry created' in line:
                    last_function = "place_training_room() - 训练室创建完成"
                elif 'Placing PlayerStart' in line:
                    last_function = "place_player_start() - 放置PlayerStart"
                elif 'PlayerStart placed' in line:
                    last_function = "place_player_start() - PlayerStart放置完成"
                elif 'Setting up lighting' in line:
                    last_function = "setup_lighting() - 设置照明"
                elif 'Lighting system configured' in line:
                    last_function = "setup_lighting() - 照明系统配置完成"
                elif 'Configuring GameMode' in line:
                    last_function = "configure_game_mode() - 配置GameMode"
                elif 'GameMode set to' in line:
                    last_function = "configure_game_mode() - GameMode设置完成"
                elif 'Saving map' in line:
                    last_function = "save_map() - 保存地图"
                elif 'Map saved successfully' in line:
                    last_function = "save_map() - 地图保存成功"
                elif 'Map generation completed' in line:
                    last_function = "generate_map() - 地图生成完成"
                elif 'STARTING MAP GENERATOR' in line:
                    last_function = "main() - 脚本启动"
                
                # 统计创建的 actors（检测 "Created:" 关键字）
                if 'Created:' in line or 'created:' in line:
                    actors_created += 1
                
                # 提取预期的 actors 总数（从 "Total actors created:" 行）
                if 'Total actors created:' in line:
                    try:
                        # 格式: "LogPython: Display: Total actors created: 15"
                        parts = line.split(':')
                        if len(parts) >= 3:
                            expected_actors = int(parts[-1].strip())
                    except:
                        pass
            
            # 调试模式：显示全部输出
            if DEBUG_MODE:
                print(line.rstrip())
                sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n[监控] 用户中断")
        process.terminate()
        return (1, "用户中断")
    
    process.wait()
    monitor.is_running = False
    
    # Output compressed summary with progress
    print("\n" + "="*60)
    print("  执行摘要 (压缩)")
    print("="*60)
    print(monitor.get_compressed_summary())
    
    # 显示进度统计
    completed_steps = sum(1 for completed in progress_steps.values() if completed)
    total_steps = len(progress_steps)
    step_progress = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
    print(f"\n构建进度:")
    print(f"  步骤完成: {completed_steps}/{total_steps} ({step_progress:.0f}%)")
    for step, completed in progress_steps.items():
        status = "✓" if completed else "✗"
        print(f"    {status} {step}")
    
    if expected_actors > 0:
        actor_progress = (actors_created / expected_actors * 100) if expected_actors > 0 else 0
        print(f"  Actors创建: {actors_created}/{expected_actors} ({actor_progress:.0f}%)")
    else:
        print(f"  Actors创建: {actors_created} (未知总数)")
    
    # 显示追踪信息
    if last_trace_line or last_checkpoint or last_function:
        print(f"\n执行追踪:")
        if last_checkpoint:
            print(f"  最后检查点: {last_checkpoint}")
        if last_function:
            print(f"  最后函数: {last_function}")
        if last_trace_line:
            print(f"  最后追踪行号: {last_trace_line}")
    else:
        print(f"\n执行追踪:")
        print(f"  (无追踪信息 - 脚本可能未启动)")
    
    # 从日志中提取详细的追踪信息
    detailed_trace_line = None
    detailed_trace_context = None
    
    for line in reversed(monitor.lines):
        # 从新的TRACE标记中提取
        if 'LogPython' in line and '[TRACE:' in line and not detailed_trace_line:
            try:
                if '[TRACE:CHECKPOINT:' in line:
                    checkpoint_str = line.split('[TRACE:CHECKPOINT:')[1].split(']')[0]
                    parts = checkpoint_str.split()
                    if len(parts) >= 2:
                        detailed_trace_line = int(parts[0])
                        detailed_trace_context = f"检查点: {parts[1]}"
                elif '[TRACE:LINE:' in line:
                    line_num_str = line.split('[TRACE:LINE:')[1].split(']')[0]
                    detailed_trace_line = int(line_num_str)
                    # 尝试提取上下文
                    if ']' in line:
                        context = line.split(']', 1)[1].strip()
                        if context:
                            detailed_trace_context = context[:100]
                        else:
                            detailed_trace_context = "正常执行"
                elif '[TRACE:ENTER:' in line:
                    parts = line.split('[TRACE:ENTER:')[1].split(']')
                    if len(parts) >= 2:
                        detailed_trace_line = int(parts[0])
                        detailed_trace_context = f"进入函数: {parts[1].strip()}"
                elif '[TRACE:EXIT:' in line:
                    parts = line.split('[TRACE:EXIT:')[1].split(']')
                    if len(parts) >= 2:
                        detailed_trace_line = int(parts[0])
                        detailed_trace_context = f"退出函数: {parts[1].strip()}"
                elif '[TRACE:BEFORE_API:' in line or '[TRACE:AFTER_API:' in line:
                    if '[TRACE:BEFORE_API:' in line:
                        parts = line.split('[TRACE:BEFORE_API:')[1].split(']')
                        prefix = "调用前"
                    else:
                        parts = line.split('[TRACE:AFTER_API:')[1].split(']')
                        prefix = "调用后"
                    
                    if len(parts) >= 2:
                        detailed_trace_line = int(parts[0])
                        detailed_trace_context = f"{prefix}: {parts[1].strip()}"
            except:
                pass
        
        # 从异常traceback中提取
        if 'LogPython: Error:' in line and ', line ' in line and not detailed_trace_line:
            try:
                line_num_str = line.split(', line ')[1].split(',')[0].strip()
                detailed_trace_line = int(line_num_str)
                if ' in ' in line:
                    func_name = line.split(' in ')[1].strip()
                    detailed_trace_context = f"异常: {func_name}"
                else:
                    detailed_trace_context = "异常"
            except:
                pass
    
    if detailed_trace_line:
        print(f"\n详细追踪:")
        print(f"  行号: {detailed_trace_line}")
        if detailed_trace_context:
            print(f"  上下文: {detailed_trace_context}")
    
    print("="*60)
    
    # 保存日志到文件
    monitor.save_logs()
    
    # Analyze result
    map_exists = MAP_PATH.exists()
    
    if map_exists:
        # 成功：地图文件已生成
        stat = MAP_PATH.stat()
        new_size = stat.st_size
        new_mtime = stat.st_mtime
        
        print(f"\n✓ 成功: 地图文件已生成")
        print(f"  路径: {MAP_PATH}")
        
        # 显示文件大小对比
        if old_size > 0:
            size_diff = new_size - old_size
            print(f"  旧文件大小: {old_size:,} bytes ({old_size/1024:.2f} KB)")
            print(f"  新文件大小: {new_size:,} bytes ({new_size/1024:.2f} KB)")
            
            if size_diff > 0:
                print(f"  大小变化: +{size_diff:,} bytes (+{size_diff/1024:.2f} KB, {(size_diff/old_size)*100:.1f}% 增大)")
            elif size_diff < 0:
                print(f"  大小变化: {size_diff:,} bytes ({size_diff/1024:.2f} KB, {abs(size_diff/old_size)*100:.1f}% 减小)")
            else:
                print(f"  大小变化: 无变化")
            
            # 显示修改时间对比
            if old_mtime and new_mtime != old_mtime:
                print(f"  旧修改时间: {datetime.fromtimestamp(old_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  新修改时间: {datetime.fromtimestamp(new_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"  修改时间: {datetime.fromtimestamp(new_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            # 首次生成，没有旧文件
            print(f"  文件大小: {new_size:,} bytes ({new_size/1024:.2f} KB)")
            print(f"  修改时间: {datetime.fromtimestamp(new_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        return (0, "地图生成成功")
    
    # 地图未生成，分析原因
    if script_error:
        # Python 脚本执行错误（不应该重试）
        reason = "Python 脚本执行错误"
        if error_messages:
            reason += f": {error_messages[0][:100]}"
        return (1, reason)
    
    if not script_started:
        # 脚本根本没启动（不应该重试）
        return (1, "Python 脚本未启动，可能是 UE5 启动失败")
    
    if compilation_detected:
        # 脚本启动了，检测到编译，但地图未生成（可能需要重试）
        return (2, "检测到资源编译活动，UE5 可能在编译完成前退出")
    
    # 其他未知错误（不应该重试）
    return (1, "未知错误：脚本启动但地图未生成，且无编译活动")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
