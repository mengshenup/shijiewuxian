"""
Timeout monitoring module - monitors for silence and auto-stops
"""

import time
from datetime import datetime
from config import DEBUG_MODE
from summary_generator import get_new_lines_summary


def monitor_timeout(monitor, timeout, check_interval, process=None):
    """Monitor thread - checks for timeout every N seconds"""
    while monitor.is_running:
        time.sleep(check_interval)
        elapsed = monitor.get_silence_duration()
        
        # Show new output summary (silent mode)
        if not DEBUG_MODE:
            summary = get_new_lines_summary(monitor)
            if summary:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
                print(summary)
        
        # Check timeout (only if we've received output)
        if monitor.has_output and elapsed > timeout:
            print(f"\n[监控] {timeout}秒无新输出，自动停止...")
            print(f"  总输出行数: {len(monitor.lines)}")
            
            # Show last lines
            if len(monitor.lines) >= 2:
                print(f"  最后第二行: {monitor.lines[-2][:100]}")
            elif len(monitor.lines) == 1:
                print(f"  最后一行: {monitor.lines[-1][:100]}")
            else:
                print(f"  (无输出)")
            
            monitor.stop()
            
            # Terminate process
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
