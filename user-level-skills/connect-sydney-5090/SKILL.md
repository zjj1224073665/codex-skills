---
name: connect-sydney-5090
description: Use when Codex needs to connect to, run commands on, verify SSH configuration for, or troubleshoot the Sydney_5090 SSH host at 100.120.95.16 as user junjiezhao with the ~/.ssh/id_ed25519 identity.
---

# Connect Sydney 5090

## Purpose

Use the SSH alias `Sydney_5090` for remote access to the host at `100.120.95.16` as `junjiezhao`. Prefer the alias over repeating raw SSH options.

## Expected SSH Config

The expected `~/.ssh/config` entry is:

```sshconfig
Host Sydney_5090
    HostName 100.120.95.16
    User junjiezhao
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 20
    ServerAliveCountMax 3
    TCPKeepAlive yes
    ControlMaster auto
    ControlPersist 10m
    ControlPath ~/.ssh/cm-%C
```

Before connecting, verify the alias exists if the local SSH setup is uncertain:

```bash
ssh -G Sydney_5090 | rg '^(hostname|user|identityfile|identitiesonly|controlpath) '
```

If the alias is missing and the task requires using this host, add or update only the `Host Sydney_5090` block in `~/.ssh/config`. Preserve other SSH config entries.

## Connection Commands

Use these commands:

```bash
ssh Sydney_5090
ssh Sydney_5090 'hostname && whoami && uptime'
scp local-file Sydney_5090:/remote/path/
rsync -av local-dir/ Sydney_5090:/remote/path/
```

Prefer non-interactive `ssh Sydney_5090 '<command>'` for checks and small remote tasks. Use an interactive shell only when the user asks for one or when a task genuinely requires it.

## Troubleshooting

- If authentication fails, check that `~/.ssh/id_ed25519` exists and is not world-readable.
- If the host is unreachable, remember that `100.120.95.16` is in the private `100.64.0.0/10` range; check the relevant overlay network or VPN before changing SSH options.
- If a multiplexed connection is stale, try `ssh -O check Sydney_5090` and then `ssh -O exit Sydney_5090` before removing control socket files manually.
- Use `ssh -vvv Sydney_5090` only for diagnosis, and redact sensitive paths or environment details before reporting output.

## Safety Rules

- Never print or inspect private key contents.
- Do not disable host key checking to bypass warnings.
- Do not modify `known_hosts`, delete SSH control sockets, or change key permissions unless the task requires it and the action is clearly scoped.
- Ask for explicit confirmation before destructive or long-running remote commands.
