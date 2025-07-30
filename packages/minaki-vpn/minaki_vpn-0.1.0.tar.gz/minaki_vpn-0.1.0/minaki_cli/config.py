from __future__ import annotations
import json, os, pathlib, typing as t
from rich.console import Console

CONFIG_PATH = pathlib.Path.home() / ".minaki" / "cli-config.json"
console = Console()

def _ensure_dir() -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

def load() -> dict[str, t.Any]:
    """Load config or return empty dict if file missing/invalid."""
    try:
        with CONFIG_PATH.open() as fp:
            return json.load(fp)
    except Exception:
        return {}

def save(cfg: dict[str, t.Any]) -> None:
    _ensure_dir()
    with CONFIG_PATH.open("w") as fp:
        json.dump(cfg, fp, indent=2)
    console.print(f"💾  Saved config → {CONFIG_PATH}")
