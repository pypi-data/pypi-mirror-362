# cdock Package Structure

## Overview
This document describes the Python package structure for cdock, designed for uvx distribution and modular orchestration capabilities.

## Package Layout

```
cdock/
├── pyproject.toml              # uv package configuration
├── README.md                   # Package documentation
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore patterns
├── src/
│   └── cdock/
│       ├── __init__.py         # Package initialization
│       ├── cli.py              # Click-based CLI interface
│       ├── docker.py           # Docker container management
│       ├── config.py           # Configuration handling
│       ├── hooks.py            # Security hook management
│       ├── utils.py            # Utility functions
│       ├── constants.py        # Constants and defaults
│       │
│       ├── orchestration/      # Phase 2: Orchestration features
│       │   ├── __init__.py
│       │   ├── github.py       # GitHub API integration
│       │   ├── state.py        # State management
│       │   ├── orchestrator.py # Orchestration logic
│       │   └── safety.py       # Agent safety mechanisms
│       │
│       └── templates/          # Configuration templates
│           ├── settings.json   # Claude settings template
│           ├── claude.md       # Task instruction template
│           └── hooks/
│               └── orchestrator-security-hook.sh
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_docker.py
│   ├── test_config.py
│   ├── test_hooks.py
│   └── orchestration/
│       ├── __init__.py
│       ├── test_github.py
│       ├── test_state.py
│       └── test_orchestrator.py
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── DEV_NOTES.md
│   ├── PYTHON_CONVERSION_PLAN.md
│   ├── GITHUB_INTEGRATION_PLAN.md
│   └── PACKAGE_STRUCTURE.md
└── legacy/
    ├── cdock                   # Original bash script
    ├── Dockerfile              # Docker image definition
    ├── entrypoint.sh           # Container entrypoint
    └── orchestrator-security-hook.sh
```

## Package Configuration

### pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "cdock"
dynamic = ["version"]
description = "Docker-based Claude Code runner with orchestration support"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "click>=8.0",
    "rich>=13.0",
    "docker>=6.0",
    "pyyaml>=6.0",
    "jinja2>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]
github = [
    "pygithub>=1.59",
    "gql[all]>=3.4",
    "python-dotenv>=1.0",
]
all = [
    "cdock[github]",
]

[project.urls]
Homepage = "https://github.com/yourusername/cdock"
Repository = "https://github.com/yourusername/cdock"
Documentation = "https://github.com/yourusername/cdock/docs"
Issues = "https://github.com/yourusername/cdock/issues"

[project.scripts]
cdock = "cdock.cli:cli"

[tool.hatch.version]
path = "src/cdock/__init__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/cdock"]

