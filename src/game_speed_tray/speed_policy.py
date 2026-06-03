"""Safe speed multiplier policy.

This module intentionally does not inject DLLs, patch memory, bypass anti-cheat,
or alter closed-source games. It controls an opt-in state file that cooperative
apps/demos can read, and it can optionally raise/lower Windows process priority.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path

VALID_MULTIPLIERS = (1, 2, 3, 5, 10)


@dataclass
class SpeedState:
    multiplier: float = 1.0
    updated_at: float = 0.0
    mode: str = "normal"
    safety_note: str = (
        "Opt-in only: no memory patching, DLL injection, anti-cheat bypass, "
        "or forced closed-source game time scaling."
    )


def default_state_path() -> Path:
    base = Path.home() / "AppData" / "Local" / "SafeGameSpeedTray" if Path.home().drive else Path.cwd()
    return base / "speed_state.json"


def validate_multiplier(value: float) -> float:
    value = float(value)
    if value not in VALID_MULTIPLIERS:
        raise ValueError(f"Unsupported multiplier {value}. Choose one of {VALID_MULTIPLIERS}.")
    return value


def write_state(path: Path, multiplier: float) -> SpeedState:
    multiplier = validate_multiplier(multiplier)
    state = SpeedState(multiplier=multiplier, updated_at=time.time(), mode="normal" if multiplier == 1 else "faster")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")
    return state


def read_state(path: Path) -> SpeedState:
    if not path.exists():
        return SpeedState(multiplier=1.0, updated_at=0.0)
    data = json.loads(path.read_text(encoding="utf-8"))
    return SpeedState(**data)


def try_set_priority(process_name_contains: str, high: bool = True) -> list[str]:
    """Best-effort Windows priority helper; never required for speed scaling."""
    changed: list[str] = []
    try:
        import psutil
    except Exception:
        return changed
    needle = process_name_contains.lower()
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = (proc.info.get("name") or "").lower()
            if needle and needle not in name:
                continue
            if high and hasattr(psutil, "HIGH_PRIORITY_CLASS"):
                proc.nice(psutil.HIGH_PRIORITY_CLASS)
            elif hasattr(psutil, "NORMAL_PRIORITY_CLASS"):
                proc.nice(psutil.NORMAL_PRIORITY_CLASS)
            changed.append(f"{proc.info.get('name')}[{proc.info.get('pid')}]")
        except Exception:
            continue
    return changed
