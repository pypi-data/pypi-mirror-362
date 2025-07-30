#!/bin/bash
set -e

# Get username from environment or default to hostuser
USERNAME=${HOST_USERNAME:-hostuser}

# Create user and group first
groupadd -g ${HOST_GID:-1000} hostgroup 2>/dev/null || true
useradd -u ${HOST_UID:-1000} -g ${HOST_GID:-1000} -d /home/${USERNAME} ${USERNAME} 2>/dev/null || true

# Create user home directory
mkdir -p /home/${USERNAME}
chown -R ${USERNAME}:hostgroup /home/${USERNAME}

# Initialize claude auth from host on first run
if [ ! -f /home/${USERNAME}/.claude-auth/.initialized ]; then
  echo "First run: initializing Claude auth from host..."
  mkdir -p /home/${USERNAME}/.claude-auth

  # Copy host claude directory and file if they exist
  if [ -d /host-claude-dir ]; then
    cp -r /host-claude-dir /home/${USERNAME}/.claude-auth/claude-dir
  fi
  if [ -f /host-claude-file ]; then
    cp /host-claude-file /home/${USERNAME}/.claude-auth/claude.json
  fi

  chown -R ${USERNAME}:hostgroup /home/${USERNAME}/.claude-auth
  touch /home/${USERNAME}/.claude-auth/.initialized
fi

# Create symlinks to auth volume
ln -sf /home/${USERNAME}/.claude-auth/claude-dir /home/${USERNAME}/.claude
ln -sf /home/${USERNAME}/.claude-auth/claude.json /home/${USERNAME}/.claude.json

# SSH key setup
if [ -f /root/.ssh/id_rsa ]; then
  # Create user SSH directory
  mkdir -p /home/${USERNAME}/.ssh
  chown ${USERNAME}:hostgroup /home/${USERNAME}/.ssh
  chmod 700 /home/${USERNAME}/.ssh
  
  # Copy SSH keys from mounted location to user directory
  cp /root/.ssh/id_rsa /home/${USERNAME}/.ssh/id_rsa
  chmod 600 /home/${USERNAME}/.ssh/id_rsa
  chown ${USERNAME}:hostgroup /home/${USERNAME}/.ssh/id_rsa
  
  if [ -f /root/.ssh/id_rsa.pub ]; then
    cp /root/.ssh/id_rsa.pub /home/${USERNAME}/.ssh/id_rsa.pub
    chmod 644 /home/${USERNAME}/.ssh/id_rsa.pub
    chown ${USERNAME}:hostgroup /home/${USERNAME}/.ssh/id_rsa.pub
  fi
  
  # Create SSH config for git operations
  cat >/home/${USERNAME}/.ssh/config <<EOF
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
EOF
  chmod 600 /home/${USERNAME}/.ssh/config
  chown ${USERNAME}:hostgroup /home/${USERNAME}/.ssh/config
fi

# Configure git
sudo -u ${USERNAME} git config --global core.sshCommand "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR" 2>/dev/null || true

# Create other directories
sudo -u ${USERNAME} mkdir -p /home/${USERNAME}/.cache/uv
sudo -u ${USERNAME} mkdir -p /home/${USERNAME}/.local/share/uv
sudo -u ${USERNAME} mkdir -p /home/${USERNAME}/.config
sudo -u ${USERNAME} mkdir -p /home/${USERNAME}/git

# Add aliases
cat >>/home/${USERNAME}/.bashrc <<'EOF'
alias va='. .venv/bin/activate'
alias ll='ls -la'
alias la='ls -A'

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi
EOF
chown ${USERNAME}:hostgroup /home/${USERNAME}/.bashrc

# Find repo and continue...
# Look for any directory in /home/${USERNAME}/git/ (mounted repo)
REPO_DIR=$(find /home/${USERNAME}/git -maxdepth 1 -type d ! -name git | head -1)
if [ -n "$REPO_DIR" ]; then
  cd "$REPO_DIR"
  chown -R ${USERNAME}:hostgroup "$REPO_DIR"

  if [ "$1" = "bash" ]; then
    shift  # Remove "bash" from arguments
    exec sudo -u ${USERNAME} bash -c "cd '$REPO_DIR' && exec bash $*"
  else
    if [ -f "pyproject.toml" ]; then
      echo "Python project detected, setting up uv environment..."
      sudo -u ${USERNAME} uv sync
      exec sudo -u ${USERNAME} uv run claude --dangerously-skip-permissions "$@"
    else
      echo "Non-Python project detected, running claude directly..."
      exec sudo -u ${USERNAME} claude --dangerously-skip-permissions "$@"
    fi
  fi
else
  echo "No repo directory found"
  exec sudo -u ${USERNAME} bash
fi
