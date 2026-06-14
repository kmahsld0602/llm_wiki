param(
  [int]$PollSeconds = 2
)

$Utf8NoBom = New-Object System.Text.UTF8Encoding $false
$OutputEncoding = $Utf8NoBom
[Console]::InputEncoding = $Utf8NoBom
[Console]::OutputEncoding = $Utf8NoBom
$env:PYTHONIOENCODING = 'utf-8'

$Root = Resolve-Path (Join-Path $PSScriptRoot '..')
$Inbox = Join-Path $Root 'agent_messages\inbox'
$Outbox = Join-Path $Root 'agent_messages\outbox'
$Processed = Join-Path $Root 'agent_messages\processed'

New-Item -ItemType Directory -Force -Path $Inbox, $Outbox, $Processed | Out-Null

if (-not $env:WIKI_AGENT_CLI -and (Get-Command codex -ErrorAction SilentlyContinue)) {
  $env:WIKI_AGENT_CLI = 'codex exec --skip-git-repo-check --sandbox read-only "다음 UTF-8 파일의 지시를 읽고 최종 답변만 출력하세요: {prompt_file}"'
}

Write-Host "Watching $Inbox"
Write-Host "CLI bridge: $env:WIKI_AGENT_CLI"
Write-Host "Drop .txt or .json messages into inbox. Press Ctrl+C to stop."

while ($true) {
  Get-ChildItem -LiteralPath $Inbox -File -ErrorAction SilentlyContinue | ForEach-Object {
    $file = $_
    try {
      $raw = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
      if ($file.Extension -eq '.json') {
        $payload = $raw | ConvertFrom-Json
        $question = [string]$payload.question
      } else {
        $question = $raw.Trim()
      }

      if (-not $question) {
        throw "Message file has no question text."
      }

      $response = python (Join-Path $Root 'scripts\wiki_agent.py') $question
      $outFile = Join-Path $Outbox ($file.BaseName + '.response.json')
      $response | Set-Content -LiteralPath $outFile -Encoding UTF8
      Move-Item -LiteralPath $file.FullName -Destination (Join-Path $Processed $file.Name) -Force
      Write-Host "Processed $($file.Name) -> $outFile"
    } catch {
      $errorFile = Join-Path $Outbox ($file.BaseName + '.error.txt')
      $_.Exception.Message | Set-Content -LiteralPath $errorFile -Encoding UTF8
      Move-Item -LiteralPath $file.FullName -Destination (Join-Path $Processed $file.Name) -Force
      Write-Host "Failed $($file.Name) -> $errorFile"
    }
  }

  Start-Sleep -Seconds $PollSeconds
}
