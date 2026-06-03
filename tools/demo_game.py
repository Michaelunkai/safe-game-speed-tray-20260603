"""Tiny opt-in demo game loop used to prove 5x simulation speed.

It reads the speed_state.json written by the tray/controller. Real commercial
or online games generally do not expose such a safe opt-in control surface.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from game_speed_tray.speed_policy import read_state


def run(seconds: float, state: Path, tick_rate: float = 20.0) -> float:
    start = time.perf_counter()
    sim_time = 0.0
    last = start
    while time.perf_counter() - start < seconds:
        now = time.perf_counter()
        dt = now - last
        last = now
        multiplier = read_state(state).multiplier
        sim_time += dt * multiplier
        time.sleep(1.0 / tick_rate)
    return sim_time


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=2.0)
    ap.add_argument("--state", type=Path, required=True)
    args = ap.parse_args()
    sim = run(args.seconds, args.state)
    print(f"wall_seconds={args.seconds:.3f} simulated_seconds={sim:.3f} ratio={sim/args.seconds:.3f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
