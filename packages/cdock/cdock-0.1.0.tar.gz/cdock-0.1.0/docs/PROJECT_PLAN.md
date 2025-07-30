# cdock Orchestration System - Project Plan

## Vision
Transform cdock from a simple containerized Claude Code runner into a sophisticated multi-agent orchestration system that enables parallel development workflows with human oversight.

## Core Architecture

### 1. Multi-Stage Orchestration
- **Conversational planning** in main repo (human-AI collaboration)
- **Stage-based execution** with human approval checkpoints
- **Parallel worktree execution** within each stage
- **Manual progression** between stages ("3 worked, 1 failed")

### 2. Git Worktree Management
- **Hierarchical worktrees** (features can have sub-features)
- **State files** (`.cdock/state.json`) linking filesystem to GitHub
- **Context isolation** - each worktree has complete execution context
- **Smart resumption** - agents can pick up where they left off

### 3. GitHub Integration Layer
- **Use GitHub exclusively** for now (accept outage risk)
- **GitHub Projects (new)** - only type available (Classic deprecated 2024)
- **GraphQL API** for Projects, **REST API** for Issues (mixed approach)
- **Issues + Labels** as source of truth for portability
- **Python libraries** (PyGithub + GraphQL) for integration
- **Progressive pushing** for real-time visibility

### 4. Agent Communication & Control
- **Agents pause and create issues** when stuck or need guidance
- **Progressive commits** show real-time progress
- **File-based signaling** for coordination between agents
- **GitHub comments** for structured human-agent communication

## Key Refined Decisions

### ID Format & Collision Handling
- **Format:** `cdock.{worktree}.{7-char-uuid}` (git-familiar length)
- **Examples:** `cdock.auth-system.a7b2c8d`, `cdock.logging.f1e9a3b`
- **Active collision checking** (only against open issues in same worktree)
- **Full UUID stored in issue body** for audit trail
- **Worktree namespacing** reduces collision risk significantly

### GitHub Integration Strategy
- **GitHub as source of truth** with local file backup
- **Custom field filtering** works with any kanban system later
- **Label-based integration** for future Trello/Linear/Asana compatibility
- **Gitea fallback** possible with GitHub-compatible APIs
- **File conflicts handled by git** (one writer per worktree)

### Agent Safety & Control
- **Attempt budgets** (max 3 tries on same error hash)
- **Time boxing** (30 min max per task)
- **Error pattern detection** (MD5 hash of error message)
- **Structured GitHub issues** for agent help requests with full context

### Technical Implementation
- **Python + uvx** for cross-platform CLI tool distribution
- **Self-bootstrapping** (`uvx cdock install` sets up entire environment)
- **Docker containers** for execution environment isolation
- **Rich CLI** for beautiful terminal interface
- **PyGithub** for GitHub API integration

## Implementation Strategy

### Phase 1: Python Conversion (First Priority)
**Convert existing bash cdock to Python before adding GitHub integration**

**Rationale:** 
- Current bash cdock is simple enough to convert cleanly
- Avoid implementing GitHub integration twice (bash → Python)
- Python provides better error handling and state management
- uvx distribution is the end goal anyway

**Python conversion tasks:**
- Port Docker container management to Python
- Add Click for CLI interface
- Implement current subcommands (bash, clean, nuke, init)
- Add Rich for colored output
- Package for uvx distribution

### Phase 2: GitHub Integration
**Add GitHub integration to Python version**

**Core features:**
- Create/update GitHub issues for tasks
- Implement label-based task tracking
- Add state file management (.cdock/state.json)
- Progressive git pushing with status updates
- Agent help request system

### Phase 3: Orchestration Commands
**Add orchestration-specific commands**

```python
# New cdock commands
cdock orchestrate    # Interactive planning mode
cdock status         # Show all worktree status  
cdock sync           # Sync with GitHub
cdock help-agent     # Create help issue for current worktree
```

### Phase 4: Dogfooding Test
**Use enhanced Python cdock to develop itself further**

