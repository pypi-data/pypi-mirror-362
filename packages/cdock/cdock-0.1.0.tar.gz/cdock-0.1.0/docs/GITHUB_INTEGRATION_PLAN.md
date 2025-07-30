# GitHub Integration Plan - Phase 2

## Overview
Add GitHub integration to the Python cdock for orchestration workflows. This builds on the Python foundation from Phase 1 to enable multi-agent coordination through GitHub Projects and Issues.

## Goals
- **GitHub Projects integration**: Visual kanban boards for task management
- **Issues as communication**: Agent-human coordination through GitHub Issues
- **Label-based portability**: Source of truth that works with any system
- **Progressive pushing**: Real-time visibility into agent progress
- **Agent safety**: Timeout, retry, and help request mechanisms

## Architecture

### Mixed API Strategy
- **GitHub Issues**: REST API (PyGithub) - stable, well-documented, Gitea-compatible
- **GitHub Projects**: GraphQL API (gql library) - required for new Projects
- **Labels as source of truth**: Ensures portability to other systems
- **Progressive fallback**: GitHub → local files → manual coordination

### ID System
- **Format**: `cdock.{worktree}.{7-char-uuid}`
- **Examples**: `cdock.auth-system.a7b2c8d`, `cdock.logging.f1e9a3b`
- **Collision scope**: Only check against open issues in same worktree
- **Full UUID**: Stored in issue body for audit trail

## Implementation Plan

### Phase 2.1: GitHub Issues Integration

#### Dependencies
```toml
[project.optional-dependencies]
github = [
    "pygithub>=1.59",       # GitHub REST API
    "gql[all]>=3.4",        # GraphQL client for Projects
    "python-dotenv>=1.0",   # Environment variable loading
]
```

