$ErrorActionPreference = "SilentlyContinue"
Write-Host "[WATCHDOG] Active health monitoring initialized for wholelychit." -ForegroundColor Green

while ($true) {
    try {
        $Response = Invoke-WebRequest -Uri "http://localhost:20128" -Method Head -TimeoutSec 2 -UseBasicParsing
    } catch {
        Write-Warning "[WATCHDOG] Port 20128 drop detected. Forcing high-priority hot-reload..."
        Stop-Process -Name "node" -Force
        Start-Process -FilePath "npm" -ArgumentList "run start" -NoNewWindow
        Start-Sleep -Seconds 5
    }
    Start-Sleep -Seconds 10
}
