param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Root) { $Root = (Get-Location).Path }
Set-Location -LiteralPath $Root

if (-not $RemainingArgs -or $RemainingArgs.Count -eq 0) {
    $RemainingArgs = @('tray')
}

& (Join-Path $Root 'scripts\run-safe-game-speed-tray.ps1') @RemainingArgs
exit $LASTEXITCODE