#### Core GitHub Module (github.py)
```python
import os
import uuid
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from pathlib import Path

from github import Github
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from rich.console import Console

console = Console()

@dataclass
class GitHubConfig:
    token: str
    repo: str  # format: "owner/repo"
    
    @classmethod
    def from_env(cls) -> "GitHubConfig":
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable required")
        
        repo = os.getenv("GITHUB_REPO")
        if not repo:
            # Try to detect from git remote
            repo = detect_github_repo()
        
        return cls(token=token, repo=repo)

class GitHubClient:
    def __init__(self, config: GitHubConfig):
        self.config = config
        self.gh = Github(config.token)
        self.repo = self.gh.get_repo(config.repo)
        
        # GraphQL client for Projects
        transport = RequestsHTTPTransport(
            url="https://api.github.com/graphql",
            headers={"Authorization": f"Bearer {config.token}"}
        )
        self.gql_client = Client(transport=transport, fetch_schema_from_transport=True)
    
    def create_task_issue(self, title: str, body: str, worktree: str, 
                         task_uuid: str, labels: List[str] = None) -> int:
        """Create GitHub issue for orchestration task"""
        
        # Generate short UUID for label
        short_uuid = task_uuid[:7]
        
        # Prepare labels
        all_labels = labels or []
        all_labels.extend([
            f"cdock.{worktree}.{short_uuid}",
            "cdock-task",
            "stage-1",
            "todo"
        ])
        
        # Enhanced body with metadata
        enhanced_body = f"""<!-- cdock-id: {task_uuid} -->
<!-- cdock-worktree: {worktree} -->
<!-- cdock-short: {short_uuid} -->

{body}

---
**cdock metadata:**
- Worktree: `{worktree}`
- Task UUID: `{task_uuid}`
- Created: {datetime.now().isoformat()}
"""
        
        # Create issue
        issue = self.repo.create_issue(
            title=title,
            body=enhanced_body,
            labels=all_labels
        )
        
        console.print(f"[green]✅ Created issue #{issue.number}: {title}[/green]")
        return issue.number
    
    def update_task_status(self, issue_number: int, status: str, 
                          comment: str = None) -> None:
        """Update task status via labels and comments"""
        
        issue = self.repo.get_issue(issue_number)
        
        # Update status labels
        current_labels = [label.name for label in issue.labels]
        status_labels = ["todo", "in-progress", "completed", "failed", "needs-help"]
        
        # Remove old status labels
        new_labels = [l for l in current_labels if l not in status_labels]
        new_labels.append(status)
        
        # Update issue
        issue.edit(labels=new_labels)
        
        # Add comment if provided
        if comment:
            issue.create_comment(f"**Status Update:** {status}\n\n{comment}")
        
        console.print(f"[blue]📝 Updated issue #{issue_number} to {status}[/blue]")
    
    def create_help_request(self, worktree: str, task_uuid: str, 
                           error_msg: str, attempts: int, 
                           time_spent: str) -> int:
        """Create help request issue for stuck agent"""
        
        title = f"🆘 Agent needs help in {worktree}"
        
        body = f"""**Agent is stuck and needs human guidance**

**Worktree:** `{worktree}`
**Task UUID:** `{task_uuid}`
**Error:** {error_msg}
**Attempts:** {attempts}/3
**Time spent:** {time_spent}

**Instructions:**
1. Review the error above
2. Check the worktree: `cd worktrees/{worktree}`
3. Comment with guidance or fixes
4. Update labels to `ready-to-continue` when resolved

**Agent will poll this issue for responses.**
"""
        
        issue_number = self.create_task_issue(
            title=title,
            body=body,
            worktree=worktree,
            task_uuid=task_uuid,
            labels=["needs-help", "agent-stuck", "high-priority"]
        )
        
        return issue_number
    
    def check_help_response(self, issue_number: int) -> Optional[str]:
        """Check if human has responded to help request"""
        
        issue = self.repo.get_issue(issue_number)
        labels = [label.name for label in issue.labels]
        
        if "ready-to-continue" in labels:
            # Get latest comment from human
            comments = list(issue.get_comments())
            if comments:
                return comments[-1].body
        
        return None
    
    def get_worktree_tasks(self, worktree: str) -> List[Dict[str, Any]]:
        """Get all tasks for a specific worktree"""
        
        issues = self.repo.get_issues(
            state="open",
            labels=[f"cdock-task"]
        )
        
        worktree_issues = []
        for issue in issues:
            labels = [label.name for label in issue.labels]
            worktree_labels = [l for l in labels if l.startswith(f"cdock.{worktree}.")]
            
            if worktree_labels:
                # Extract status
                status_labels = ["todo", "in-progress", "completed", "failed", "needs-help"]
                status = next((l for l in labels if l in status_labels), "unknown")
                
                worktree_issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "status": status,
                    "url": issue.html_url,
                    "labels": labels
                })
        
        return worktree_issues
```

### Phase 2.2: State Management Integration

#### State File Enhancement
```python
@dataclass
class WorktreeState:
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
    
    def save(self, path: Path = None):
        """Save state to .cdock/state.json"""
        if path is None:
            path = Path(".cdock/state.json")
        
        path.parent.mkdir(exist_ok=True)
        
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, path: Path = None) -> "WorktreeState":
        """Load state from .cdock/state.json"""
        if path is None:
            path = Path(".cdock/state.json")
        
        if not path.exists():
            raise FileNotFoundError(f"State file not found: {path}")
        
        with open(path) as f:
            data = json.load(f)
        
        return cls(**data)
    
    def update_status(self, status: str, github_client: GitHubClient = None):
        """Update status in state file and GitHub"""
        self.status = status
        self.updated_at = datetime.now().isoformat()
        
        # Update GitHub if client provided
        if github_client and self.github.get("issue_number"):
            github_client.update_task_status(
                self.github["issue_number"],
                status,
                f"Status updated from worktree: {self.worktree_id}"
            )
        
        self.save()
```

### Phase 2.3: Orchestration Commands

