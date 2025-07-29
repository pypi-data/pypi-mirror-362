# core.py

import subprocess
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from .config import BASE_PACKAGES

console = Console()

def get_installed_packages():
    """
    Retrieves a list of all installed packages.
    """
    try:
        result = subprocess.run(
            ['pip', 'list', '--format=freeze'],
            capture_output=True,
            text=True,
            check=True
        )
        # We only want the package name, not the version
        return [line.split('==')[0] for line in result.stdout.strip().split('\n') if line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[red]Error: Could not list installed packages. Is pip installed and in your PATH?[/red]")
        return []

def get_packages_to_uninstall(whitelist):
    """
    Determines which packages to uninstall based on the whitelist.
    """
    installed_packages = get_installed_packages()
    protected_packages = BASE_PACKAGES.union(set(whitelist))
    return [pkg for pkg in installed_packages if pkg not in protected_packages]

def uninstall_packages(packages, dry_run=False):
    """
    Uninstalls the given list of packages.
    """
    if not packages:
        console.print("[yellow]No user-installed packages to uninstall.[/yellow]")
        return

    table = Table(title="Packages to be Uninstalled")
    table.add_column("Package Name", style="cyan")

    for pkg in packages:
        table.add_row(pkg)

    console.print(table)

    if dry_run:
        console.print("\n[bold yellow]Dry run mode. No packages will be uninstalled.[/bold yellow]")
        return

    if not Confirm.ask("\n[bold red]Do you want to proceed with uninstallation?[/bold red]"):
        console.print("[yellow]Aborted.[/yellow]")
        return

    for pkg in packages:
        try:
            console.print(f"Uninstalling {pkg}...")
            subprocess.run(
                ['pip', 'uninstall', '-y', pkg],
                capture_output=True,
                text=True,
                check=True
            )
            console.print(f"[green]✔[/green] Uninstalled [bold]{pkg}[/bold] successfully.")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error uninstalling {pkg}: {e.stderr}[/red]")


# -------------------- NEW FUNCTION ADDED HERE --------------------

def restore_packages(backup_filepath):
    """
    Restores packages from a backup file created by PyWipe.
    """
    console.print(f"[bold blue]Attempting to restore packages from:[/] [cyan]{backup_filepath}[/cyan]")

    try:
        with open(backup_filepath, "r") as f:
            # Read all non-empty lines from the backup file
            packages_to_install = [line.strip() for line in f if line.strip()]

        if not packages_to_install:
            console.print("[yellow]Backup file is empty. Nothing to restore.[/yellow]")
            return

        console.print("\n[bold]The following packages will be installed:[/bold]")
        for pkg in packages_to_install:
            console.print(f" - {pkg}")

        if not Confirm.ask("\n[bold green]Do you want to proceed with installation?[/bold green]"):
            console.print("[yellow]Restore aborted.[/yellow]")
            return

        console.print("\n[bold]Starting installation...[/bold]")
        # We construct one single command to let pip resolve all dependencies at once
        install_command = ['pip', 'install'] + packages_to_install
        
        # We use subprocess.run but don't capture the output,
        # so the user can see pip's progress in real-time.
        process = subprocess.run(install_command, check=True)

        console.print("\n[green]✔[/green] [bold]Package restoration complete![/bold]")

    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] The backup file was not found at [cyan]{backup_filepath}[/cyan].")
    except subprocess.CalledProcessError:
        console.print(f"\n[bold red]Error:[/bold red] 'pip install' failed. Please check the output above for details.")
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred: {e}[/bold red]")