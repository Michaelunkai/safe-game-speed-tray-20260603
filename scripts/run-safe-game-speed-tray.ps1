param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
if (-not $Root) { $Root = (Get-Location).Path }
Set-Location $Root
$Py = Get-Command py -ErrorAction SilentlyContinue
if ($Py) {
    & py -m game_speed_tray @Args
} else {
    & python -m game_speed_tray @Args
}
exit $LASTEXITCODE
