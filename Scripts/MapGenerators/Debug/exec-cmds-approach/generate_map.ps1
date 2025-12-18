# Cosmos 002 Training World Map Generator - Fully Automated with Error Detection

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Cosmos 002 Training World Map Generator" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting automated map generation..." -ForegroundColor Yellow
Write-Host ""

# Configuration
$enginePath = "D:\UnrealEngine570\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$projectPath = "D:\001xm\shijiewuxian\shijiewuxian.uproject"
$scriptPath = "D:/001xm/shijiewuxian/Scripts/MapGenerators/run_generator.py"
$mapPath = "Content\Maps\Cosmos_002_Training_World.umap"
$timeoutSeconds = 180  # 3 minutes timeout

# Start process
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $enginePath
$psi.Arguments = "`"$projectPath`" -ExecCmds=`"py $scriptPath`" -stdout -unattended -nopause -nosplash -ddc=InstalledNoZenLocalFallback"
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $false

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi

# Event handlers for output
$foundSuccess = $false
$foundError = $false
$errorMessages = @()

$outputHandler = {
    param($sender, $e)
    $line = $e.Data
    if ($line) {
        # Check for success
        if ($line -match "SUCCESS|Map generation completed successfully") {
            $script:foundSuccess = $true
            Write-Host $line -ForegroundColor Green
        }
        # Check for errors
        elseif ($line -match "ERROR|Exception|Failed to load|Traceback") {
            $script:foundError = $true
            $script:errorMessages += $line
            Write-Host $line -ForegroundColor Red
        }
        # Check for important progress
        elseif ($line -match "\[1/6\]|\[2/6\]|\[3/6\]|\[4/6\]|\[5/6\]|\[6/6\]|STARTING MAP GENERATOR") {
            Write-Host $line -ForegroundColor Yellow
        }
        # Ignore Zen warnings
        elseif ($line -match "LogZenServiceInstance: Warning|LogHttp: Warning.*google.com") {
            # Silently ignore
        }
        # Show other important logs
        elseif ($line -match "LogPython:|LogInit:|LogWorld:") {
            Write-Host $line -ForegroundColor Gray
        }
    }
}

$process.add_OutputDataReceived($outputHandler)
$process.add_ErrorDataReceived($outputHandler)

# Start process
Write-Host "Launching Unreal Engine..." -ForegroundColor Cyan
$process.Start() | Out-Null
$process.BeginOutputReadLine()
$process.BeginErrorReadLine()

# Wait with timeout and error detection
$startTime = Get-Date
$checkInterval = 1000  # Check every second

while (-not $process.HasExited) {
    Start-Sleep -Milliseconds $checkInterval
    
    $elapsed = (Get-Date) - $startTime
    
    # Check for success
    if ($foundSuccess) {
        Write-Host ""
        Write-Host "SUCCESS detected! Waiting for process to finish..." -ForegroundColor Green
        $process.WaitForExit(10000)  # Wait up to 10 more seconds
        break
    }
    
    # Check for error
    if ($foundError) {
        Write-Host ""
        Write-Host "ERROR detected! Stopping process..." -ForegroundColor Red
        $process.Kill()
        break
    }
    
    # Check timeout
    if ($elapsed.TotalSeconds -gt $timeoutSeconds) {
        Write-Host ""
        Write-Host "TIMEOUT! Process took longer than $timeoutSeconds seconds." -ForegroundColor Red
        $process.Kill()
        break
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Execution Complete" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check results
if ($foundSuccess) {
    Write-Host "[SUCCESS] Map generation completed!" -ForegroundColor Green
    
    if (Test-Path $mapPath) {
        Write-Host "[SUCCESS] Map file created: $mapPath" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "[WARNING] Success reported but map file not found!" -ForegroundColor Yellow
        exit 1
    }
}
elseif ($foundError) {
    Write-Host "[ERROR] Map generation failed with errors:" -ForegroundColor Red
    foreach ($msg in $errorMessages) {
        Write-Host "  $msg" -ForegroundColor Red
    }
    exit 1
}
else {
    Write-Host "[UNKNOWN] Process ended without clear success or error." -ForegroundColor Yellow
    
    if (Test-Path $mapPath) {
        Write-Host "[INFO] Map file exists: $mapPath" -ForegroundColor Cyan
        exit 0
    } else {
        Write-Host "[ERROR] Map file not found: $mapPath" -ForegroundColor Red
        exit 1
    }
}
