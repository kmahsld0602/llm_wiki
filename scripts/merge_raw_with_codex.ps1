param(
  [Parameter(Mandatory=$true)]
  [string]$MergeRequest
)

$Utf8NoBom = New-Object System.Text.UTF8Encoding $false
$OutputEncoding = $Utf8NoBom
[Console]::InputEncoding = $Utf8NoBom
[Console]::OutputEncoding = $Utf8NoBom
$env:PYTHONIOENCODING = 'utf-8'

$Root = Resolve-Path (Join-Path $PSScriptRoot '..')
$RequestPath = Resolve-Path $MergeRequest

Set-Location $Root

$prompt = @"
You are maintaining the ML Wiki repository.

Read this merge request:
$RequestPath

Then update the relevant Markdown page under wiki/ml.
Rules:
- Keep the Wiki concise.
- Preserve front matter.
- Add only content supported by the raw source.
- If the raw source does not fit any existing page, create a new page under wiki/ml.
- Add a short entry to wiki/log.md if the file exists.
- Reply in Korean with a brief summary of changed files.
"@

codex exec --skip-git-repo-check --sandbox workspace-write $prompt
