"""
Output monitoring module - tracks and summarizes UE5 output
"""

import time
from datetime import datetime


class OutputMonitor:
    """Monitors and summarizes UE5 output"""
    
    def __init__(self, log_file=None, full_log_file=None):
        self.lines = []
        self.last_output_time = None  # Will be set on first output
        self.is_running = True
        self.start_time = time.time()
        self.last_summarized_index = 0
        self.log_file = log_file
        self.full_log_file = full_log_file
        self.summary_log = []
        self.has_output = False  # Track if we've received any output
        self.is_compiling = False  # Track if shader compilation is in progress
        self.timeout_paused = False  # Track if timeout is paused
    
    def add_line(self, line):
        """Add a new output line"""
        self.lines.append(line)
        current_time = time.time()
        
        # Check for shader compilation keywords
        line_lower = line.lower()
        if 'compiling' in line_lower and 'shader' in line_lower:
            if not self.is_compiling:
                self.is_compiling = True
                self.timeout_paused = True
                print(f"\n[编译] 检测到 Shader 编译，暂停超时检测...")
        elif self.is_compiling:
            # Check for compilation completion keywords (more specific)
            # Only end compilation state when we see specific completion messages
            if 'logpython' in line_lower:
                # Python script started - compilation must be done
                self.is_compiling = False
                self.timeout_paused = False
                print(f"[编译] Shader 编译结束，恢复超时检测")
            elif 'shader' in line_lower and any(keyword in line_lower for keyword in ['compiled', 'complete', 'finished']):
                # Shader-specific completion message
                self.is_compiling = False
                self.timeout_paused = False
                print(f"[编译] Shader 编译结束，恢复超时检测")
        
        if not self.has_output:
            # First output - start the timeout timer
            self.has_output = True
            self.last_output_time = current_time
        else:
            self.last_output_time = current_time
    
    def get_elapsed_time(self):
        """Get elapsed time since start"""
        return time.time() - self.start_time
    
    def get_silence_duration(self):
        """Get duration since last output"""
        if self.last_output_time is None:
            # No output yet, return 0 (no silence)
            return 0
        # If timeout is paused (e.g., during compilation), return 0 to prevent timeout
        if self.timeout_paused:
            return 0
        return time.time() - self.last_output_time
    
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
