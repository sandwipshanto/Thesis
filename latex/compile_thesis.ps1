# Thesis Compilation Script
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Compiling Thesis" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# Clean previous build
Write-Host "Cleaning previous build artifacts..." -ForegroundColor Yellow

# Create build directory if it doesn't exist
if (-not (Test-Path "build")) {
    New-Item -ItemType Directory -Path "build" | Out-Null
}

Remove-Item *.aux,*.log,*.toc,*.lof,*.lot,*.bbl,*.blg,*.out,*.synctex.gz -ErrorAction SilentlyContinue
Remove-Item build\* -ErrorAction SilentlyContinue
Write-Host "Done!" -ForegroundColor Green
Write-Host ""

# First compilation
Write-Host "STEP 1/4: First pdfLaTeX compilation..." -ForegroundColor Yellow
$null = pdflatex -interaction=nonstopmode thesis.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: First compilation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Done!" -ForegroundColor Green
Write-Host ""

# BibTeX
Write-Host "STEP 2/4: Running BibTeX..." -ForegroundColor Yellow
$null = bibtex thesis
Write-Host "Done!" -ForegroundColor Green
Write-Host ""

# Second compilation
Write-Host "STEP 3/4: Second pdfLaTeX compilation..." -ForegroundColor Yellow
$null = pdflatex -interaction=nonstopmode thesis.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Second compilation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Done!" -ForegroundColor Green
Write-Host ""

# Third compilation
Write-Host "STEP 4/4: Third pdfLaTeX compilation..." -ForegroundColor Yellow
$null = pdflatex -interaction=nonstopmode thesis.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Third compilation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Done!" -ForegroundColor Green
Write-Host ""

# Move build artifacts to build folder
Write-Host "Moving build artifacts..." -ForegroundColor Yellow
$buildFiles = @("*.aux", "*.log", "*.out", "*.toc", "*.lof", "*.lot", "*.bbl", "*.blg", "*.synctex.gz")
foreach ($pattern in $buildFiles) {
    Get-Item $pattern -ErrorAction SilentlyContinue | Move-Item -Destination "build\" -Force
}
Write-Host "Done!" -ForegroundColor Green
Write-Host ""

# Check result
if (Test-Path "thesis.pdf") {
    $size = (Get-Item "thesis.pdf").Length / 1MB
    Write-Host "==================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! PDF generated: thesis.pdf" -ForegroundColor Green
    Write-Host "Size: $([math]::Round($size, 2)) MB" -ForegroundColor Green
    Write-Host "==================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Opening PDF..." -ForegroundColor Yellow
    Start-Process "thesis.pdf"
} else {
    Write-Host "ERROR: PDF was not generated!" -ForegroundColor Red
    Write-Host "Check thesis.log for details" -ForegroundColor Yellow
    exit 1
}
