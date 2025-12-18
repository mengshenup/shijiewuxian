"""
关键词分析工具
运行 UE5 地图生成器，收集所有日志，分析出现频率最高的关键词
"""

import subprocess
import sys
import re
from collections import Counter
from pathlib import Path

ENGINE_PATH = r"D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
PROJECT_PATH = r"D:\001xm\shijiewuxian\shijiewuxian.uproject"
SCRIPT_PATH = "D:/001xm/shijiewuxian/Scripts/MapGenerators/Tools/run_generator.py"

def collect_logs():
    """运行 UE5 并收集所有日志"""
    print("正在运行 UE5 并收集日志...")
    print("这可能需要几分钟...\n")
    
    cmd = [
        ENGINE_PATH,
        PROJECT_PATH,
        '-ExecCmds=py ' + SCRIPT_PATH,
        '-stdout',
        '-unattended',
        '-nopause',
        '-nosplash',
        '-ddc=InstalledNoZenLocalFallback',
        '-NoZenAutoLaunch'
    ]
    
    lines = []
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        
        for line in process.stdout:
            lines.append(line.rstrip())
            # 显示进度
            if len(lines) % 100 == 0:
                print(f"  已收集 {len(lines)} 行日志...")
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n用户中断")
        process.terminate()
    
    print(f"\n✓ 收集完成，共 {len(lines)} 行日志\n")
    return lines

def analyze_keywords(lines):
    """分析日志中的关键词"""
    print("="*60)
    print("关键词分析")
    print("="*60 + "\n")
    
    # 1. 统计常见英文单词
    word_counter = Counter()
    
    for line in lines:
        # 提取英文单词（3个字母以上）
        words = re.findall(r'\b[A-Z][a-z]{2,}\b', line)
        word_counter.update(words)
    
    print("Top 30 常见单词:")
    for word, count in word_counter.most_common(30):
        print(f"  {word:20s} : {count:4d} 次")
    
    # 2. 统计 Log 类别
    print("\n" + "="*60)
    print("Log 类别统计:")
    print("="*60 + "\n")
    
    log_categories = Counter()
    
    for line in lines:
        # 匹配 Log 类别：Log<Category>:
        match = re.search(r'Log(\w+):', line)
        if match:
            log_categories[match.group(1)] += 1
    
    for category, count in log_categories.most_common(20):
        print(f"  Log{category:20s} : {count:4d} 次")
    
    # 3. 统计关键操作
    print("\n" + "="*60)
    print("关键操作统计:")
    print("="*60 + "\n")
    
    operations = {
        'Compiling': 0,
        'Loading': 0,
        'Saving': 0,
        'Building': 0,
        'Shader': 0,
        'Material': 0,
        'Texture': 0,
        'Initializing': 0,
        'Processing': 0,
        'Generating': 0,
        'Creating': 0,
        'Spawning': 0,
        'ERROR': 0,
        'Warning': 0,
        'SUCCESS': 0,
    }
    
    for line in lines:
        for op in operations:
            if op in line:
                operations[op] += 1
    
    for op, count in sorted(operations.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {op:20s} : {count:4d} 次")
    
    # 4. Python 脚本相关
    print("\n" + "="*60)
    print("Python 脚本执行:")
    print("="*60 + "\n")
    
    python_lines = [line for line in lines if 'LogPython' in line or 'STARTING' in line or '[1/6]' in line]
    
    if python_lines:
        print(f"找到 {len(python_lines)} 行 Python 相关日志:\n")
        for line in python_lines[:20]:  # 显示前20行
            print(f"  {line[:100]}")
    else:
        print("未找到 Python 相关日志")
    
    # 5. 保存完整日志
    log_file = Path("Scripts/MapGenerators/Tools/ue5_full_log.txt")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\n✓ 完整日志已保存到: {log_file}")

def main():
    print("\n" + "="*60)
    print("  UE5 日志关键词分析工具")
    print("="*60 + "\n")
    
    # 收集日志
    lines = collect_logs()
    
    # 分析关键词
    analyze_keywords(lines)
    
    print("\n" + "="*60)
    print("分析完成！")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