[tool.black]
line-length = 88
target-version = ["py38"]
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.ruff]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=cdock --cov-report=term-missing --cov-report=html"
```

## Module Organization

### Core Modules (Phase 1)

#### src/cdock/__init__.py
```python
"""cdock - Docker-based Claude Code runner with orchestration support"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .cli import cli
from .config import Config
from .docker import DockerManager

__all__ = ["cli", "Config", "DockerManager"]
```

#### src/cdock/cli.py
```python
"""Click-based CLI interface for cdock"""

import click
from rich.console import Console

from .config import Config
from .docker import DockerManager
from .hooks import HookManager
from .utils import check_prerequisites

console = Console()

@click.group()
@click.version_option()
@click.option('--config', type=click.Path(), help='Configuration file path')
@click.pass_context
def cli(ctx, config):
    """cdock - Docker-based Claude Code runner with orchestration support"""
    ctx.ensure_object(dict)
    
    # Load configuration
    ctx.obj['config'] = Config.load(config)
    
    # Initialize managers
    ctx.obj['docker'] = DockerManager(ctx.obj['config'])
    ctx.obj['hooks'] = HookManager(ctx.obj['config'])
    
    # Check prerequisites
    check_prerequisites()

@cli.command()
@click.argument('args', nargs=-1)
@click.pass_context
def run(ctx, args):
    """Run Claude Code in container"""
    docker_manager = ctx.obj['docker']
    docker_manager.run_container(args)

@cli.command()
@click.argument('args', nargs=-1)
@click.pass_context
def bash(ctx, args):
    """Open interactive bash shell"""
    docker_manager = ctx.obj['docker']
    docker_manager.run_container(['bash'] + list(args))

@cli.command()
@click.pass_context
def init(ctx):
    """Initialize repository for orchestration"""
    hooks_manager = ctx.obj['hooks']
    hooks_manager.init_orchestration()

@cli.command()
@click.option('--all', is_flag=True, help='Clean all cdock volumes')
@click.pass_context
def clean(ctx, all):
    """Clean local project volumes"""
    docker_manager = ctx.obj['docker']
    docker_manager.clean_volumes(all_volumes=all)

@cli.command()
@click.pass_context
def nuke(ctx):
    """Remove all volumes and images"""
    docker_manager = ctx.obj['docker']
    docker_manager.nuke_everything()

if __name__ == '__main__':
    cli()
```

#### src/cdock/config.py
```python
"""Configuration management for cdock"""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Config:
    """cdock configuration"""
    
    # Docker settings
    docker_image: str = "claude-code"
    docker_timeout: int = 120
    
    # SSH settings
    default_ssh_key: Path = field(default_factory=lambda: Path.home() / ".ssh" / "cdock")
    
    # GitHub settings (Phase 2)
    github_token: Optional[str] = None
    github_repo: Optional[str] = None
    
    # Orchestration settings (Phase 2)
    max_attempts: int = 3
    task_timeout: int = 1800  # 30 minutes
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """Load configuration from file and environment variables"""
        config = cls()
        
        # Load from config file
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = Path.home() / ".cdock.yaml"
            
        if config_file.exists():
            config._load_from_file(config_file)
        
        # Override with environment variables
        config._load_from_env()
        
        return config
    
    def _load_from_file(self, config_file: Path) -> None:
        """Load configuration from YAML file"""
        with open(config_file) as f:
            file_config = yaml.safe_load(f) or {}
        
        for key, value in file_config.items():
            if hasattr(self, key):
                if key == 'default_ssh_key':
                    setattr(self, key, Path(value))
                else:
                    setattr(self, key, value)
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables"""
        if ssh_key := os.getenv("CDOCK_SSH_KEY"):
            self.default_ssh_key = Path(ssh_key)
        
        if docker_image := os.getenv("CDOCK_DOCKER_IMAGE"):
            self.docker_image = docker_image
        
        if github_token := os.getenv("GITHUB_TOKEN"):
            self.github_token = github_token
        
        if github_repo := os.getenv("GITHUB_REPO"):
            self.github_repo = github_repo
    
    def save(self, config_path: Optional[str] = None) -> None:
        """Save configuration to file"""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = Path.home() / ".cdock.yaml"
        
        config_data = {
            'docker_image': self.docker_image,
            'docker_timeout': self.docker_timeout,
            'default_ssh_key': str(self.default_ssh_key),
            'max_attempts': self.max_attempts,
            'task_timeout': self.task_timeout,
        }
        
        # Don't save sensitive data like tokens
        config_file.parent.mkdir(exist_ok=True)
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)
```

#### src/cdock/constants.py
```python
"""Constants and defaults for cdock"""

# Docker configuration
DEFAULT_DOCKER_IMAGE = "claude-code"
DEFAULT_DOCKER_TIMEOUT = 120

# Volume naming
VOLUME_PREFIX = "claude-venv"
GLOBAL_CACHE_VOLUME = "uv-global-cache"
AUTH_VOLUME = "claude-home-auth"

# SSH configuration
DEFAULT_SSH_KEY_NAME = "cdock"

# Orchestration configuration
DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_TASK_TIMEOUT = 1800  # 30 minutes
DEFAULT_STAGE_TIMEOUT = 3600  # 1 hour

# GitHub configuration
GITHUB_LABEL_PREFIX = "cdock"
GITHUB_TASK_LABEL = "cdock-task"
GITHUB_HELP_LABEL = "cdock-help"

# File paths
CDOCK_DIR = ".cdock"
STATE_FILE = "state.json"
CLAUDE_INSTRUCTIONS = "CLAUDE.md"
SETTINGS_FILE = "settings.json"

# Dangerous directories
DANGEROUS_DIRS = [
    "/",
    "/root",
    "/home",
    "/usr",
    "/var",
    "/etc",
    "/bin",
    "/sbin",
]
```

### Orchestration Modules (Phase 2)

#### src/cdock/orchestration/__init__.py
```python
"""Orchestration functionality for cdock"""

from .github import GitHubClient, GitHubConfig
from .state import WorktreeState
from .orchestrator import Orchestrator
from .safety import AgentSafetyManager

