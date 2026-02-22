# git-autopush.ps1
# ─────────────────────────────────────────────────────────────────────────────
# Run this from c:\django to instantly commit all changes and push to GitHub.
# Usage:  .\git-autopush.ps1
#         .\git-autopush.ps1 "Optional custom commit message"
# ─────────────────────────────────────────────────────────────────────────────

param(
    [string]$Message = ""
)

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

if ($Message -eq "") {
    $commitMsg = "Auto-push: $timestamp"
} else {
    $commitMsg = "$Message ($timestamp)"
}

Write-Host "`n🔍 Checking for changes..." -ForegroundColor Cyan

git add .

$status = git status --porcelain
if (-not $status) {
    Write-Host "✅ Nothing to commit — working tree is clean." -ForegroundColor Green
    exit 0
}

Write-Host "📦 Committing: $commitMsg" -ForegroundColor Yellow
git commit -m $commitMsg

Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Pushed successfully to GitHub!" -ForegroundColor Green
} else {
    Write-Host "❌ Push failed. Check your connection or token." -ForegroundColor Red
}
