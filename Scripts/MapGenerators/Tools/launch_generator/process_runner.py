"""
Process running module - runs UE5 process and monitors output
"""

import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from config import ENGINE_PATH, PROJECT_PATH, SCRIPT_PATH, DEBUG_MODE, TIMEOUT_SECONDS, CHECK_INTERVAL, UE5_LOG_DIR
from output_monitor import OutputMonitor
from timeout_monitor import monitor_timeout
from trace_parser import TraceInfo, parse_line
from summary_generator import get_compressed_summary
from log_saver import save_logs
from result_analyzer import analyze_result, print_progress_stats, print_trace_info


def get_latest_ue5_log():
    """Find the most recently modified UE5 log file"""
    if not UE5_LOG_DIR.exists():
        return None
    
    log_files = list(UE5_LOG_DIR.glob("shijiewuxian*.log"))
    if not log_files:
        return None
    
    # Return the most recently modified log file
    latest = max(log_files, key=lambda p: p.stat().st_mtime)
    return latest


def tail_ue5_log(monitor, trace_info, process, start_pos=0, log_file=None):
    """
    Tail UE5 log file and feed lines to monitor
    Returns tuple: (last_file_position, log_file_path)
    """
    try:
        # Find latest log file if not provided
        if log_file is None:
            log_file = get_latest_ue5_log()
            if log_file is None:
                return (start_pos, None)
        
        if not log_file.exists():
            return (start_pos, log_file)
        
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(start_pos)
            lines_read = 0
            for line in f:
                if not monitor.is_running or process.poll() is not None:
                    break
                
                monitor.add_line(line)
                parse_line(line, trace_info)
                lines_read += 1
                
                # Debug mode: show all output
                if DEBUG_MODE:
                    print(line.rstrip())
                    sys.stdout.flush()
            
            new_pos = f.tell()
            if DEBUG_MODE and lines_read > 0:
                print(f"[DEBUG] 读取了 {lines_read} 行，位置: {start_pos} -> {new_pos}")
            return (new_pos, log_file)
    except Exception as e:
        print(f"[警告] 读取UE5日志失败: {e}")
        return (start_pos, log_file)


