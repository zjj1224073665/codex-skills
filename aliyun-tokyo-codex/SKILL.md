---
name: aliyun-tokyo-codex
description: Use when the user asks to connect to Tokyo Aliyun, aliyun-Tokyo, 阿里云东京, 东京阿里云, or says "连东京阿里云codex". This skill identifies the SSH target Host aliyun-Tokyo at 8.216.84.102 with user binquant.
---

# Aliyun Tokyo Codex

## SSH Target

When the user asks to connect to "东京阿里云codex", "东京阿里云", "阿里云东京", or `aliyun-Tokyo`, use this SSH target:

```sshconfig
Host aliyun-Tokyo
  HostName 8.216.84.102
  User binquant
```

Prefer the configured alias if it exists:

```bash
ssh aliyun-Tokyo
```

If the alias is not present in the local SSH config, connect directly:

```bash
ssh binquant@8.216.84.102
```

## Handling

- Do not expose private keys, passwords, or SSH agent details.
- If authentication needs a password, passphrase, MFA, or host-key confirmation, leave the SSH session interactive for the user to handle.
- If the user asks only which host this refers to, answer with `binquant@8.216.84.102` and mention alias `aliyun-Tokyo`.
