---
name: call-local-codex-from-claude
description: Use when Claude Code (or any script/agent) must send a prompt to the LOCAL Codex CLI (本机 codex, gpt-5.6-luna, xhigh) and get its full answer back, e.g. "发给本机codex", "让 codex 回答", "用 luna xhigh 跑一下". Covers the 4 invocation paths tested on 2026-09-05 (codex exec / SDK / app-server / mcp-server), which one to use, and the traps (browser plugin permission denial, sandbox network, npm cache).
---

# Call local Codex from Claude Code

Tested on macOS with `codex-cli 0.153.2`, `~/.codex/config.toml` already set to
`model = "gpt-5.6-luna"`, `model_reasoning_effort = "xhigh"`. If the user says "luna xhigh",
no model flags are needed; the config default already is that. Pass `-m gpt-5.6-luna
-c model_reasoning_effort="xhigh"` only if the config has changed.

## TL;DR: which method

| # | Method | Works? | Web research? | Verdict |
|---|--------|--------|---------------|---------|
| 1 | `codex exec - < prompt.md --json -o last.md` | yes | yes (built-in `web_search`) | **Use this by default.** Simplest, no deps, survives classifier/permission prompts. |
| 3 | `@openai/codex-sdk` (Node, ESM) | yes | yes | Same engine as #1 (it spawns `codex exec --experimental-json`). Use only when you already live in Node and want typed events / multi-turn `resumeThread`. |
| 4 | `codex app-server` v2 JSON-RPC over stdio | yes | yes (must `--disable browser_use`) | Most control (threads, steer, interrupt, structured output), most code. Use for multi-turn or when you need server-side approvals routed to `auto_review`. |
| 2 | `codex mcp-server` (tools `codex`, `codex-reply`) | returns, but **research fails** | no | **Avoid.** Deprecated (prints a warning), and the Chrome browser plugin steals the search job then gets "user declined permission" because no human is there. `config.features.browser_use=false` inside the tool call did NOT disable it. |

Third-party wrappers found on the web (`@cexll/codex-mcp-server`, `codex-bridge`, `cli-agent-mcp`)
are just shells around `codex exec`; no reason to install them when #1 works.

## Method 1 (default): `codex exec`

```bash
# 1. write the prompt to a file (heredoc keeps CJK + LaTeX backslashes intact)
cat > /path/prompt.md <<'EOF_PROMPT'
...prompt...
EOF_PROMPT

# 2. run; "-" means read the whole prompt from stdin
codex exec --skip-git-repo-check \
  -s workspace-write \
  -c sandbox_workspace_write.network_access=true \
  -c 'web_search="live"' \
  --json -o /path/last.md - < /path/prompt.md > /path/events.jsonl 2> /path/stderr.log
```

`scripts/codex_exec.sh PROMPT_FILE OUT_DIR` wraps exactly this.

- `-o last.md` is the final agent message (the answer to relay). `events.jsonl` has every
  `item.started/completed` event (`web_search` items carry the queries; `agent_message` the text).
- Run it in the background (`run_in_background: true`, timeout 600000) and poll
  `wc -l events.jsonl`; an xhigh research task took ~6 min and 52 web searches.
- Do **not** use `-s danger-full-access`: Claude Code's auto-mode classifier blocks that
  command line. `workspace-write` + `network_access=true` is enough for web search.
- `--ephemeral` skips writing to `~/.codex/sessions`; omit it if you want `codex exec resume --last "follow-up"`.
- Multi-turn: `codex exec resume --last "next question"` or `codex exec resume <thread_id> "..."`
  (thread id is in the first `thread.started` event).
- Structured answer: add `--output-schema schema.json`.
- Stdin + argument together: `cat context.txt | codex exec "instruction"` puts the pipe in a `<stdin>` block.

## Method 3: TypeScript SDK

```bash
mkdir sdk && cd sdk && npm init -y && npm install --cache ./npmcache @openai/codex-sdk   # ~/.npm may be EACCES under sandbox
node scripts/codex_sdk.mjs prompt.md out/
```
ESM only (`require()` throws `ERR_PACKAGE_PATH_NOT_EXPORTED`). `startThread({model, modelReasoningEffort,
sandboxMode, networkAccessEnabled, webSearchMode:"live", approvalPolicy:"never", skipGitRepoCheck})`,
then `thread.runStreamed(prompt)` yields the same events as `--json`. `codex.resumeThread(id)` for follow-ups.

## Method 4: app-server (JSON-RPC v2, stdio)

`python3 scripts/codex_appserver.py prompt.md out/ [model] [effort]`

Sequence: `initialize` -> notification `initialized` -> `thread/start {cwd, model, sandbox,
approvalPolicy:"never", approvalsReviewer:"auto_review"}` -> `turn/start {threadId, input:[{type:"text",text}], effort}`
-> read notifications until `turn/completed`. Final text = last `item/completed` whose `item.type == "agentMessage"`.
Start the server with `--disable browser_use --disable browser_use_external -c 'web_search="live"'`
so the model uses built-in web search instead of the Chrome plugin.
Get the full protocol with `codex app-server generate-json-schema --out DIR`.

## Method 2: mcp-server (do not use for research)

Kept in `scripts/codex_mcp_server_DEPRECATED.py` for reference only. It answers in ~100 s
but every Google/OpenReview/arXiv visit is "rejected ... user declined permission" so the
model gives up on provenance and just writes the translation itself.

## Traps learned

- **Browser plugin hijack.** Codex has bundled `browser_use` plugins that prefer the user's
  Chrome. Headless callers must disable them (`--disable browser_use`) or, as with `codex exec`,
  rely on the model choosing `web_search`. If a result says "browser security policy ... user declined",
  that is what happened.
- **Sandbox network is off by default** in `workspace-write`; without
  `sandbox_workspace_write.network_access=true` curl/pip inside Codex fail (built-in web_search still works, it runs server-side).
- **Do not `cd` before the command** in Claude Code Bash; pass absolute paths (the shell resets cwd).
- **Foreground `sleep`** and `danger-full-access` get blocked by the auto-mode classifier; use `run_in_background` + Monitor instead.
- `codex features list` shows flags; `web_search` config values: `disabled | cached | live`.
- Codex reasoning at xhigh is slow; ~2 min for a plain answer, ~6 min with 50 searches. Budget the timeout accordingly.

## Relaying the answer

Copy `last.md` verbatim into the reply (the user wants Codex's own words, including its
provenance table). Then add a one-line note on which method ran, how long, how many searches.
See `examples/` for a real prompt and the three answers it produced.

## Benchmark (2026-09-05, same prompt in `examples/`, gpt-5.6-luna xhigh)

| Method | Wall time | Built-in web searches | Provenance table delivered? |
|---|---|---|---|
| 1 `codex exec` | 6 min 15 s | 52 | yes (3 of 5 sentences sourced, ICLR 2024/2025/2026 + NeurIPS 2024) |
| 3 SDK | 6 min 29 s | 25 | yes (3 of 5 sourced, ICLR 2025 + NeurIPS 2024) |
| 4 app-server | 5 min 41 s | 24 | yes (4 of 5 sourced, ICLR 2025 + NeurIPS 2024) |
| 2 mcp-server | 1 min 40 s | 0 (browser plugin denied) | no |

All three working paths give comparable answers; pick #1 for simplicity.
