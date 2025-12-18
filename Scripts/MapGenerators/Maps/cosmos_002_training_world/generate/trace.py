"""
UE5-compatible execution tracing module (Auto-tracing with inspect)
Automatically captures module name, line number, and timestamp
No need to hardcode line numbers!
"""

import unreal
import inspect
import time


# Global variable: script start time
_start_time = time.time()


# Status keywords for automatic inference
ERROR_KEYWORDS = ["错误", "失败", "异常"]
WARNING_KEYWORDS = ["警告", "跳过", "未找到"]
SUCCESS_KEYWORDS = ["成功", "完成", "创建", "生成", "保存", 
                    "验证成功", "放置成功", "配置", "初始化"]

# Valid status values
VALID_STATUSES = ["success", "warning", "error", "info"]


def infer_status(context):
    """
    Infer status from context keywords
    
    Args:
        context: Context description string
        
    Returns:
        status: "success", "warning", "error", or "info"
        
    Priority rules:
        1. Error keywords > Warning keywords > Success keywords
        2. No match → default "info"
    """
    if not context:
        return "info"
    
    # Convert to string if not already
    context_str = str(context)
    
    # Check error keywords first (highest priority)
    for keyword in ERROR_KEYWORDS:
        if keyword in context_str:
            return "error"
    
    # Check warning keywords second
    for keyword in WARNING_KEYWORDS:
        if keyword in context_str:
            return "warning"
    
    # Check success keywords third
    for keyword in SUCCESS_KEYWORDS:
        if keyword in context_str:
            return "success"
    
    # Default to info
    return "info"


def log_auto(context="", status=None):
    """
    Automatically log current execution position (Enhanced with status support)
    
    Args:
        context: Optional context description (e.g., "创建墙壁")
        status: Optional explicit status ("success", "warning", "error", "info")
                If None, will be inferred from context
    
    Output format:
        [TRACE:module_name:line_number:timestamp_ms:status] context
    
    Example:
        [TRACE:room_builder:25:2450:success] 创建地板
        [TRACE:room_builder:30:2500:error] 错误：资源加载失败
    """
    # Get caller's stack frame
    frame = inspect.currentframe().f_back
    
    # Auto-get module name (extract from filename)
    filename = frame.f_code.co_filename
    module_name = filename.split('/')[-1].split('\\')[-1].replace('.py', '')
    
    # Auto-get line number
    line_num = frame.f_lineno
    
    # Get timestamp (relative to script start, in milliseconds)
    elapsed_ms = int((time.time() - _start_time) * 1000)
    
    # Determine status
    if status is not None:
        # Validate explicit status
        if status not in VALID_STATUSES:
            warning_msg = f"Invalid status '{status}', defaulting to 'info'"
            unreal.log_warning(warning_msg)
            print(f"WARNING: {warning_msg}", flush=True)
            status = "info"
    else:
        # Infer status from context
        status = infer_status(context)
    
    # Output trace marker (enhanced format with status)
    marker = f"[TRACE:{module_name}:{line_num}:{elapsed_ms}:{status}]"
    if context:
        marker += f" {context}"
    
    unreal.log(marker)
    print(marker, flush=True)


def log_step(step_num, total_steps, description):
    """
    Log progress step
    
    Args:
        step_num: Current step number (1-based)
        total_steps: Total number of steps
        description: Step description
    """
    marker = f"[{step_num}/{total_steps}] {description}"
    unreal.log(marker)
    print(marker)
    
    import sys
    sys.stdout.flush()


def log_checkpoint(checkpoint_name):
    """
    Log checkpoint (auto-get line number)
    
    Args:
        checkpoint_name: Checkpoint name
    """
    frame = inspect.currentframe().f_back
    line_num = frame.f_lineno
    elapsed_ms = int((time.time() - _start_time) * 1000)
    
    marker = f"[CHECKPOINT:{line_num}:{elapsed_ms}] {checkpoint_name}"
    unreal.log(marker)
    print(marker, flush=True)
