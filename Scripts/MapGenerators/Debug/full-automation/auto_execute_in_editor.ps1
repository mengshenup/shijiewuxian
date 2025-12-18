# PowerShell脚本：自动在UE5编辑器中执行Python代码
# 使用Windows UI Automation发送按键

param(
    [string]$PythonCode = @"
import sys
sys.path.append('D:/001xm/shijiewuxian/Scripts/MapGenerators')
import generate_cosmos_002_training_world
generate_cosmos_002_training_world.main()
"@
)

Write-Host "============================================================"
Write-Host "自动执行Python代码在UE5编辑器"
Write-Host "============================================================"
Write-Host ""

# 检查编辑器是否运行
$editor = Get-Process | Where-Object {$_.ProcessName -like "*UnrealEditor*"} | Select-Object -First 1

if (-not $editor) {
    Write-Host "错误: 未检测到运行中的UE5编辑器"
    exit 1
}

Write-Host "检测到编辑器 (PID: $($editor.Id))"
Write-Host ""

# 加载Windows Forms for SendKeys
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Runtime.WindowsRuntime

# 将代码复制到剪贴板
Set-Clipboard -Value $PythonCode
Write-Host "✓ Python代码已复制到剪贴板"
Write-Host ""

# 尝试激活编辑器窗口
Write-Host "尝试激活编辑器窗口..."
$signature = @'
[DllImport("user32.dll")]
public static extern bool SetForegroundWindow(IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
'@

$type = Add-Type -MemberDefinition $signature -Name Win32Utils -Namespace Win32Functions -PassThru
$type::ShowWindow($editor.MainWindowHandle, 9) # SW_RESTORE
$type::SetForegroundWindow($editor.MainWindowHandle)

Start-Sleep -Milliseconds 500

Write-Host "✓ 编辑器窗口已激活"
Write-Host ""

Write-Host "发送按键序列..."
Write-Host "1. 打开Output Log (Ctrl+Shift+O)"
[System.Windows.Forms.SendKeys]::SendWait("^+o")
Start-Sleep -Milliseconds 1000

Write-Host "2. 切换到Python标签 (模拟点击)"
# 注意: 这里无法自动切换标签，需要用户确保Python标签已打开

Write-Host "3. 粘贴代码 (Ctrl+V)"
[System.Windows.Forms.SendKeys]::SendWait("^v")
Start-Sleep -Milliseconds 500

Write-Host "4. 执行代码 (Enter)"
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

Write-Host ""
Write-Host "============================================================"
Write-Host "按键序列已发送"
Write-Host "============================================================"
Write-Host ""
Write-Host "注意: 此方法依赖于:"
Write-Host "1. Output Log窗口已打开"
Write-Host "2. Python标签已选中"
Write-Host "3. 焦点在Python输入框"
Write-Host ""
Write-Host "如果执行失败，请手动:"
Write-Host "1. 打开 Window -> Developer Tools -> Output Log"
Write-Host "2. 切换到 Python 标签"
Write-Host "3. 按 Ctrl+V 粘贴代码"
Write-Host "4. 按 Enter 执行"
Write-Host "============================================================"
