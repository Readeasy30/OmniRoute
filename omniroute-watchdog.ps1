```powershell
# [CHECKPOINT: WATCHDOG_INITIALIZATION | Status: COMPLETED | State: PRESERVED]
\$ErrorActionPreference = "SilentlyContinue"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "[WATCHDOG] Active container health monitoring initialized for wholelychit." -ForegroundColor Green
Write-Host "[WATCHDOG] Target Endpoint: http://localhost:20128" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

while (\$true) {
    try {
        # Check container availability locally
        \$Response = Invoke-WebRequest -Uri "http://localhost:20128" -Method Head -TimeoutSec 2 -UseBasicParsing
        
        # Also confirm container container status reporting via engine daemon
        \$ContainerStatus = docker inspect --format='{{.State.Running}}' omniroute_gateway
        
        if (\$ContainerStatus -ne "true") { throw "Container daemon reports unhealthy state." }
    } 
    catch {
        Write-Warning "[WATCHDOG] Port 20128 drop or daemon fault detected. Initiating immediate engine hot-reload..."
        
        # Force high-priority orchestration restoration
        docker compose restart omniroute
        
        # Log event checkpoint
        Write-Host "[WATCHDOG] [CHECKPOINT: HOT_RELOAD_EXECUTED | Status: COMPLETED | State: PRESERVED]" -ForegroundColor Yellow
        Start-Sleep -Seconds 8
    }
    Start-Sleep -Seconds 10
}
```

---
