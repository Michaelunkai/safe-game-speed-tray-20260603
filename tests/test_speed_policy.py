from pathlib import Path
import subprocess
import sys

from game_speed_tray.speed_policy import read_state, write_state


def test_state_roundtrip(tmp_path: Path):
    p = tmp_path / "speed_state.json"
    write_state(p, 5)
    assert read_state(p).multiplier == 5
    write_state(p, 3)
    assert read_state(p).multiplier == 3


def test_all_supported_demo_speeds(tmp_path: Path):
    p = tmp_path / "speed_state.json"
    for speed in (1, 2, 3, 5, 10):
        write_state(p, speed)
        out = subprocess.check_output([
            sys.executable, "tools/demo_game.py", "--seconds", "0.65", "--state", str(p)
        ], text=True)
        ratio = float(out.strip().split("ratio=")[-1])
        assert speed * 0.82 <= ratio <= speed * 1.18, (speed, out)
