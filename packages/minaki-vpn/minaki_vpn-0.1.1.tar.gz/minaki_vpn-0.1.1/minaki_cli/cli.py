import os
import click
import subprocess
import shutil
from pathlib import Path
from rich import print

from . import config as cfg, api
from .api import get_status, download_config
from .config import load as load_config

#CONFIG_NAME = "wg2.conf"
#CONFIG_PATH = Path.cwd() / CONFIG_NAM

CONFIG_DIR = Path.home() / ".minaki"
CONFIG_NAME = "wg2.conf"
CONFIG_PATH = CONFIG_DIR / CONFIG_NAME

@click.group()
def cli():
    """MinakiLabs VPN CLI."""


# ------------------ Configure ------------------
@cli.command("configure")
@click.option("--api-key", prompt=True, hide_input=True, help="Your Minaki API key")
def configure(api_key):
    """Save your API key locally (~/.minaki/cli-config.json)."""
    data = cfg.load()
    data["api_key"] = api_key.strip()
    cfg.save(data)
    print("✅ API key stored.")


# ------------------ Status ------------------
@cli.command("status")
def status():
    """Show your current lease status."""
    try:
        s = get_status()
    except api.APIError as e:
        print(f"[red]{e}[/red]")
        raise SystemExit(1)

    print(f"[bold cyan]IP:[/bold cyan] {s['ip']}   "
          f"[bold magenta]Public:[/bold magenta] {s['public_ip']}")
    print(f"Listen port: {s['listen_port']}")
    print("Config snippet:\n", s["config"].splitlines()[0:5], "…")


# ------------------ Pull Config ------------------
@cli.command("pull-config")
def pull_config_cmd():
    """Download your WireGuard .conf locally."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        download_config(CONFIG_PATH)
        print(f"✅ Config downloaded as [green]{CONFIG_PATH}[/green]")
    except api.APIError as e:
        print(f"[red]{e}[/red]")


# ------------------ Install WireGuard ------------------
@cli.command("install-wg")
def install_wg():
    """Attempt to install WireGuard & tools for your OS."""
    if shutil.which("wg-quick"):
        print("✅ WireGuard is already installed.")
    else:
        print("[red]❌ WireGuard tools not found. Please install manually.[/red]")


# ------------------ Connect ------------------
@cli.command()
def connect():
    """Pull WireGuard config and bring up VPN tunnel."""
    config = load_config()
    api_key = config.get("api_key") or os.environ.get("API_KEY")

    if not api_key:
        print("[red]❌ No API key found. Use 'configure' or set API_KEY env var.[/red]")
        return

    cfg.save({"api_key": api_key})

    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        download_config(CONFIG_PATH)
        print(f"✅ Config downloaded to [green]{CONFIG_PATH}[/green]")
        os.chmod(CONFIG_PATH, 0o600)
    except Exception as e:
        print(f"[red]❌ Failed to download config: {e}[/red]")
        return

    if not shutil.which("wg-quick"):
        print("[red]❌ wg-quick not found. Please install WireGuard first.[/red]")
        return

    print(f"🚀 Bringing up VPN using [bold]{CONFIG_NAME}[/bold]...")
    try:
        subprocess.run(["sudo", "wg-quick", "up", str(CONFIG_PATH)], check=True)
        print("[green]✅ VPN tunnel started with wg-quick.[/green]")
    except subprocess.CalledProcessError as e:
        print(f"[red]❌ wg-quick failed to start VPN: {e}[/red]")


# ------------------ Disconnect ------------------
@cli.command()
def disconnect():
    """Tear down the VPN tunnel."""
    print(f"🔌 Tearing down VPN tunnel...")

    try:
        result = subprocess.run(["ip", "link", "show", "wg2"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("[yellow]⚠️ Interface wg2 does not exist. Nothing to disconnect.[/yellow]")
            return
    except Exception as e:
        print(f"[red]❌ Failed to check interface: {e}[/red]")
        return

    try:
        subprocess.run(["sudo", "wg-quick", "down", str(CONFIG_PATH)], check=True)
        print("[green]✅ VPN tunnel stopped using wg-quick.[/green]")
    except subprocess.CalledProcessError as e:
        print(f"[red]❌ Failed to stop VPN: {e}[/red]")


# ------------------ Restart ------------------
@cli.command()
def restart():
    """Restart the VPN tunnel."""
    print("🔄 Restarting VPN tunnel...")
    try:
        disconnect()
    except Exception as e:
        print(f"[yellow]⚠️ Disconnect failed: {e}. Trying to reconnect anyway.[/yellow]")

    try:
        connect()
    except Exception as e:
        print(f"[red]❌ Failed to restart VPN tunnel: {e}[/red]")


if __name__ == "__main__":
    cli()
