from pathlib import Path
from rich.console import Console

console = Console()

def init_project():
    """Setup worktree folder, .gitignore, cdock.md notes"""
    console.print("Initializing repository for cdock...")
    
    # Create worktrees directory
    worktrees_dir = Path("worktrees")
    worktrees_dir.mkdir(exist_ok=True)
    console.print("[green]✅ Created worktrees/ directory[/green]")
    
    # Add to .gitignore if not already there
    gitignore_path = Path(".gitignore")
    worktrees_entry = "worktrees/"
    
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text()
        if worktrees_entry not in gitignore_content:
            with gitignore_path.open("a") as f:
                f.write(f"\n{worktrees_entry}\n")
            console.print("[green]✅ Added worktrees/ to .gitignore[/green]")
        else:
            console.print("[yellow]worktrees/ already in .gitignore[/yellow]")
    else:
        gitignore_path.write_text(f"{worktrees_entry}\n")
        console.print("[green]✅ Created .gitignore with worktrees/[/green]")
    
    # Create cdock.md with usage notes
    cdock_md_path = Path("cdock.md")
    if not cdock_md_path.exists():
        cdock_md_content = """# cdock Development Notes

## Usage

Use `cdock` to run Claude Code in a containerized environment:

```bash
# Run Claude Code
cdock

# Open interactive shell
cdock bash

# Clean project volumes
cdock clean

# Clean all cdock volumes system-wide
cdock clean --all

# Force image rebuild
cdock upgrade
```

## Worktrees

The `worktrees/` directory is for git worktrees to work on multiple branches simultaneously.
"""
        cdock_md_path.write_text(cdock_md_content)
        console.print("[green]✅ Created cdock.md with usage notes[/green]")
    else:
        console.print("[yellow]cdock.md already exists[/yellow]")
    
    console.print("")
    console.print("[green]✅ Repository initialized for cdock![/green]")