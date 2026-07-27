cd "C:\Users\Carol\OmniRoute"
$TimeStamp = Get-Date -Format "yyyyMMdd_HHmmss"
if (Test-Path ".\config\models_cache.json") {
    Copy-Item -Path ".\config\models_cache.json" -Destination ".\config\models_cache_$TimeStamp.bak" -Force
    Write-Host "[BACKUP] Local configuration snapshot preserved safely." -ForegroundColor Green
}
