param([string]$Message)
if ($env:DISCORD_WEBHOOK_URL) {
    $Body = @{ content = "[OmniRoute::wholelychit] $Message" } | ConvertTo-Json -Compress
    Invoke-RestMethod -Uri $env:DISCORD_WEBHOOK_URL -Method Post -Body $Body -ContentType "application/json" -ErrorAction SilentlyContinue
}
