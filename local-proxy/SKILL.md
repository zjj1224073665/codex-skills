---
name: local-proxy
description: Use this skill when a command, dependency install, package manager, git clone, API call, model/tool download, or other network access fails or may fail on this machine due to connectivity, DNS, TLS, timeout, registry, index, or unreachable-service errors. This machine can often reach blocked services by exporting the local HTTP/HTTPS proxy at http://192.168.8.223:10809.
---

# Local Proxy

When network access fails or is likely to fail on this machine, retry the command with the local proxy:

```bash
export http_proxy=http://192.168.8.223:10809
export https_proxy=http://192.168.8.223:10809
export HTTP_PROXY=http://192.168.8.223:10809
export HTTPS_PROXY=http://192.168.8.223:10809
```

For one-off commands, prefix the command instead of changing the whole shell:

```bash
http_proxy=http://192.168.8.223:10809 https_proxy=http://192.168.8.223:10809 HTTP_PROXY=http://192.168.8.223:10809 HTTPS_PROXY=http://192.168.8.223:10809 <command>
```

For package managers:

- `apt-get`: use `-o Acquire::http::Proxy=http://192.168.8.223:10809 -o Acquire::https::Proxy=http://192.168.8.223:10809`.
- `npm`/`pnpm`/`yarn`: prefer proxy environment variables first; if needed, also set the tool-specific proxy config for the current command.
- `git`: prefer proxy environment variables first; if needed, use `git -c http.proxy=http://192.168.8.223:10809 -c https.proxy=http://192.168.8.223:10809 ...`.

Do not add these proxy variables to project files unless the user asks. Keep proxy use scoped to the failing command or current shell session.
