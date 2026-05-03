param(
  [string]$Message = "docs: update blog content"
)

$ErrorActionPreference = "Stop"

Write-Host "==> Building docs..."
npm.cmd run docs:build

Write-Host "==> Checking git status..."
$status = git status --short
if (-not $status) {
  Write-Host "No changes to commit."
  exit 0
}

Write-Host "==> Staging changes..."
git add .

Write-Host "==> Committing changes..."
git commit -m $Message

Write-Host "==> Pushing to origin/main..."
git push origin main

Write-Host "Done. GitHub Actions will deploy the site to GitHub Pages."