__all__ = ["GitHubClient", "GitHubConfig", "WorktreeState", "Orchestrator", "AgentSafetyManager"]
```

#### src/cdock/orchestration/state.py
```python
"""State management for orchestration"""

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class WorktreeState:
    """State tracking for individual worktree"""
    
    worktree_id: str
    task_uuid: str
    short_uuid: str
    branch: str
    status: str
    github: Dict[str, Any]
    attempts: Dict[str, Any]
    timing: Dict[str, Any]
    created_at: str
    updated_at: str
    
    def save(self, path: Optional[Path] = None) -> None:
        """Save state to file"""
        if path is None:
            path = Path(".cdock/state.json")
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, path: Optional[Path] = None) -> "WorktreeState":
        """Load state from file"""
        if path is None:
            path = Path(".cdock/state.json")
        
        if not path.exists():
            raise FileNotFoundError(f"State file not found: {path}")
        
        with open(path) as f:
            data = json.load(f)
        
        return cls(**data)
    
    def update_status(self, status: str) -> None:
        """Update status and timestamp"""
        self.status = status
        self.updated_at = datetime.now().isoformat()
        self.save()
    
    @classmethod
    def create(cls, worktree_name: str, task_uuid: str, 
               branch: str = None) -> "WorktreeState":
        """Create new worktree state"""
        if branch is None:
            branch = f"feature/{worktree_name}"
        
        timestamp = datetime.now()
        
        return cls(
            worktree_id=f"{worktree_name}-{timestamp.strftime('%Y%m%d')}",
            task_uuid=task_uuid,
            short_uuid=task_uuid[:7],
            branch=branch,
            status="created",
            github={
                "issue_number": None,
                "pr_number": None,
                "labels": [],
                "project_item_id": None
            },
            attempts={
                "current": 0,
                "max": 3,
                "last_error": None,
                "error_hash": None
            },
            timing={
                "started_at": None,
                "max_duration": 1800,
                "timeout_at": None
            },
            created_at=timestamp.isoformat(),
            updated_at=timestamp.isoformat()
        )
```

## Templates

### src/cdock/templates/claude.md
```markdown
# {{ task_title }}

## Task Description
{{ task_description }}

## GitHub Integration
- Issue: #{{ github_issue }}
- Labels: {{ github_labels }}
- Project: {{ github_project }}

## Instructions
{{ instructions }}

## Success Criteria
{{ success_criteria }}

## Notes
- Update GitHub issue with progress
- Push commits regularly for visibility
- Create help request if stuck for more than {{ max_attempts }} attempts
- Task timeout: {{ task_timeout }} minutes
```

### src/cdock/templates/settings.json
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "{{ hook_path }}/orchestrator-security-hook.sh"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "{{ hook_path }}/orchestrator-security-hook.sh"
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "{{ hook_path }}/orchestrator-security-hook.sh"
          }
        ]
      }
    ]
  }
}
```

## Testing Structure

### tests/test_cli.py
```python
"""Tests for CLI interface"""

import pytest
from click.testing import CliRunner

from cdock.cli import cli

class TestCLI:
    def test_help(self):
        """Test help command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'cdock' in result.output
    
    def test_version(self):
        """Test version command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
    
    def test_run_command(self):
        """Test run command"""
        # Mock Docker to avoid actual container runs
        pass
    
    def test_bash_command(self):
        """Test bash command"""
        pass
    
    def test_init_command(self):
        """Test init command"""
        pass
    
    def test_clean_command(self):
        """Test clean command"""
        pass
    
    def test_nuke_command(self):
        """Test nuke command"""
        pass
```

## Distribution

### uvx Installation
```bash
# Install from PyPI
uvx cdock

# Install from git
uvx --from git+https://github.com/yourusername/cdock.git cdock

# Install local development version
uvx --from . cdock
```

### Development Installation
```bash
# Clone repository
git clone https://github.com/yourusername/cdock.git
cd cdock

# Install in development mode
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run black src tests
uv run ruff src tests
uv run mypy src

# Build package
uv build

# Test local installation
uv tool install -e .
```

## Maintenance

### Version Management
- Version is managed in `src/cdock/__init__.py`
- Use semantic versioning (semver)
- Update version for each release

### Dependencies
- Keep dependencies minimal for core functionality
- Use optional dependencies for GitHub integration
- Pin major versions, allow minor/patch updates

### Testing
- Maintain >80% test coverage
- Test on multiple Python versions (3.8-3.12)
- Test on multiple platforms (Linux, macOS, Windows)
- Integration tests with real Docker containers

This package structure provides a solid foundation for both the Python conversion (Phase 1) and the orchestration features (Phase 2) while maintaining clean separation of concerns and excellent maintainability.