def run_generation_attempt(attempt_num, log_file, full_log_file, old_size, old_mtime):
    """
    Run one generation attempt
    
    Returns:
        tuple: (result_code, reason_message)
            result_code: 0=success, 1=failure, 2=needs_retry
            reason_message: detailed reason
    """
    # Ensure DerivedDataCache directory exists
    ddc_dir = Path("DerivedDataCache")
    if not ddc_dir.exists():
        print(f"[初始化] 创建 DDC 目录: {ddc_dir}")
        ddc_dir.mkdir(parents=True, exist_ok=True)
    
    # ExecCmds format - use quotes for the command
    exec_cmd = f'py {SCRIPT_PATH}'
    cmd = [
        ENGINE_PATH,
        PROJECT_PATH,
        f'-ExecCmds={exec_cmd}',
        '-stdout',
        '-unattended',
        '-nopause',
        '-nosplash',
        '-DDC-ForceMemoryCache'      # Force memory cache, bypass all disk/Zen cache
    ]
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 启动UE5...")
    if DEBUG_MODE:
        print("(调试模式: 显示全部输出)\n")
    else:
        print("(静默运行中，请等待...)\n")
    sys.stdout.flush()
    
    # Delete old log files to ensure UE5 creates a new one
    deleted_count = 0
    if UE5_LOG_DIR.exists():
        old_log_files = list(UE5_LOG_DIR.glob("shijiewuxian*.log"))
        for log_file in old_log_files:
            try:
                log_file.unlink()
                deleted_count += 1
            except Exception as e:
                if DEBUG_MODE:
                    print(f"[DEBUG] 无法删除 {log_file.name}: {e}")
    
    if DEBUG_MODE:
        print(f"[DEBUG] 已删除 {deleted_count} 个旧日志文件")
    
    # Record that we expect a new log file
    existing_log_files = set()  # Empty set since we deleted all logs
    
    # Create monitor
    monitor = OutputMonitor(log_file=log_file, full_log_file=full_log_file)
    
    # Create trace info
    trace_info = TraceInfo()
    
    # Run process
    if DEBUG_MODE:
        print(f"[DEBUG] 启动命令: {' '.join(cmd[:3])}")
    
    # Redirect stdout to devnull to avoid pipe blocking and keep output clean
    # We read from log files instead for monitoring
    import os
    devnull = open(os.devnull, 'w')
    process = subprocess.Popen(
        cmd,
        stdout=devnull,  # Redirect to null to avoid blocking
        stderr=devnull,  # Redirect to null
    )
    if DEBUG_MODE:
        print(f"[DEBUG] 进程PID: {process.pid}")
    
    # Start timeout monitor thread
    monitor_thread = threading.Thread(
        target=monitor_timeout,
        args=(monitor, TIMEOUT_SECONDS, CHECK_INTERVAL, process)
    )
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Monitor UE5 log file instead of stdout
    try:
        startup_wait_shown = False
        last_log_check = time.time()
        ue5_log_file = None
        log_start_pos = 0
        log_file_found = False
        wait_for_new_file_timeout = 60  # Wait up to 60 seconds for new log file
        start_wait_time = time.time()
        
        while process.poll() is None and monitor.is_running:
            # Check for new log file every 0.5 seconds
            if not log_file_found or time.time() - last_log_check > 2:
                # Find new log files created after UE5 started
                if UE5_LOG_DIR.exists():
                    current_log_files = set(UE5_LOG_DIR.glob("shijiewuxian*.log"))
                    new_log_files = current_log_files - existing_log_files
                    
                    if DEBUG_MODE and not log_file_found and time.time() - start_wait_time > 10:
                        # Show debug info every 10 seconds
                        if int(time.time() - start_wait_time) % 10 == 0:
                            print(f"[DEBUG] 当前日志文件数: {len(current_log_files)}, 新文件数: {len(new_log_files)}")
                            if current_log_files:
                                latest = max(current_log_files, key=lambda p: p.stat().st_mtime)
                                print(f"[DEBUG] 最新文件: {latest.name}, 修改时间: {latest.stat().st_mtime}")
                    
                    if new_log_files:
                        # Use the newest log file (ONLY new files)
                        new_log_file = max(new_log_files, key=lambda p: p.stat().st_mtime)
                        if new_log_file != ue5_log_file:
                            print(f"[✓] 检测到新日志文件: {new_log_file.name}")
                            ue5_log_file = new_log_file
                            log_start_pos = 0  # Start from beginning of new file
                            log_file_found = True
                            # Reset monitor's last_output_time to start timeout from now
                            monitor.last_output_time = None
                            monitor.has_output = False
                    elif not log_file_found:
                        # Check if we've been waiting too long
                        if time.time() - start_wait_time > wait_for_new_file_timeout:
                            print(f"\n[错误] {wait_for_new_file_timeout}秒内未检测到新日志文件")
                            print(f"  UE5 可能启动失败或日志文件路径错误")
                            print(f"  请检查: {UE5_LOG_DIR}")
                            monitor.stop()
                            break
                
                last_log_check = time.time()
            
            if ue5_log_file:
                log_start_pos, ue5_log_file = tail_ue5_log(monitor, trace_info, process, log_start_pos, ue5_log_file)
            
            # Show startup wait message if no output yet
            if not log_file_found and not startup_wait_shown:
                if time.time() - monitor.start_time > 5:
                    print("[等待] UE5正在启动，等待新日志文件创建...")
                    startup_wait_shown = True
            
            time.sleep(0.5)  # Check every 0.5 seconds
        
        # Read any remaining log content
        tail_ue5_log(monitor, trace_info, process, log_start_pos, ue5_log_file)
    
    except KeyboardInterrupt:
        print("\n[监控] 用户中断")
        process.terminate()
        return (1, "用户中断")
    
    process.wait()
    monitor.stop()
    
    # Output summary
    print("\n" + "="*60)
    print("  执行摘要 (压缩)")
    print("="*60)
    print(get_compressed_summary(monitor))
    
    # Print progress stats
    print_progress_stats(trace_info)
    
    # Print trace info (now includes module history and performance analysis)
    print_trace_info(trace_info)
    
    print("="*60)
    
    # Save logs
    save_logs(monitor)
    
    # Analyze result
    return analyze_result(trace_info, old_size, old_mtime)
