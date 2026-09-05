# call-local-codex-from-claude

Skill + scripts for handing a prompt from Claude Code (or any shell) to the local Codex CLI
and collecting the full answer. Read `SKILL.md` first.

```
scripts/codex_exec.sh PROMPT.md OUT/          # default, bash only
python3 scripts/codex_appserver.py PROMPT.md OUT/   # JSON-RPC app-server
node scripts/codex_sdk.mjs PROMPT.md OUT/     # needs: npm install @openai/codex-sdk
scripts/codex_mcp_server_DEPRECATED.py        # reference only; fails for web research
examples/                                      # real prompt + the answers each method produced
```
