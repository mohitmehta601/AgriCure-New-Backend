# Start AgriCure Backend Server
Write-Host "🚀 Starting AgriCure Backend Server..." -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location "P:\Latest AgriCure\Backend"

# Check if MongoDB is running
$mongoService = Get-Service -Name MongoDB -ErrorAction SilentlyContinue
if ($mongoService -and $mongoService.Status -eq 'Running') {
    Write-Host "✅ MongoDB is running" -ForegroundColor Green
} else {
    Write-Host "⚠️  MongoDB service not found or not running" -ForegroundColor Yellow
    Write-Host "   Please start MongoDB first" -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "📝 Starting Node.js server..." -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server (this will keep running)
node src/server.js

# This line will only execute if server stops
Write-Host ""
Write-Host "⚠️  Server stopped" -ForegroundColor Yellow
pause
