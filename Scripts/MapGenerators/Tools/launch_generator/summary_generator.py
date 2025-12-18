"""
Summary generation module - creates compressed summaries
"""

from datetime import datetime


def get_new_lines_summary(monitor):
    """Get compressed summary of new lines since last check"""
    new_lines = monitor.lines[monitor.last_summarized_index:]
    if not new_lines:
        return None
    
    # Update index
    monitor.last_summarized_index = len(monitor.lines)
    
    # Extract keywords and count
    keyword_counts = {}
    important_messages = []
    error_details = []
    
    for line in new_lines:
        # Count keywords
        _count_keywords(line, keyword_counts)
        
        # Extract important messages
        _extract_important_messages(line, important_messages)
        
        # Extract error details
        if 'ERROR' in line or 'Failed' in line or 'Error' in line:
            keyword_counts['错误'] = keyword_counts.get('错误', 0) + 1
            error_msg = line.strip()[:150]
            if error_msg not in error_details:
                error_details.append(error_msg)
    
    # Build summary
    summary_lines = []
    
    # 1. Important messages
    if important_messages:
        summary_lines.append('  ' + ' | '.join(important_messages))
    
    # 2. Keyword counts
    if keyword_counts:
        parts = _format_keyword_counts(keyword_counts)
        if parts:
            summary_lines.append('  ' + ' '.join(parts))
    
    # 3. Error details
    if error_details:
        for error in error_details[:3]:
            summary_lines.append(f"  ✗ {error}")
    
    # 4. Fallback
    if not summary_lines:
        summary_lines.append(f"  {len(new_lines)}行日志")
    
    result = '\n'.join(summary_lines)
    
    # Save to summary log
    if result:
        monitor.summary_log.append(f"[{datetime.now().strftime('%H:%M:%S')}]")
        monitor.summary_log.append(result)
    
    return result


def _count_keywords(line, counts):
    """Count keywords in line"""
    keywords = {
        '编译': ['Compiling', 'LogShaderCompilers'],
        '着色器': ['Shader', 'Shading'],
        '加载': ['Loading', 'Loaded', 'LogStreaming'],
        '保存': ['Saving', 'Saved'],
        '构建': ['Building', 'Build'],
        '材质': ['Material'],
        '纹理': ['Texture'],
        '音频': ['Audio', 'LogAudio'],
        '初始化': ['Initializing', 'Initialize'],
        '挂载': ['Mounted', 'Pak', 'LogPakFile'],
        '处理': ['Processing', 'Generating', 'Creating'],
        '注册': ['Registered', 'Register'],
        '插件': ['Plugin'],
        '动画': ['Animation', 'Anim'],
        '配置': ['Config', 'LogConfig'],
        '网络': ['Messaging', 'Network'],
        '警告': ['Warning'],
        '刷新': ['Flushing', 'Flush'],
        '元数据': ['Metadata'],
        '设备': ['Device', 'Driver']
    }
    
    for keyword, patterns in keywords.items():
        if any(pattern in line for pattern in patterns):
            counts[keyword] = counts.get(keyword, 0) + 1


def _extract_important_messages(line, messages):
    """Extract important messages from line"""
    if 'SUCCESS' in line:
        messages.append('✓成功')
    elif 'ERROR' in line and 'LogPython' in line:
        messages.append('✗错误')
    elif 'STARTING MAP GENERATOR' in line:
        messages.append('✓脚本启动')
    elif '[1/6]' in line:
        messages.append('✓准备Level')
    elif '[2/6]' in line:
        messages.append('✓放置TrainingRoom')
    elif '[3/6]' in line:
        messages.append('✓放置PlayerStart')
    elif '[4/6]' in line:
        messages.append('✓设置照明')
    elif '[5/6]' in line:
        messages.append('✓配置GameMode')
    elif '[6/6]' in line:
        messages.append('✓保存地图')


def _format_keyword_counts(counts):
    """Format keyword counts into display parts"""
    high_priority = []
    medium_priority = []
    low_priority = []
    
    for keyword, count in counts.items():
        display = f"{keyword}×{count}" if count > 1 else keyword
        
        if keyword in ['错误', '警告']:
            high_priority.append(display)
        elif keyword in ['编译', '着色器', '加载', '保存', '构建']:
            medium_priority.append(display)
        else:
            low_priority.append(display)
    
    parts = []
    if high_priority:
        parts.append('⚠ ' + ' | '.join(high_priority))
    if medium_priority:
        parts.append(' | '.join(medium_priority))
    if low_priority and len(low_priority) <= 5:
        parts.append(' | '.join(low_priority[:5]))
    
    return parts


def get_compressed_summary(monitor):
    """Get final compressed summary"""
    summary = []
    
    # Basic stats
    total_lines = len(monitor.lines)
    elapsed = monitor.get_elapsed_time()
    summary.append(f"执行时间: {elapsed:.1f}秒")
    summary.append(f"总输出行数: {total_lines}")
    
    # Analyze key steps
    steps_completed = []
    errors = []
    
    for line in monitor.lines:
        # Detect steps
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
        
        # Detect errors
        if 'ERROR' in line or 'Exception' in line or 'Failed to load' in line:
            if 'LogPython' in line or 'TrainingRoom' in line or 'PlayerStart' in line:
                errors.append(line.strip())
    
    # Output steps
    if steps_completed:
        summary.append(f"\n完成步骤 ({len(steps_completed)}):")
        for step in steps_completed:
            summary.append(f"  {step}")
    
    # Output errors
    if errors:
        summary.append(f"\n检测到错误 ({len(errors)}):")
        for error in errors[:5]:
            summary.append(f"  {error[:100]}")
    
    result = "\n".join(summary)
    
    # Save to summary log
    monitor.summary_log.append("\n" + "="*60)
    monitor.summary_log.append("  执行摘要 (压缩)")
    monitor.summary_log.append("="*60)
    monitor.summary_log.append(result)
    monitor.summary_log.append("="*60)
    
    return result
