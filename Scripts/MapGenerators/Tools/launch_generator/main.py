"""
Main entry point for launch generator
"""

import sys
import time
from config import MAP_NAME, SCRIPT_PATH, UE5_MAP_NAME, MAX_ATTEMPTS, RETRY_DELAY, MAP_PATH, LOG_FILE, FULL_LOG_FILE
from path_setup import setup_paths
from process_runner import run_generation_attempt


def main():
    """Main function - entry point"""
    # Setup paths
    if not setup_paths():
        return 1
    
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
    
    attempt = 1
    retry_count = 0
    
    while attempt <= MAX_ATTEMPTS:
        print(f"\n{'='*60}")
        if attempt == 1:
            print(f"  首次尝试")
        else:
            print(f"  重试 {retry_count}/{MAX_ATTEMPTS - 1}")
        print(f"{'='*60}\n")
        
        # Get old file info
        old_size = 0
        old_mtime = None
        if MAP_PATH.exists():
            old_stat = MAP_PATH.stat()
            old_size = old_stat.st_size
            old_mtime = old_stat.st_mtime
        
        # Run attempt
        result, reason = run_generation_attempt(
            attempt,
            LOG_FILE,
            FULL_LOG_FILE,
            old_size,
            old_mtime
        )
        
        if result == 0:
            # Success
            print(f"\n{'='*60}")
            print(f"✓ 地图生成成功！")
            if retry_count > 0:
                print(f"  (经过 {retry_count} 次重试)")
            print(f"{'='*60}")
            return 0
        
        elif result == 2:
            # Needs retry (compilation not complete)
            if attempt >= MAX_ATTEMPTS:
                print(f"\n{'='*60}")
                print(f"✗ 达到最大重试次数 ({MAX_ATTEMPTS})，放弃")
                print(f"  原因: {reason}")
                print(f"  建议: 在编辑器中手动运行脚本")
                print(f"{'='*60}")
                return 1
            
            print(f"\n⚠ 需要重试")
            print(f"  原因: {reason}")
            print(f"  等待 {RETRY_DELAY} 秒后重试...")
            attempt += 1
            retry_count += 1
            time.sleep(RETRY_DELAY)
        
        else:
            # Real error (should not retry)
            print(f"\n{'='*60}")
            print(f"✗ 生成失败 (错误码: {result})")
            print(f"  原因: {reason}")
            print(f"  这不是编译问题，重试无效")
            print(f"{'='*60}")
            return result
    
    # Should not reach here
    print(f"\n✗ 未知错误")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