#### New CLI Commands
```python
@cli.command()
def orchestrate():
    """Interactive orchestration planning"""
    from .orchestrator import start_orchestration
    start_orchestration()

@cli.command()
def status():
    """Show status of all worktrees"""
    from .orchestrator import show_status
    show_status()

@cli.command()
@click.option('--worktree', help='Specific worktree to sync')
def sync(worktree):
    """Sync worktree states with GitHub"""
    from .orchestrator import sync_github
    sync_github(worktree)

@cli.command()
def help_agent():
    """Create help request for current worktree"""
    from .orchestrator import create_help_request
    create_help_request()
```

#### Orchestrator Module (orchestrator.py)
```python
import os
import json
from pathlib import Path
from typing import List, Dict, Any

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

from .github import GitHubClient, GitHubConfig
from .state import WorktreeState

console = Console()

class Orchestrator:
    def __init__(self):
        self.github_config = GitHubConfig.from_env()
        self.github = GitHubClient(self.github_config)
    
    def start_orchestration(self):
        """Interactive orchestration planning"""
        console.print("[bold blue]🎯 cdock Orchestrator[/bold blue]")
        console.print("Let's plan your development workflow!\n")
        
        # Get goal from user
        goal = Prompt.ask("What would you like to build?")
        
        # Get AI suggestion (placeholder - would integrate with Claude)
        console.print(f"\n[yellow]Analyzing goal: {goal}[/yellow]")
        console.print("Suggested breakdown:")
        console.print("1. Backend API implementation")
        console.print("2. Frontend components")
        console.print("3. Database schema")
        console.print("4. Testing suite")
        
        # Confirm plan
        if Confirm.ask("\nProceed with this plan?"):
            self.create_orchestration_plan(goal)
        else:
            console.print("Plan cancelled.")
    
    def create_orchestration_plan(self, goal: str):
        """Create GitHub project and worktrees for orchestration"""
        
        # Create main tracking issue
        main_issue = self.github.create_task_issue(
            title=f"Orchestration: {goal}",
            body=f"Main tracking issue for: {goal}",
            worktree="main",
            task_uuid=str(uuid.uuid4()),
            labels=["orchestration", "epic"]
        )
        
        # Create worktrees for each task
        tasks = [
            {"name": "backend-api", "title": "Backend API implementation"},
            {"name": "frontend-components", "title": "Frontend components"},
            {"name": "database-schema", "title": "Database schema"},
            {"name": "testing-suite", "title": "Testing suite"}
        ]
        
        for task in tasks:
            self.create_worktree_task(task["name"], task["title"], main_issue)
        
        console.print(f"\n[green]✅ Created orchestration plan with {len(tasks)} tasks[/green]")
        console.print(f"Main issue: #{main_issue}")
        console.print("\nNext steps:")
        console.print("1. Review issues on GitHub")
        console.print("2. Run parallel execution: `cdock execute-stage`")
    
    def create_worktree_task(self, worktree_name: str, title: str, 
                           main_issue: int):
        """Create worktree and GitHub issue for task"""
        
        # Generate task UUID
        task_uuid = str(uuid.uuid4())
        
        # Create worktree
        os.system(f"git worktree add worktrees/{worktree_name}")
        
        # Create GitHub issue
        issue_number = self.github.create_task_issue(
            title=title,
            body=f"Task for worktree: {worktree_name}\n\nRelated to #{main_issue}",
            worktree=worktree_name,
            task_uuid=task_uuid,
            labels=["task", "stage-1"]
        )
        
        # Create state file in worktree
        worktree_path = Path(f"worktrees/{worktree_name}")
        state = WorktreeState(
            worktree_id=f"{worktree_name}-{datetime.now().strftime('%Y%m%d')}",
            task_uuid=task_uuid,
            short_uuid=task_uuid[:7],
            branch=f"feature/{worktree_name}",
            status="todo",
            github={
                "issue_number": issue_number,
                "pr_number": None,
                "labels": [f"cdock.{worktree_name}.{task_uuid[:7]}", "task", "stage-1", "todo"]
            },
            attempts={"current": 0, "max": 3, "last_error": None, "error_hash": None},
            timing={
                "started_at": None,
                "max_duration": 1800,  # 30 minutes
                "timeout_at": None
            },
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        state.save(worktree_path / ".cdock" / "state.json")
        
        # Create task instructions
        with open(worktree_path / "CLAUDE.md", "w") as f:
            f.write(f"# {title}\n\n")
            f.write(f"## Task Description\n{title}\n\n")
            f.write(f"## GitHub Issue\n#{issue_number}\n\n")
            f.write(f"## Instructions\n")
            f.write(f"Implement {title} according to project requirements.\n")
            f.write(f"Update GitHub issue #{issue_number} with progress.\n")
    
    def show_status(self):
        """Show status of all worktrees"""
        console.print("[bold blue]📊 Worktree Status[/bold blue]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Worktree", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("GitHub Issue", style="blue")
        table.add_column("Last Updated", style="yellow")
        
        # Find all worktrees
        worktrees_dir = Path("worktrees")
        if worktrees_dir.exists():
            for worktree_path in worktrees_dir.iterdir():
                if worktree_path.is_dir():
                    state_file = worktree_path / ".cdock" / "state.json"
                    if state_file.exists():
                        try:
                            state = WorktreeState.load(state_file)
                            table.add_row(
                                worktree_path.name,
                                state.status,
                                f"#{state.github['issue_number']}" if state.github.get('issue_number') else "None",
                                state.updated_at
                            )
                        except Exception as e:
                            table.add_row(
                                worktree_path.name,
                                "Error loading state",
                                "Unknown",
                                "Unknown"
                            )
        
        console.print(table)
    
    def sync_github(self, worktree: str = None):
        """Sync worktree states with GitHub"""
        console.print("[yellow]🔄 Syncing with GitHub...[/yellow]")
        
        if worktree:
            # Sync specific worktree
            self._sync_worktree(worktree)
        else:
            # Sync all worktrees
            worktrees_dir = Path("worktrees")
            if worktrees_dir.exists():
                for worktree_path in worktrees_dir.iterdir():
                    if worktree_path.is_dir():
                        self._sync_worktree(worktree_path.name)
        
        console.print("[green]✅ Sync complete[/green]")
    
    def _sync_worktree(self, worktree: str):
        """Sync single worktree with GitHub"""
        state_file = Path(f"worktrees/{worktree}/.cdock/state.json")
        
        if state_file.exists():
            try:
                state = WorktreeState.load(state_file)
                if state.github.get("issue_number"):
                    # Get latest GitHub status
                    github_tasks = self.github.get_worktree_tasks(worktree)
                    if github_tasks:
                        github_status = github_tasks[0]["status"]
                        if github_status != state.status:
                            console.print(f"[blue]Updating {worktree}: {state.status} → {github_status}[/blue]")
                            state.status = github_status
                            state.save(state_file)
            except Exception as e:
                console.print(f"[red]Error syncing {worktree}: {e}[/red]")
```

