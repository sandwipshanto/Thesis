# LaTeX Installation Script for Windows
# This script installs MiKTeX (LaTeX distribution for Windows)

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  LaTeX Installation for Thesis Compilation" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  WARNING: Not running as Administrator" -ForegroundColor Yellow
    Write-Host "   Some installations may require admin privileges." -ForegroundColor Yellow
    Write-Host ""
}

# Check if Chocolatey is installed
Write-Host "Checking for Chocolatey package manager..." -ForegroundColor Green
$chocoInstalled = Get-Command choco -ErrorAction SilentlyContinue

if (-not $chocoInstalled) {
    Write-Host "❌ Chocolatey not found. Installing Chocolatey..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Installing Chocolatey requires Administrator privileges." -ForegroundColor Yellow
    Write-Host "Please run this command in an Administrator PowerShell:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "After installing Chocolatey, run this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host "ALTERNATIVE: Manual Installation" -ForegroundColor Cyan
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Option 1: Install MiKTeX manually" -ForegroundColor Green
    Write-Host "  1. Visit: https://miktex.org/download" -ForegroundColor White
    Write-Host "  2. Download 'Basic MiKTeX Installer'" -ForegroundColor White
    Write-Host "  3. Run installer and follow prompts" -ForegroundColor White
    Write-Host "  4. Choose 'Install missing packages on-the-fly: Yes'" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 2: Install TeX Live (larger but complete)" -ForegroundColor Green
    Write-Host "  1. Visit: https://www.tug.org/texlive/windows.html" -ForegroundColor White
    Write-Host "  2. Download install-tl-windows.exe" -ForegroundColor White
    Write-Host "  3. Run installer (takes 1-2 hours, ~7GB)" -ForegroundColor White
    Write-Host ""
    exit
}

Write-Host "✅ Chocolatey found!" -ForegroundColor Green
Write-Host ""

# Check if MiKTeX is installed
Write-Host "Checking for MiKTeX..." -ForegroundColor Green
$miktexInstalled = Get-Command pdflatex -ErrorAction SilentlyContinue

if ($miktexInstalled) {
    Write-Host "✅ MiKTeX already installed!" -ForegroundColor Green
    pdflatex --version | Select-Object -First 1
    Write-Host ""
    Write-Host "You're ready to compile your thesis!" -ForegroundColor Green
    Write-Host "Run: .\compile_thesis.ps1" -ForegroundColor Cyan
} else {
    Write-Host "❌ MiKTeX not found. Installing..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This will install MiKTeX (may take 10-20 minutes)..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        choco install miktex -y
        
        Write-Host ""
        Write-Host "==================================================================" -ForegroundColor Green
        Write-Host "✅ MiKTeX installed successfully!" -ForegroundColor Green
        Write-Host "==================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "IMPORTANT: You may need to:" -ForegroundColor Yellow
        Write-Host "  1. Close and reopen PowerShell" -ForegroundColor White
        Write-Host "  2. Or refresh your PATH by running:" -ForegroundColor White
        Write-Host "     `$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Then run: .\compile_thesis.ps1" -ForegroundColor Cyan
        Write-Host ""
    } catch {
        Write-Host "❌ Installation failed: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install manually from: https://miktex.org/download" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
