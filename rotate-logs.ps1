cd "C:\Users\Carol\OmniRoute"
$LogFile = ".\omniroute_runtime.log"
if (Test-Path $LogFile) {
    if ((Get-Item $LogFile).Length -gt 10MB) {
        Clear-Content $LogFile -ErrorAction SilentlyContinue
        Write-Host "[ENGINE] Runtime logs safely cleared to prevent storage leaks." -ForegroundColor Green
    }
}
