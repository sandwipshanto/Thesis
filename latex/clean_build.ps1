# Clean Build Artifacts Script
# Removes temporary LaTeX compilation files

Write-Host "🧹 Cleaning build artifacts..." -ForegroundColor Yellow
Write-Host ""

$filesToClean = @(
    "*.aux",
    "*.log", 
    "*.toc",
    "*.lof",
    "*.lot",
    "*.bbl",
    "*.blg",
    "*.out",
    "*.synctex.gz",
    "*.fdb_latexmk",
    "*.fls"
)

$cleaned = 0
foreach ($pattern in $filesToClean) {
    $files = Get-ChildItem -Path . -Filter $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        Write-Host "  Removing: $($file.Name)" -ForegroundColor Gray
        Remove-Item $file.FullName -Force
        $cleaned++
    }
}

Write-Host ""
if ($cleaned -gt 0) {
    Write-Host "✅ Cleaned $cleaned file(s)" -ForegroundColor Green
} else {
    Write-Host "✅ No files to clean" -ForegroundColor Green
}
Write-Host ""
Write-Host "Note: thesis.pdf was NOT removed" -ForegroundColor Cyan
Write-Host ""
