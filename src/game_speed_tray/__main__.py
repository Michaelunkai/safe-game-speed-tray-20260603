from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from .speed_policy import default_state_path, read_state, try_set_priority, write_state
except ImportError:  # PyInstaller may execute this file as a top-level script.
    from game_speed_tray.speed_policy import default_state_path, read_state, try_set_priority, write_state


def run_tray(state_path: Path) -> int:
    try:
        import pystray
        from PIL import Image, ImageDraw
    except Exception as exc:
        print("Tray dependencies are not installed. Run: py -m pip install -e .", file=sys.stderr)
        print(f"Import error: {exc}", file=sys.stderr)
        return 2

    def make_icon():
        img = Image.new("RGB", (64, 64), "#122033")
        draw = ImageDraw.Draw(img)
        draw.ellipse((8, 8, 56, 56), fill="#31d158")
        draw.text((22, 23), "x", fill="black")
        return img

    def set_speed(multiplier: float):
        def _inner(icon, item):
            write_state(state_path, multiplier)
            icon.title = f"Safe speed: {multiplier:g}x"
        return _inner

    current = read_state(state_path)
    if not state_path.exists():
        current = write_state(state_path, current.multiplier)

    menu = pystray.Menu(
        pystray.MenuItem("Normal 1x", set_speed(1)),
        pystray.MenuItem("2x (opt-in apps)", set_speed(2)),
        pystray.MenuItem("3x (opt-in apps)", set_speed(3)),
        pystray.MenuItem("5x (opt-in apps)", set_speed(5)),
        pystray.MenuItem("10x (opt-in apps)", set_speed(10)),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", lambda icon, item: icon.stop()),
    )
    icon = pystray.Icon("SafeGameSpeedTray", make_icon(), f"Safe speed: {current.multiplier:g}x", menu)
    icon.run()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe opt-in game speed tray/controller")
    parser.add_argument("--state", type=Path, default=default_state_path(), help="Path to speed_state.json")
    sub = parser.add_subparsers(dest="cmd")

    setp = sub.add_parser("set", help="Set opt-in speed multiplier")
    setp.add_argument("multiplier", type=float, choices=[1, 2, 3, 5, 10])

    sub.add_parser("status", help="Print current multiplier")
    sub.add_parser("tray", help="Run Windows system tray UI")

    pr = sub.add_parser("priority", help="Best-effort set matching process priority only")
    pr.add_argument("name_contains")
    pr.add_argument("--normal", action="store_true")

    args = parser.parse_args(argv)
    if args.cmd is None and getattr(sys, "frozen", False):
        return run_tray(args.state)
    if args.cmd == "set":
        state = write_state(args.state, args.multiplier)
        print(f"set multiplier={state.multiplier:g}x state={args.state}")
        return 0
    if args.cmd == "status" or args.cmd is None:
        state = read_state(args.state)
        print(f"multiplier={state.multiplier:g}x state={args.state}")
        return 0
    if args.cmd == "tray":
        return run_tray(args.state)
    if args.cmd == "priority":
        changed = try_set_priority(args.name_contains, high=not args.normal)
        print("changed=" + (", ".join(changed) if changed else "none"))
        return 0
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
