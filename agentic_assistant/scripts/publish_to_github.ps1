Param(
  [Parameter(Mandatory=$true)][string]$RepoName,
  [switch]$Private
)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Error "gh (GitHub CLI) not found. Install and run 'gh auth login' first."
  exit 1
}

git init 2>$null
git add .
try { git commit -m "chore: publish repository" } catch { }

$flag = $null
if ($Private) { $flag = "--private" } else { $flag = "--public" }

gh repo create "$RepoName" $flag --source=. --push
Write-Host "Repository published: $RepoName"
