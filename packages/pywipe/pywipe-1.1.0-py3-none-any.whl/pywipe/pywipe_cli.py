# pywipe_cli.py

import click
from rich.console import Console
from . import core, backup, utils

console = Console()

@click.group()
def cli():
    """
    PyWipe: The 'Factory Reset' for your Global Python Environment.
    
    A command-line tool to safely clean your global Python environment
    by uninstalling user-installed packages, or restoring them from a backup.
    """
    if utils.is_in_virtualenv():
        console.print("[bold red]Error:[/bold red] PyWipe is designed to clean the global Python environment and should not be run inside a virtual environment.")
        raise click.Abort()

@cli.command()
@click.option('--keep', '-k', multiple=True, help="A package to whitelist and not uninstall.")
@click.option('--dry-run', is_flag=True, help="Show what would be uninstalled without actually doing it.")
def run(keep, dry_run):
    """
    Identifies and uninstalls all user-installed packages.
    """
    console.print("[bold blue]PyWipe: Starting the cleanup process.[/bold blue]")

    if not dry_run:
        if not backup.create_backup():
            console.print("[bold red]Aborting due to backup failure.[/bold red]")
            return

    packages_to_uninstall = core.get_packages_to_uninstall(keep)
    core.uninstall_packages(packages_to_uninstall, dry_run)

    console.print("\n[bold green]PyWipe cleanup process complete.[/bold green]")


# -------------------- NEW COMMAND ADDED HERE --------------------

@cli.command()
@click.option(
    '--from',
    'backup_file',
    required=True,
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to the pywipe_backup_*.txt file to restore from."
)
def restore(backup_file):
    """
    Restores packages from a backup file.
    """
    console.print("[bold blue]PyWipe: Starting the restore process.[/bold blue]")
    core.restore_packages(backup_file)


if __name__ == '__main__':
    cli()