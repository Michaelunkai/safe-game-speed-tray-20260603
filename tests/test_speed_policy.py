from pathlib import Path
import subprocess
import sys

from game_speed_tray.speed_policy import read_state, write_state


def test_state_roundtrip(tmp_path: Path):
    p = tmp_path / "speed_state.json"
    write_state(p, 5)
    assert read_state(p).multiplier == 5


def test_demo_runs_about_5x(tmp_path: Path):
    p = tmp_path / "speed_state.json"
    write_state(p, 5)
    out = subprocess.check_output([
        sys.executable, "tools/demo_game.py", "--seconds", "0.8", "--state", str(p)
    ], text=True)
    ratio = float(out.strip().split("ratio=")[-1])
    assert 4.5 <= ratio <= 5.8, out
