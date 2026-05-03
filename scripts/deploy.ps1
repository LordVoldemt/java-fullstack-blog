param(
  [string]$Message = "docs: update blog content"
)

$ErrorActionPreference = "Stop"

$pathsToStage = @(
  "docs",
  "README.md",
  "package.json",
  "package-lock.json",
  "scripts",
  ".github"
)

Write-Host "==> Building docs..."
npm.cmd run docs:build

Write-Host "==> Checking git status..."
$status = git status --short
if (-not $status) {
  Write-Host "No changes to commit."
  exit 0
}

Write-Host "==> Staging changes..."
git add -- $pathsToStage

Write-Host "==> Committing changes..."
$staged = git diff --cached --name-only
if (-not $staged) {
  Write-Host "No blog-related changes staged. Nothing to publish."
  exit 0
}

git commit -m $Message

Write-Host "==> Pushing to origin/main..."
git push origin main

Write-Host "Done. GitHub Actions will deploy the site to GitHub Pages."
