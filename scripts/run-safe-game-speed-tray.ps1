param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
if (-not $Root) { $Root = (Get-Location).Path }
Set-Location -LiteralPath $Root

function Get-ProjectPython {
    $venvPython = Join-Path $Root '.venv-win\Scripts\python.exe'
    if (Test-Path -LiteralPath $venvPython) {
        return $venvPython
    }

    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        Write-Host 'Creating project Windows Python environment (.venv-win)...'
        & py -3 -m venv (Join-Path $Root '.venv-win')
    } else {
        $python = Get-Command python -ErrorAction SilentlyContinue
        if (-not $python) { throw 'Python was not found. Install Python 3, then run this launcher again.' }
        if ($python.Source -like '*\Microsoft\WindowsApps\python.exe') { throw 'Only the Microsoft Store Python alias was found. Install real Python 3 or enable py.exe.' }
        Write-Host 'Creating project Windows Python environment (.venv-win)...'
        & $python.Source -m venv (Join-Path $Root '.venv-win')
    }

    if (-not (Test-Path -LiteralPath $venvPython)) { throw "Failed to create venv python: $venvPython" }
    return $venvPython
}

$PythonExe = Get-ProjectPython

# Run from source so first launch does not hang on editable installs on F:.
$SourcePath = Join-Path $Root 'src'
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = $SourcePath + ';' + $env:PYTHONPATH
} else {
    $env:PYTHONPATH = $SourcePath
}

# Make the tray app self-starting on clean Windows: install/update only external deps.
# Temporarily relax ErrorActionPreference so PowerShell 5 does not turn native
# stderr from Python into a terminating NativeCommandError during the probe.
$needsInstall = $false
$oldErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = 'SilentlyContinue'
& $PythonExe -c "import pystray, PIL, psutil" >$null 2>$null
$probeExitCode = $LASTEXITCODE
$ErrorActionPreference = $oldErrorActionPreference
if ($probeExitCode -ne 0) { $needsInstall = $true }

if ($needsInstall) {
    Write-Host 'Installing/updating tray dependencies for this project...'
    & $PythonExe -m pip install --disable-pip-version-check pystray pillow psutil
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if (-not $RemainingArgs -or $RemainingArgs.Count -eq 0) {
    $RemainingArgs = @('tray')
}

& $PythonExe -m game_speed_tray @RemainingArgs
exit $LASTEXITCODE
