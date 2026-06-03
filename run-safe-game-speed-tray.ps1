param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
if ($Args.Count -eq 0) { $Args = @('tray') }
& (Join-Path $Root 'scriptsun-safe-game-speed-tray.ps1') @Args
exit $LASTEXITCODE
