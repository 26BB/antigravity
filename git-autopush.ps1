# git-autopush.ps1
param(
    [string]$Message = ""
)

$date = Get-Date -Format "yyyy-MM-dd HH:mm"
if ([string]::IsNullOrWhiteSpace($Message)) {
    $commitMsg = "Auto-push: $date"
}
else {
    $commitMsg = "$Message ($date)"
}

Write-Host "🔍 Checking for changes..."
git add .
$status = git status --porcelain
if (-not $status) {
    Write-Host "✅ No changes to push."
    exit 0
}

Write-Host "📦 Committing: $commitMsg"
git commit -m "$commitMsg"

Write-Host "🚀 Pushing..."
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success!"
}
else {
    Write-Host "❌ Failed."
}
