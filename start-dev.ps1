# Django Development Environment Startup Script
# This script navigates to the project directory and activates the virtual environment

# Set the project directory
$ProjectPath = "c:\Users\kjson\Documents\Dev\Sept\website"

# Check if the project directory exists
if (-not (Test-Path $ProjectPath)) {
    Write-Host "❌ Project directory not found: $ProjectPath" -ForegroundColor Red
    exit 1
}

# Navigate to the project directory
Write-Host "📁 Navigating to project directory..." -ForegroundColor Cyan
Set-Location $ProjectPath

# Check for virtual environment (common locations)
$VenvPaths = @(
    ".\venv\Scripts\Activate.ps1",
    ".\env\Scripts\Activate.ps1", 
    ".\.venv\Scripts\Activate.ps1",
    "..\.venv\Scripts\Activate.ps1",
    "..\venv\Scripts\Activate.ps1"
)

$VenvFound = $false
foreach ($VenvPath in $VenvPaths) {
    if (Test-Path $VenvPath) {
        Write-Host "🐍 Activating virtual environment: $VenvPath" -ForegroundColor Green
        & $VenvPath
        $VenvFound = $true
        break
    }
}

if (-not $VenvFound) {
    Write-Host "⚠️  Virtual environment not found. Checking for Python..." -ForegroundColor Yellow
    try {
        $PythonVersion = python --version 2>$null
        Write-Host "✅ Using system Python: $PythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    }
}

# Display current location and Python info
Write-Host "`n📍 Current location: $(Get-Location)" -ForegroundColor Cyan
Write-Host "🎯 Ready to work on Django project!" -ForegroundColor Green

# Optional: Show useful commands
Write-Host "`n🚀 Useful Django commands:" -ForegroundColor Yellow
Write-Host "   python manage.py runserver     # Start development server"
Write-Host "   python manage.py migrate       # Apply database migrations"
Write-Host "   python manage.py makemigrations # Create new migrations"
Write-Host "   python manage.py shell         # Open Django shell"
Write-Host "   python manage.py collectstatic # Collect static files"