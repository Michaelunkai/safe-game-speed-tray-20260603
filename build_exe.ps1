param()
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $Root
$PythonExe = Join-Path $Root '.venv-win\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $PythonExe)) {
    & py -3 -m venv (Join-Path $Root '.venv-win')
}
& $PythonExe -m pip install --disable-pip-version-check --upgrade pyinstaller pystray pillow psutil
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$Build = Join-Path $Root 'build'
$Spec = Join-Path $Root 'SafeGameSpeedTray.spec'
$Exe = Join-Path $Root 'dist\SafeGameSpeedTray.exe'
if (Test-Path -LiteralPath $Build) { Remove-Item -LiteralPath $Build -Recurse -Force }
if (Test-Path -LiteralPath $Spec) { Remove-Item -LiteralPath $Spec -Force }
if (Test-Path -LiteralPath $Exe) {
    Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq $Exe } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 2
    Remove-Item -LiteralPath $Exe -Force
}
& $PythonExe -m PyInstaller --clean --noconsole --onefile --name SafeGameSpeedTray --paths (Join-Path $Root 'src') --collect-all pystray --collect-all PIL (Join-Path $Root 'src\game_speed_tray\__main__.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if (-not (Test-Path -LiteralPath $Exe)) { throw "Missing EXE: $Exe" }
Get-Item -LiteralPath $Exe | Select-Object FullName,Length,LastWriteTime
