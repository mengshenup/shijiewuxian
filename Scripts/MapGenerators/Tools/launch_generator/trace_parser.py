"""
Trace parsing module - extracts execution trace from logs
Supports new auto-trace format: [TRACE:module:line:timestamp:status] context
Also supports old format: [TRACE:module:line:timestamp] context (infers status)
"""

import time


# Status keywords for automatic inference (for backward compatibility)
ERROR_KEYWORDS = ["错误", "失败", "异常"]
WARNING_KEYWORDS = ["警告", "跳过", "未找到"]
SUCCESS_KEYWORDS = ["成功", "完成", "创建", "生成", "保存", 
                    "验证成功", "放置成功", "配置", "初始化"]


def infer_status_from_context(context):
    """
    Infer status from context keywords (for backward compatibility)
    
    Args:
        context: Context description string
        
    Returns:
        status: "success", "warning", "error", or "info"
    """
    if not context:
        return "info"
    
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


class TraceInfo:
    """Stores trace information"""
    def __init__(self):
        self.last_function = None
        self.last_trace_line = None
        self.last_checkpoint = None
        self.script_started = False
        self.script_error = False
        self.compilation_detected = False
        self.error_messages = []
        self.actors_created = 0
        self.expected_actors = 0
        self.materials_created = 0
        self.materials_failed = 0
        self.assets_loaded = 0
        self.assets_failed = 0
        self.progress_steps = {
            '[1/6]': False,
            '[2/6]': False,
            '[3/6]': False,
            '[4/6]': False,
            '[5/6]': False,
            '[6/6]': False
        }
        
        # New: module execution history (complete record)
        self.module_history = []  # Format: {'module': str, 'line': int, 'timestamp': int, 'context': str}
        self.current_module = None
        self.current_module_line = None
        self.start_time = None


def parse_line(line, trace_info):
    """Parse a single line and update trace info"""
    # Parse TRACE markers
    if 'LogPython' in line and '[TRACE:' in line:
        _parse_trace_marker(line, trace_info)
    
    # Detect script start
    if 'STARTING MAP GENERATOR' in line:
        trace_info.script_started = True
    
    # Detect compilation
    if 'Compiling' in line or 'Building' in line or 'Shader' in line:
        trace_info.compilation_detected = True
    
    # Detect script errors
    if 'LogPython' in line and ('ERROR' in line or 'Exception' in line):
        trace_info.script_error = True
        trace_info.error_messages.append(line.strip())
    
    # Track engine status
    _track_engine_status(line, trace_info)
    
    # Track progress steps
    if 'LogPython' in line:
        _track_progress(line, trace_info)
        _track_function(line, trace_info)
        _track_actors(line, trace_info)


def _parse_trace_marker(line, trace_info):
    """Parse TRACE marker from line (supports new format with status and old format)"""
    try:
        # New format: [TRACE:module:line:timestamp:status] context
        # Old format: [TRACE:module:line:timestamp] context (backward compatible)
        if '[TRACE:' in line and 'LogPython' in line:
            marker_start = line.find('[TRACE:')
            marker_end = line.find(']', marker_start)
            
            if marker_start != -1 and marker_end != -1:
                marker = line[marker_start+7:marker_end]  # Remove "[TRACE:"
                parts = marker.split(':')
                
                # Extract context (description after the marker)
                context = line[marker_end+1:].strip() if marker_end+1 < len(line) else ""
                
                if len(parts) >= 4:
                    # New format with status: [TRACE:module:line:timestamp:status]
                    module_name = parts[0]
                    line_num = int(parts[1])
                    timestamp_ms = int(parts[2])
                    status = parts[3]
                    
                elif len(parts) >= 3:
                    # Old format without status: [TRACE:module:line:timestamp]
                    # Infer status from context for backward compatibility
                    module_name = parts[0]
                    line_num = int(parts[1])
                    timestamp_ms = int(parts[2])
                    status = infer_status_from_context(context)
                    
                else:
                    # Invalid format, skip
                    return
                
                # Update current state
                trace_info.current_module = module_name
                trace_info.current_module_line = line_num
                trace_info.last_trace_line = line_num
                
                # Record history with status
                trace_info.module_history.append({
                    'module': module_name,
                    'line': line_num,
                    'timestamp': timestamp_ms,
                    'context': context,
                    'status': status  # New field
                })
                
                # Record start time (first record)
                if trace_info.start_time is None:
                    trace_info.start_time = timestamp_ms
        
        # Parse checkpoint: [CHECKPOINT:line:timestamp] name
        elif '[CHECKPOINT:' in line:
            marker_start = line.find('[CHECKPOINT:')
            marker_end = line.find(']', marker_start)
            
            if marker_start != -1 and marker_end != -1:
                marker = line[marker_start+12:marker_end]
                parts = marker.split(':')
                
                if len(parts) >= 2:
                    line_num = int(parts[0])
                    timestamp_ms = int(parts[1])
                    checkpoint_name = line[marker_end+1:].strip()
                    
                    trace_info.last_checkpoint = checkpoint_name
                    trace_info.last_trace_line = line_num
        
        # Legacy format support (for backward compatibility)
        elif '[TRACE:LINE:' in line:
            line_num_str = line.split('[TRACE:LINE:')[1].split(']')[0]
            trace_info.last_trace_line = int(line_num_str)
        
        elif '[TRACE:ENTER:' in line or '[TRACE:EXIT:' in line:
            if '[TRACE:ENTER:' in line:
                parts = line.split('[TRACE:ENTER:')[1].split(']')
            else:
                parts = line.split('[TRACE:EXIT:')[1].split(']')
            
            if len(parts) >= 2:
                trace_info.last_trace_line = int(parts[0])
                trace_info.last_function = parts[1].strip()
    except:
        pass


