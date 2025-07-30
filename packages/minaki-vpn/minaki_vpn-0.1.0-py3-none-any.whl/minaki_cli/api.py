import requests
import platform
import subprocess
import shutil
import sys
from rich.console import Console
from .config import load
import logging

# Setup
API_BASE = "https://api.minaki.io/public/api/v1"
console = Console()
logging.basicConfig(level=logging.DEBUG)

class APIError(RuntimeError):
    """Custom error for API issues."""
    pass

def _key_header() -> dict[str, str]:
    """Load API key and return headers."""
    config = load()
    logging.debug(f"Loaded config: {config}")
    key = config.get("api_key")
    if not key:
        raise APIError("Missing API key. Run:  minaki configure --api-key <KEY>")
    return {"apikey": key}

def get_status() -> dict:
    """Query current VPN lease status."""
    r = requests.get(f"{API_BASE}/vpn/status", headers=_key_header(), timeout=15)
    logging.debug(f"Raw status response: {r.text}")
    if r.status_code == 404:
        raise APIError("No lease found for your user.")
    if not r.ok:
        raise APIError(f"Upstream error {r.status_code}: {r.text}")
    try:
        return r.json()
    except Exception as e:
        logging.error(f"JSON decode error: {e}")
        raise APIError("Invalid JSON response")

def download_config(path: str | None = None) -> str:
    """Download WireGuard config file and save it locally with a safe filename."""
    data = get_status()
    cfg_txt = data["config"]
    
    # Sanitize filename to work with wg-quick
    safe_ip = data["ip"].replace(".", "_")
    dest = path or f"minaki-{safe_ip}.conf"

    try:
        with open(dest, "w") as fp:
            fp.write(cfg_txt)
        console.print(f"✅  WireGuard config saved → [bold]{dest}[/bold]")
        return dest
    except Exception as e:
        logging.error(f"Failed to write config to {dest}: {e}")
        raise APIError(f"Failed to write config file: {e}")

def is_wireguard_installed() -> bool:
    """Check if WireGuard is installed."""
    return shutil.which("wg") is not None

def install_wireguard() -> None:
    """Attempt to install WireGuard based on detected OS."""
    sys_os = platform.system().lower()
    console.print(f"🔧 Installing WireGuard for [bold]{sys_os}[/bold]…")

    try:
        if sys_os == "linux":
            subprocess.check_call(["sudo", "apt-get", "update"])
            subprocess.check_call(["sudo", "apt-get", "install", "-y", "wireguard", "wireguard-tools"])
        elif sys_os == "darwin":
            subprocess.check_call(["brew", "install", "wireguard-tools"])
        elif sys_os == "windows":
            console.print("➡️  Download the official installer: https://www.wireguard.com/install/")
        else:
            console.print(":warning: Unsupported OS.")
    except subprocess.CalledProcessError as e:
        logging.error(f"WireGuard install failed: {e}")
        raise APIError(f"WireGuard installation failed: {e}")
