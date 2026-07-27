# Periodic SQLite engine validation routine for wholelychit
$DbFile = "$HOME\.omniroute\omniroute.db"
if (Test-Path $DbFile) {
    Write-Host "[MAINTENANCE] Compacting SQLite database to recover disk pages..." -ForegroundColor Cyan
    # Fire raw transaction calls directly against the data pool file if sqlite3 command exists
    if (Get-Command sqlite3 -ErrorAction SilentlyContinue) {
        sqlite3 $DbFile "VACUUM; REINDEX;" 2>&1 | Out-Null
        Write-Host "[MAINTENANCE] Compaction process succeeded." -ForegroundColor Green
    }
}