**Test scenario:**
1. Plan: "Add advanced orchestration features"
2. Create parallel worktrees for different features
3. Use GitHub issues for coordination
4. Test agent help requests and human intervention
5. Validate the entire workflow

## Key Features

### Orchestration Flow
1. **Planning Phase:** `cdock orchestrate` - conversational planning
   - Human describes goal: "Add authentication system"
   - AI suggests breakdown: "OAuth backend, login UI, session management, tests"
   - Create GitHub project board with issues for each task

2. **Execution Phase:** Stage-based parallel execution
   - Create worktrees for parallel tasks
   - Launch `cdock` in each worktree with specific instructions
   - Agents update GitHub issues with progress

3. **Integration Phase:** Human-gated progression
   - Review completed work via GitHub
   - Handle failures ("1 task failed, let's fix it")
   - Approve next stage execution

### State Management
```json
{
    "worktree_id": "auth-system-20240115",
    "task_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "short_uuid": "a7b2c8d",
    "branch": "feature/auth-system",
    "github": {
        "issue_number": 42,
        "pr_number": null,
        "labels": ["cdock.auth-system.a7b2c8d", "stage-1", "in-progress"]
    },
    "parent_worktree": null,
    "sub_worktrees": ["worktrees/login-ui", "worktrees/oauth-flow"],
    "status": "in-progress",
    "attempts": {
        "current": 0,
        "max": 3,
        "last_error": null,
        "error_hash": null
    },
    "timing": {
        "started_at": "2024-01-15T10:00:00Z",
        "max_duration": 1800,
        "timeout_at": "2024-01-15T10:30:00Z"
    }
}
```

### Agent Safety Features
- **Error hash tracking** to detect repeated failures
- **Progressive escalation** (simple → complex → human help)
- **Structured help requests** with full context
- **Time limits** to prevent infinite loops
- **Graceful degradation** when GitHub unavailable

## Success Metrics

### Technical Success
- **Python conversion** maintains all current functionality
- **GitHub integration** provides clear task coordination
- **Worktree management** handles parallel development
- **Agent help system** enables human intervention
- **State management** survives interruptions and restarts

### User Experience Success
- **Dogfooding** - team uses cdock to develop cdock
- **Parallel efficiency** - 4+ features developed simultaneously
- **Clear oversight** - human can monitor and intervene easily
- **Failure recovery** - stuck agents get help gracefully
- **Context isolation** - worktrees don't interfere with each other

### System Reliability
- **Offline resilience** - works when GitHub is down
- **State consistency** - no lost work or orphaned tasks
- **Error recovery** - agents fail gracefully
- **Performance** - responsive even with many active worktrees

## Future Enhancements

### Advanced Features
- **Nested orchestration** - sub-features with their own stages
- **Template system** - common orchestration patterns
- **Metrics dashboard** - progress visualization
- **Integration hooks** - CI/CD pipeline integration
- **Multi-repo support** - orchestration across repositories

### Alternative Integrations
- **Gitea/Forgejo** fallback for GitHub independence
- **Trello/Linear** integration for different PM tools
- **Slack/Discord** notifications for team coordination
- **Local-only mode** for completely offline development

## Architecture Decisions

### Why Python First
- **Better API integration** than bash subprocess calls
- **Cleaner error handling** and state management
- **Rich ecosystem** for CLI tools (Click, Rich, PyGithub)
- **Future-proof** for advanced features
- **Avoid double implementation** of GitHub integration

### Why Mixed GitHub API Approach
- **Issues REST API** - well-documented, stable, works with Gitea
- **Projects GraphQL API** - only option (Classic REST deprecated 2024)
- **Labels as source of truth** - ensures portability to other systems
- **GitHub Projects for UX** - best visual experience when available

### Why Progressive Pushing
- **Real-time visibility** into agent progress
- **Human intervention** possible at any time
- **GitHub integration** shows live work
- **Failure recovery** - work isn't lost if agent crashes

### Why File-Based State
- **Git-native** - conflicts handled by git
- **Debuggable** - human readable JSON
- **Persistent** - survives container restarts
- **Offline-capable** - works without GitHub

This plan prioritizes getting a working system quickly while building toward the full orchestration vision.