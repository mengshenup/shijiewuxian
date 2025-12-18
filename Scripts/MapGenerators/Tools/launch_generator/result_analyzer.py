"""
Result analysis module - analyzes generation results
"""

from datetime import datetime
from config import MAP_PATH
from trace_parser import infer_status_from_context


# Status icon mapping
STATUS_ICONS = {
    "success": "✅",
    "warning": "⚠️",
    "error": "❌",
    "info": "ℹ️"
}


def get_status_icon(status):
    """
    Get icon for status
    
    Args:
        status: Status string ("success", "warning", "error", "info")
        
    Returns:
        icon: Corresponding emoji icon, or empty string for invalid status
    """
    return STATUS_ICONS.get(status, "ℹ️")  # Default to info icon


def analyze_result(trace_info, old_size, old_mtime):
    """
    Analyze generation result
    
    Returns:
        tuple: (result_code, reason_message)
            result_code: 0=success, 1=failure, 2=needs_retry
            reason_message: detailed reason
    """
    map_exists = MAP_PATH.exists()
    
    if map_exists:
        # Success: map file generated
        _print_success_info(old_size, old_mtime)
        return (0, "地图生成成功")
    
    # Map not generated, analyze why
    if trace_info.script_error:
        # Python script error (should not retry)
        reason = "Python 脚本执行错误"
        if trace_info.error_messages:
            reason += f": {trace_info.error_messages[0][:100]}"
        return (1, reason)
    
    if not trace_info.script_started:
        # Script never started (should not retry)
        return (1, "Python 脚本未启动，可能是 UE5 启动失败")
    
    if trace_info.compilation_detected:
        # Script started, compilation detected, but map not generated (may need retry)
        return (2, "检测到资源编译活动，UE5 可能在编译完成前退出")
    
    # Other unknown error (should not retry)
    return (1, "未知错误：脚本启动但地图未生成，且无编译活动")


