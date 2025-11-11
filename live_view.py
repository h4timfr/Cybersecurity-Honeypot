import json
import time
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from datetime import datetime

LOG_FOLDER = "honeypot_logs"
console = Console()

def load_latest_log():
    """Find the most recent honeypot log file"""
    if not os.path.exists(LOG_FOLDER):
        return None
    files = [f for f in os.listdir(LOG_FOLDER) if f.startswith("honeypot_") and f.endswith(".json")]
    if not files:
        return None
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(LOG_FOLDER, x)))
    return os.path.join(LOG_FOLDER, latest_file)

def read_logs(log_path):
    """Read and return all logs from the honeypot log file"""
    try:
        with open(log_path, "r") as f:
            data = json.load(f)
            return data
    except Exception:
        return []

def make_dashboard(logs):
    """Create a live dashboard table from log data"""
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("No.", justify="right", style="bold")
    table.add_column("Time", style="dim")
    table.add_column("Remote IP", style="yellow")
    table.add_column("Port", justify="center", style="green")
    table.add_column("Data (First 40 chars)", style="white")

    # Add the 10 most recent logs
    for i, entry in enumerate(logs[-10:], start=1):
        t = entry.get("timestamp", "")
        ip = entry.get("remote_ip", "")
        port = str(entry.get("port", ""))
        data = entry.get("data", "").strip().replace("\n", " ")
        if len(data) > 40:
            data = data[:40] + "..."
        table.add_row(str(i), t, ip, port, data)

    stats_text = Text()
    stats_text.append(f"Total Logged Events: {len(logs)}\n", style="bold green")
    if logs:
        last_event_time = logs[-1].get("timestamp", "")
        stats_text.append(f"Last Event: {last_event_time}", style="cyan")
    else:
        stats_text.append("No events logged yet", style="red")

    panel = Panel.fit(stats_text, title="📊 Stats", border_style="magenta")
    layout = Table.grid(expand=True)
    layout.add_row(panel)
    layout.add_row(table)
    return layout

def main():
    console.clear()
    console.print("[bold magenta]🛡️ Live Honeypot Attack Dashboard[/bold magenta]\n")
    last_count = 0

    log_path = load_latest_log()
    if not log_path:
        console.print("[red]No log files found yet. Run main.py to start the honeypot.[/red]")
        return

    with Live(refresh_per_second=2) as live:
        while True:
            logs = read_logs(log_path)
            if len(logs) != last_count:
                dashboard = make_dashboard(logs)
                live.update(dashboard)
                last_count = len(logs)
            time.sleep(1)

if __name__ == "__main__":
    main()
