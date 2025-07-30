#!/bin/bash
# Claude Code Orchestrator Security Hook
# Restricts orchestrator to only worktree management and instruction writing

# Read JSON input from stdin
input=$(cat)

# Extract the command from JSON input using correct Claude Code format
# For Bash tool, look for tool_input.command
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# If no command found, try looking for file_path (Write/Edit tools)
if [[ -z "$command" ]]; then
  file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
  if [[ -n "$file_path" ]]; then
    command="$file_path"
  fi
fi

# If still no command, block by default
if [[ -z "$command" ]]; then
  echo "🚫 Orchestrator blocked: No command found in input"
  exit 2
fi

# Check allowed commands
if [[ "$command" == "git worktree add worktrees/"* ]] || \
   [[ "$command" == "git worktree remove worktrees/"* ]] || \
   [[ "$command" == "git worktree list"* ]]; then
  exit 0  # Allow worktree management
fi

if [[ "$command" == "cdock"* ]]; then
  exit 0  # Allow spawning containers
fi

if [[ "$command" == "echo"* ]] || \
   [[ "$command" == "mkdir -p worktrees"* ]] || \
   [[ "$command" == "cd worktrees/"* ]] || \
   [[ "$command" == "basename"* ]] || \
   [[ "$command" == "pwd"* ]]; then
  exit 0  # Allow basic orchestration commands
fi

# Allow writing instructions to worktrees (for Write tool)
if [[ "$command" == "worktrees/"*"/CLAUDE.md" ]] || \
   [[ "$command" == "worktrees/"*"/CLAUDE.local.md" ]]; then
  exit 0  # Allow instruction writing
fi

# Also allow absolute paths to worktrees
if [[ "$command" == *"/worktrees/"*"/CLAUDE.md" ]] || \
   [[ "$command" == *"/worktrees/"*"/CLAUDE.local.md" ]]; then
  exit 0  # Allow instruction writing with absolute paths
fi

# Debug: log what we're actually checking
echo "Debug: command='$command'" >> /tmp/hook-debug.log

# Block everything else
echo "🚫 Orchestrator blocked: $command"
exit 2