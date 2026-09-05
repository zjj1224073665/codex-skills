#!/usr/bin/env bash
# Method 1 (recommended): codex exec, prompt from a file via stdin, JSONL events + final answer file.
# Usage: codex_exec.sh PROMPT_FILE OUT_DIR [extra codex args...]
set -euo pipefail
PROMPT="$1"; OUT="$2"; shift 2; mkdir -p "$OUT"
codex exec --skip-git-repo-check \
  -s workspace-write \
  -c sandbox_workspace_write.network_access=true \
  -c 'web_search="live"' \
  --json -o "$OUT/last.md" "$@" - < "$PROMPT" > "$OUT/events.jsonl" 2> "$OUT/stderr.log"
echo "final answer: $OUT/last.md"
