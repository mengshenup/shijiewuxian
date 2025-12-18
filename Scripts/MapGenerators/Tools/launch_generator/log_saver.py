"""
Log saving module - saves compressed and full logs
"""


def save_logs(monitor):
    """Save compressed summary and full logs to files"""
    # Save compressed summary
    if monitor.log_file:
        try:
            with open(monitor.log_file, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("  压缩摘要日志\n")
                f.write("="*60 + "\n\n")
                f.write('\n'.join(monitor.summary_log))
                f.write("\n")
            
            print(f"\n✓ 压缩摘要已保存到: {monitor.log_file}")
        except Exception as e:
            print(f"\n⚠ 保存压缩摘要失败: {e}")
    
    # Save full log
    if monitor.full_log_file:
        try:
            with open(monitor.full_log_file, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("  完整输出日志\n")
                f.write("="*60 + "\n\n")
                for line in monitor.lines:
                    f.write(line)
                f.write("\n")
            
            print(f"✓ 完整日志已保存到: {monitor.full_log_file}")
        except Exception as e:
            print(f"⚠ 保存完整日志失败: {e}")