def _print_success_info(old_size, old_mtime):
    """Print success information with file size comparison"""
    stat = MAP_PATH.stat()
    new_size = stat.st_size
    new_mtime = stat.st_mtime
    
    print(f"\n✓ 成功: 地图文件已生成")
    print(f"  路径: {MAP_PATH}")
    
    # Show file size comparison
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
        
        # Show modification time comparison
        if old_mtime and new_mtime != old_mtime:
            print(f"  旧修改时间: {datetime.fromtimestamp(old_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  新修改时间: {datetime.fromtimestamp(new_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"  修改时间: {datetime.fromtimestamp(new_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        # First generation, no old file
        print(f"  文件大小: {new_size:,} bytes ({new_size/1024:.2f} KB)")
        print(f"  修改时间: {datetime.fromtimestamp(new_mtime).strftime('%Y-%m-%d %H:%M:%S')}")


def print_progress_stats(trace_info):
    """Print progress statistics"""
    completed_steps = sum(1 for completed in trace_info.progress_steps.values() if completed)
    total_steps = len(trace_info.progress_steps)
    step_progress = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
    print(f"\n构建进度:")
    print(f"  步骤完成: {completed_steps}/{total_steps} ({step_progress:.0f}%)")
    for step, completed in trace_info.progress_steps.items():
        status = "✓" if completed else "✗"
        print(f"    {status} {step}")
    
    # Actor creation stats
    if trace_info.expected_actors > 0:
        actor_progress = (trace_info.actors_created / trace_info.expected_actors * 100)
        print(f"  Actors创建: {trace_info.actors_created}/{trace_info.expected_actors} ({actor_progress:.0f}%)")
    else:
        print(f"  Actors创建: {trace_info.actors_created} (未知总数)")
    
    # Material creation stats (show below Actors)
    total_materials = trace_info.materials_created + trace_info.materials_failed
    if total_materials > 0:
        material_progress = (trace_info.materials_created / total_materials * 100)
        status_icon = "✓" if trace_info.materials_failed == 0 else "⚠"
        print(f"  {status_icon} 材质创建: {trace_info.materials_created}/{total_materials} ({material_progress:.0f}%)")
        if trace_info.materials_failed > 0:
            print(f"    ⚠ 失败: {trace_info.materials_failed} 个材质创建失败")
    
    # Asset loading stats
    total_assets = trace_info.assets_loaded + trace_info.assets_failed
    if total_assets > 0:
        asset_progress = (trace_info.assets_loaded / total_assets * 100)
        status_icon = "✓" if trace_info.assets_failed == 0 else "✗"
        print(f"  {status_icon} 资源加载: {trace_info.assets_loaded}/{total_assets} ({asset_progress:.0f}%)")
        if trace_info.assets_failed > 0:
            print(f"    ✗ 失败: {trace_info.assets_failed} 个资源加载失败")


def print_trace_info(trace_info):
    """Print trace information"""
    print(f"\n📍 执行追踪:")
    
    # Show current module
    if trace_info.current_module:
        print(f"  当前模块: {trace_info.current_module}.py")
        print(f"  模块行号: {trace_info.current_module_line}")
    
    # Show last checkpoint
    if trace_info.last_checkpoint:
        print(f"  最后检查点: {trace_info.last_checkpoint}")
    
    # Show last function (legacy)
    if trace_info.last_function:
        print(f"  最后函数: {trace_info.last_function}")
    
    # Show execution time
    if trace_info.module_history:
        last_entry = trace_info.module_history[-1]
        total_time_ms = last_entry['timestamp']
        total_time_s = total_time_ms / 1000.0
        print(f"  执行时间: {total_time_s:.3f}秒")
    
    # Show module execution history
    print_trace_history(trace_info)


def print_trace_history(trace_info):
    """Print module execution history (beautiful format with status column)"""
    if not trace_info.module_history:
        print(f"\n  📜 模块执行历史: (无)")
        return
    
    history = trace_info.module_history
    total_count = len(history)
    
    print(f"\n  📜 模块执行历史（共 {total_count} 条，按执行顺序）:")
    print(f"      {'序号':<4}  {'模块':<20}  {'行号':<6}  {'说明':<25}  {'状态':<6}  {'耗时':<10}  {'总共':<10}")
    print(f"      {'─'*105}")
    
    for i, entry in enumerate(history, 1):
        module = entry['module'] + '.py'
        line = f"L{entry['line']}"
        timestamp = entry['timestamp']
        context = entry.get('context', '')  # Get description
        
        # Get status (with backward compatibility)
        if 'status' in entry and entry['status']:
            status = entry['status']
        else:
            # Infer status from context for backward compatibility
            status = infer_status_from_context(context)
        
        # Get status icon
        status_icon = get_status_icon(status)
        
        # Calculate elapsed time (difference from previous step)
        if i == 1:
            elapsed = 0
        else:
            elapsed = timestamp - history[i-2]['timestamp']
        
        print(f"      {i:3d}.  {module:<20}  {line:<6}  {context:<25}  {status_icon:<6}  {elapsed:6d}ms  {timestamp:8d}ms")
    
    # Performance analysis: find slowest 3 steps
    if len(history) > 1:
        # Calculate time for each step
        steps_with_time = []
        for i in range(1, len(history)):
            elapsed = history[i]['timestamp'] - history[i-1]['timestamp']
            steps_with_time.append({
                'module': history[i]['module'],
                'line': history[i]['line'],
                'elapsed': elapsed,
                'context': history[i]['context']
            })
        
        # Sort to find slowest 3
        slowest = sorted(steps_with_time, key=lambda x: x['elapsed'], reverse=True)[:3]
        
        print(f"\n  ⏱️  性能分析:")
        print(f"      最慢的3个步骤:")
        for i, step in enumerate(slowest, 1):
            context = f"({step['context']})" if step['context'] else ""
            print(f"        {i}. {step['module']}.py:L{step['line']} → {step['elapsed']}ms {context}")