### Phase 2.4: Agent Safety Integration

#### Error Handling and Recovery
```python
class AgentSafetyManager:
    def __init__(self, worktree_state: WorktreeState, github_client: GitHubClient):
        self.state = worktree_state
        self.github = github_client
    
    def check_attempt_limit(self, error_msg: str) -> bool:
        """Check if agent has exceeded attempt limit"""
        error_hash = hashlib.md5(error_msg.encode()).hexdigest()
        
        # Check if same error as before
        if self.state.attempts["error_hash"] == error_hash:
            self.state.attempts["current"] += 1
        else:
            # New error, reset counter
            self.state.attempts = {
                "current": 1,
                "max": 3,
                "last_error": error_msg,
                "error_hash": error_hash
            }
        
        # Check if exceeded limit
        if self.state.attempts["current"] >= self.state.attempts["max"]:
            self.create_help_request(error_msg)
            return False
        
        self.state.save()
        return True
    
    def check_time_limit(self) -> bool:
        """Check if agent has exceeded time limit"""
        if not self.state.timing["started_at"]:
            self.state.timing["started_at"] = datetime.now().isoformat()
            self.state.timing["timeout_at"] = (
                datetime.now() + timedelta(seconds=self.state.timing["max_duration"])
            ).isoformat()
            self.state.save()
            return True
        
        timeout_at = datetime.fromisoformat(self.state.timing["timeout_at"])
        if datetime.now() > timeout_at:
            self.create_help_request("Task timeout - exceeded maximum duration")
            return False
        
        return True
    
    def create_help_request(self, error_msg: str):
        """Create help request issue"""
        time_spent = self.calculate_time_spent()
        
        issue_number = self.github.create_help_request(
            worktree=self.state.worktree_id.split("-")[0],  # Extract worktree name
            task_uuid=self.state.task_uuid,
            error_msg=error_msg,
            attempts=self.state.attempts["current"],
            time_spent=time_spent
        )
        
        # Update state
        self.state.status = "needs-help"
        self.state.github["help_issue"] = issue_number
        self.state.save()
        
        console.print(f"[red]🆘 Created help request: #{issue_number}[/red]")
        console.print("Agent paused. Waiting for human response...")
    
    def wait_for_help_response(self) -> Optional[str]:
        """Wait for human response to help request"""
        help_issue = self.state.github.get("help_issue")
        if not help_issue:
            return None
        
        console.print("[yellow]⏳ Waiting for human response...[/yellow]")
        
        # Poll for response (in real implementation, this would be more sophisticated)
        import time
        while True:
            response = self.github.check_help_response(help_issue)
            if response:
                console.print("[green]✅ Human response received![/green]")
                self.state.status = "in-progress"
                self.state.attempts["current"] = 0  # Reset attempts
                self.state.save()
                return response
            
            time.sleep(30)  # Poll every 30 seconds
    
    def calculate_time_spent(self) -> str:
        """Calculate time spent on task"""
        if not self.state.timing["started_at"]:
            return "Unknown"
        
        started = datetime.fromisoformat(self.state.timing["started_at"])
        elapsed = datetime.now() - started
        
        hours = int(elapsed.total_seconds() // 3600)
        minutes = int((elapsed.total_seconds() % 3600) // 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
```

