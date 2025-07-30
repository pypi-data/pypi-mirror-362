import click
from rich.console import Console
from .manager import CDockManager

console = Console()
manager = CDockManager()

@click.group()
@click.version_option()
def cli():
    """cdock - Docker-based Claude Code runner"""
    pass

@cli.command()
@click.argument('args', nargs=-1)
def run(args):
    """Run Claude Code in container (default command)"""
    manager.run_container(list(args))

@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def bash(args):
    """Open interactive bash shell"""
    manager.run_container(['bash'] + list(args))

@cli.command()
def init():
    """Setup worktree folder, .gitignore, CLAUDE.md notes"""
    from .project import init_project
    init_project()

@cli.command()
@click.option('--all', is_flag=True, help='Clean all cdock volumes system-wide')
@click.option('--force', is_flag=True, help='Force remove volumes by stopping containers')
def clean(all, force):
    """Clean project scope volumes"""
    manager.clean_volumes(all_volumes=all, force=force)

@cli.command()
@click.option('--force', is_flag=True, help='Force complete rebuild without cache')
@click.option('--check', is_flag=True, help='Check if upgrade is needed without building')
def upgrade(force, check):
    """Rebuild Docker image (uses cache by default)"""
    if check:
        needs_upgrade = manager.needs_upgrade()
        if needs_upgrade:
            console.print("[yellow]📦 Upgrade needed[/yellow]")
        else:
            console.print("[green]✅ Image is up to date[/green]")
    else:
        manager.upgrade(force_rebuild=force)

if __name__ == '__main__':
    cli()