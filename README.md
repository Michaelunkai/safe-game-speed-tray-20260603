# safe-game-speed-tray-20260603

Repository: https://github.com/Michaelunkai/safe-game-speed-tray-20260603

Safe Windows tray/CLI project for experimenting with game speed multipliers in **opt-in** games, demos, and tools that deliberately read a speed-state file.

## Important safety boundary

This project does **not** force arbitrary commercial, online, anti-cheat-protected, or closed-source games to run faster. Doing that reliably would require process injection, memory patching, API hooking, or anti-cheat bypass behavior that can break games, violate terms of service, or create malware-like tooling. Instead, this repository provides a safe tray/menu controller and a working opt-in demo proving 5x simulation speed.

## What it creates

- A Windows system tray app with right-click speed choices: 1x, 2x, 3x, 5x, 10x.
- A CLI controller to set/read the multiplier.
- A small demo game loop that reads the multiplier and runs its simulation at the selected speed.
- Tests that prove the demo runs at about 5x when 5x is selected.
- A best-effort process-priority helper for normal/high priority, which is not the same as true time acceleration.

## Prerequisites

- Windows 10/11.
- Python 3.9+ installed as `py` or `python`.
- For tray UI: `pystray` and `pillow` installed by `pip install -e .`.

## Setup

From this project folder:

```powershell
py -m pip install -e .
```

If `py` is unavailable:

```powershell
python -m pip install -e .
```

## Usage

Run the tray app from Windows PowerShell 5.1:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "F:\study\projects\software\windows\desktop\apps\gaming\utilities\time-control\safe-game-speed-tray-20260603\run-safe-game-speed-tray.ps1"
```

The launcher creates `.venv-win`, installs `pystray`, `pillow`, and `psutil` if missing, then opens the system tray icon. First run can take a minute while dependencies install.

Run from inside the project folder:

```powershell
.\run-safe-game-speed-tray.ps1
```

Set 5x from CLI:

```powershell
.un-safe-game-speed-tray.ps1 set 5
```

Return to normal:

```powershell
.un-safe-game-speed-tray.ps1 set 1
```

Check status:

```powershell
.un-safe-game-speed-tray.ps1 status
```

Run the included demo at 5x:

```powershell
.un-safe-game-speed-tray.ps1 set 5
py tools\demo_game.py --seconds 2 --state "$env:LOCALAPPDATA\SafeGameSpeedTray\speed_state.json"
```

## Inputs and outputs

- Input: chosen speed multiplier from tray or CLI.
- Output: `speed_state.json` in `%LOCALAPPDATA%\SafeGameSpeedTray\` on Windows.
- Opt-in games/tools can read this JSON and multiply their own simulation delta time.

## Important files

- `run-safe-game-speed-tray.ps1` — Windows-friendly entry point.
- `src/game_speed_tray/__main__.py` — CLI and tray menu.
- `src/game_speed_tray/speed_policy.py` — state file and safety policy.
- `tools/demo_game.py` — opt-in demo loop used for verification.
- `tests/test_speed_policy.py` — automated 5x proof.

## Testing

From the project root:

```powershell
py -m pip install -e . pytest
py -m pytest
```

Expected result: tests pass, including a demo ratio near 5x.

## Troubleshooting

- **Tray import error:** run `py -m pip install -e .` on Windows.
- **No arbitrary game changes:** expected. Closed-source games must expose a safe plugin/mod/API or be built to read the multiplier.
- **Anti-cheat warnings:** do not use injection or memory patching. This project intentionally avoids those techniques.
- **Priority helper does not speed up the game:** process priority can reduce scheduling contention, but it does not multiply game time.
