# cdock Development Notes

## **Package Management**

- **ALWAYS use `uv add` and `uv remove` for dependency management**
- **ALWAYS use `uv run python` instead of `python` for running scripts**
- **ALWAYS use `uv run` for running any commands in the project environment**

## Project Structure

- Python package in `src/cdock/`
- CLI entry point configured in `pyproject.toml`
- Focus on Linux/WSL2 support initially
- When installed as package, import as `from cdock.manager import CDockManager` (no "src.")

## Testing Philosophy

- Test real functionality, not object existence
- Minimal/zero mocks - test actual behavior
- Fail fast and loud - no silent failures
- Tests document expected behavior
- Quality over coverage metrics

## ✅ TESTED: Volume naming in worktrees
- ✅ Main repo: `/home/user/git/cdock/` → `cdock-cdock-{hash}`
- ✅ Feature worktree: `/home/user/git/cdock/worktrees/logging/` → `cdock-logging-{hash}`
- ✅ Subtask worktree: `/home/user/git/cdock/worktrees/logging/worktree/add-loguru-config/` → `cdock-add-loguru-config-{hash}`
- ✅ Each gets unique volume based on directory name + full path SHA256 hash
- ✅ Perfect isolation - each worktree has separate dependency environment
