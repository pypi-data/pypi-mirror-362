# backup.py

import subprocess
import datetime
from rich.console import Console

console = Console()

def create_backup():
    """
    Saves the list of currently installed packages to a backup file.
    """
    try:
        result = subprocess.run(
            ['pip', 'freeze'],
            capture_output=True,
            text=True,
            check=True
        )
        backup_filename = f"pywipe_backup_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.txt"
        with open(backup_filename, "w") as f:
            f.write(result.stdout)
        console.print(f"[green]✔[/green] Successfully backed up installed packages to [bold]{backup_filename}[/bold].")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        console.print(f"[red]Error creating backup: {e}[/red]")
        return False