def _track_engine_status(line, trace_info):
    """Track UE5 engine status"""
    if 'LogAssetRegistry' in line and 'cache written' in line:
        trace_info.last_function = "UE5引擎 - 保存资产注册表缓存（脚本已完成）"
    elif 'LogContentValidation' in line and 'Starting to validate' in line:
        trace_info.last_function = "UE5引擎 - 验证资产（脚本已完成，正在清理）"
    elif 'LogRenderer' in line and 'Warning' in line:
        trace_info.last_function = "UE5引擎 - 渲染器警告（脚本已完成，正在退出）"


def _track_progress(line, trace_info):
    """Track progress steps"""
    for step in trace_info.progress_steps:
        if step in line:
            trace_info.progress_steps[step] = True


def _track_function(line, trace_info):
    """Track last executed function"""
    function_markers = {
        'Preparing level': "create_new_level() - 准备Level",
        'Map exists, loading': "create_new_level() - 加载现有地图",
        'Getting world reference': "create_new_level() - 获取World引用",
        'Map loaded, will regenerate': "create_new_level() - 地图加载完成",
        'Level ready': "create_new_level() - Level准备完成",
        'Creating training room': "place_training_room() - 开始创建训练室",
        'Loading cube mesh': "place_training_room() - 加载Cube网格",
        'Loading plane mesh': "place_training_room() - 加载Plane网格",
        'Training room geometry created': "place_training_room() - 训练室创建完成",
        'Placing PlayerStart': "place_player_start() - 放置PlayerStart",
        'PlayerStart placed': "place_player_start() - PlayerStart放置完成",
        'Setting up lighting': "setup_lighting() - 设置照明",
        'Lighting system configured': "setup_lighting() - 照明系统配置完成",
        'Configuring GameMode': "configure_game_mode() - 配置GameMode",
        'GameMode set to': "configure_game_mode() - GameMode设置完成",
        'Saving map': "save_map() - 保存地图",
        'Map saved successfully': "save_map() - 地图保存成功",
        'Map generation completed': "generate_map() - 地图生成完成",
        'STARTING MAP GENERATOR': "main() - 脚本启动"
    }
    
    for marker, function in function_markers.items():
        if marker in line:
            trace_info.last_function = function
            break


def _track_actors(line, trace_info):
    """Track actor creation, materials, and assets"""
    # Track actor creation - multiple formats
    if ('Created:' in line or 
        'Created transparent partition:' in line or
        'light created:' in line or  # Directional/Sky/Point light
        'PlayerStart placed' in line):
        trace_info.actors_created += 1
    
    if 'Total actors created:' in line:
        try:
            parts = line.split(':')
            if len(parts) >= 3:
                trace_info.expected_actors = int(parts[-1].strip())
        except:
            pass
    
    # Track material creation
    if 'Dynamic material created' in line or '动态材质创建成功' in line:
        trace_info.materials_created += 1
    
    if 'Failed to create dynamic material' in line or '创建动态材质失败' in line:
        trace_info.materials_failed += 1
    
    # Track asset loading
    if 'Asset loaded:' in line or '资源加载成功' in line:
        trace_info.assets_loaded += 1
    
    if 'Failed to load asset' in line or '资源加载失败' in line:
        trace_info.assets_failed += 1


# extract_detailed_trace() function removed - no longer needed!
# All trace information is now captured in real-time by _parse_trace_marker()
