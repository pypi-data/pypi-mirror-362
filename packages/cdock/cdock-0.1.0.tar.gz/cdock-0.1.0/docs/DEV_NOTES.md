# cdock Development Notes

## Agent Control & Safety Mechanisms

### Attempt Budgets
```python
# In .cdock/state.json
"attempts": {
    "current": 2,
    "max": 3,
    "last_error": "ESLint: 'unused-variable' error",
    "error_hash": "abc123"
}
```

**Implementation:**
- Track error hash (MD5 of error message)
- Increment attempts only for same error
- Create GitHub issue after max attempts reached
- Reset counter on successful completion

### Time Boxing
```python
# In .cdock/state.json
"timing": {
    "started_at": "2024-01-15T10:00:00Z",
    "max_duration": 1800,  # 30 minutes
    "timeout_at": "2024-01-15T10:30:00Z"
}
```

**Implementation:**
- Check elapsed time before each major operation
- Create timeout issue with progress summary
- Allow human to extend timeout or redirect approach

### Error Pattern Detection
```bash
# Agent checks for repeated errors
current_error_hash=$(echo "$ERROR_MSG" | md5sum | cut -d' ' -f1)
if [[ "$current_error_hash" == "$last_error_hash" ]]; then
    ((attempts++))
    if [[ $attempts -ge 3 ]]; then
        create_help_issue "Stuck on repeated error" "$ERROR_MSG"
        exit 1
    fi
fi
```

### Structured Help Issues
```python
def create_help_issue(title, error_detail):
    gh.create_issue(
        title=f"🆘 Agent needs help: {title}",
        body=f"""**Worktree:** {os.getcwd()}
**Task:** {read_file('CLAUDE.md').split('\n')[0]}
**Error:** {error_detail}
**Attempts:** {attempts}/{max_attempts}
**Time spent:** {calculate_elapsed_time()}
**Error hash:** {error_hash}

Please review and comment with guidance.""",
        labels=["agent-help", f"cdock.{worktree_name}.{task_uuid}"]
    )
```

## GitHub Integration Strategy

### API Approach
- **Mixed API approach** - Issues REST API + Projects GraphQL API
- **Python libraries** (PyGithub + GraphQL client) for uvx version
- **Issues + Labels** as source of truth for portability
- **GitHub Projects** for enhanced UX (GraphQL required)
- **Progressive pushing** for real-time visibility

### ID Format
- **Pattern:** `cdock.{worktree}.{7-char-uuid}`
- **Examples:** `cdock.auth-system.a7b2c8d`, `cdock.logging.f1e9a3b`
- **Collision scope:** Only check against open issues in same worktree namespace
- **Storage:** Full UUID in issue body for audit trail

### Label Strategy
```python
# GitHub label examples
labels = [
    f"cdock.{worktree_name}.{short_uuid}",  # Unique identifier
    "stage-1",                              # Current stage
    "in-progress",                          # Status
    "agent-help"                            # Special flags
]
```

### Sync Strategy
- **GitHub as source of truth** with local backup
- **Periodic sync** to local JSON files
- **Offline fallback** to file-based coordination
- **Git handles file conflicts** (one writer per worktree)

## State Management

### Worktree State File (.cdock/state.json)
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
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T14:22:00Z"
}
```

### Coordination Backup
```python
# Periodic backup of GitHub state
def backup_coordination_state():
    issues = github_api.get_issues(labels="cdock.*")
    projects = github_api.get_projects()
    
    # Local backup
    save_json('coordination/issues.json', issues)
    save_json('coordination/projects.json', projects)
    
    # Markdown fallback
    generate_markdown_issues()
    generate_markdown_projects()
```

## Future Portability

### System Agnostic Design
- **Custom field filtering** works with any kanban system
- **Label-based integration** for Trello/Linear/Asana
- **GitHub-compatible APIs** (Gitea/Forgejo fallback)
- **File-based fallback** for complete independence

### Migration Strategy
```python
def migrate_to_new_system(new_api):
    for issue in github_issues:
        task_uuid = extract_uuid_from_body(issue.body)
        new_api.create_task(
            title=issue.title,
            custom_field="cdock_id",
            value=task_uuid
        )
```

## Performance Considerations

### Collision Checking
- **Scope:** Only check open issues in same worktree namespace
- **Frequency:** Only on task creation, not every operation
- **Fallback:** Generate new UUID if collision found

### API Rate Limits
- **GitHub:** 5,000 requests/hour for authenticated users
- **Batching:** Group multiple operations when possible
- **Caching:** Cache GitHub state locally, sync periodically

### Container Reuse
- **Same worktree:** Reuse container for multiple operations
- **Different worktrees:** Fresh containers for isolation
- **Cleanup:** Remove containers after task completion