## Implementation Timeline

### Week 1: GitHub Issues Integration
- [ ] Set up GitHub API clients (REST + GraphQL)
- [ ] Implement issue creation and status updates
- [ ] Add label-based task tracking
- [ ] Test with simple worktree scenarios

### Week 2: State Management
- [ ] Enhance state files with GitHub integration
- [ ] Add state synchronization between local and GitHub
- [ ] Implement progressive pushing workflow
- [ ] Add backup and recovery mechanisms

### Week 3: Orchestration Commands
- [ ] Add `cdock orchestrate` command
- [ ] Implement `cdock status` and `cdock sync`
- [ ] Add worktree creation and management
- [ ] Test multi-worktree scenarios

### Week 4: Agent Safety
- [ ] Implement attempt limiting and error detection
- [ ] Add timeout mechanisms
- [ ] Create help request system
- [ ] Test agent recovery workflows

## Success Criteria

### Technical Integration
- [ ] GitHub Issues created and updated automatically
- [ ] Labels provide portable task tracking
- [ ] State synchronization works reliably
- [ ] GraphQL Projects integration functions
- [ ] Progressive pushing shows real-time progress

### User Experience
- [ ] Orchestration planning is intuitive
- [ ] Status visibility is clear and helpful
- [ ] Agent help requests are actionable
- [ ] Human intervention points are obvious
- [ ] Failure recovery is smooth

### System Reliability
- [ ] Works with GitHub API rate limits
- [ ] Handles network failures gracefully
- [ ] State consistency maintained across restarts
- [ ] No data loss during failures
- [ ] Proper error reporting and logging

## Future Enhancements

### Advanced Features
- [ ] GitHub Projects visual boards
- [ ] Slack/Discord notifications
- [ ] PR creation and management
- [ ] Automated testing integration
- [ ] Metrics and analytics

### Alternative Integrations
- [ ] Gitea/Forgejo compatibility
- [ ] Linear/Trello integration
- [ ] Local-only mode
- [ ] Enterprise GitHub support

This plan provides comprehensive GitHub integration while maintaining the portability and reliability principles established in the overall project plan.