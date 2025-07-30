# minaki_cli/wg_control.py
import subprocess, platform
from pathlib import Path

BINARIES = {
    "linux": "wireguard-go-linux",
    "darwin": "wireguard-go-macos",
    "windows": "wireguard-go.exe",
}

def start_wireguard(interface="wg0") -> subprocess.Popen:
    system = platform.system().lower()
    binary = Path(__file__).parent / "assets" / BINARIES.get(system, "")
    
    if not binary.exists():
        raise RuntimeError(f"WireGuard binary not found for {system}: {binary}")
    
    print(f"🚀 Launching embedded WireGuard for {system} using {binary}")
    proc = subprocess.Popen(
        ["sudo", str(binary), interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc
