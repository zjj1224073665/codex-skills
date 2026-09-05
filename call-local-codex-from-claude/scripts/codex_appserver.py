#!/usr/bin/env python3
"""Method 4: drive `codex app-server` (v2 JSON-RPC over stdio). Browser plugin disabled so the
model uses the built-in web_search tool instead of asking a human for Chrome permission.
Usage: codex_appserver.py PROMPT_FILE OUT_DIR [MODEL] [EFFORT]"""
import json, subprocess, sys, time, os
prompt_file, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "gpt-5.6-luna"
effort = sys.argv[4] if len(sys.argv) > 4 else "xhigh"
os.makedirs(out, exist_ok=True)
prompt = open(prompt_file).read()
p = subprocess.Popen(["codex", "app-server", "--listen", "stdio://",
                      "--disable", "browser_use", "--disable", "browser_use_external",
                      "-c", 'web_search="live"', "-c", "sandbox_workspace_write.network_access=true"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=open(f"{out}/stderr.log", "w"), text=True)
log = open(f"{out}/events.jsonl", "w"); rid = 0; last = ""
def send(o): p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()
def req(method, params):
    global rid; rid += 1; send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params}); return rid
def handle(m):
    global last
    meth = m.get("method"); pr = m.get("params", {})
    if meth == "item/completed" and pr.get("item", {}).get("type") == "agentMessage":
        last = pr["item"].get("text", "")
    if meth and "id" in m and meth.endswith(("Approval", "approval")):  # server->client request: decline
        send({"jsonrpc": "2.0", "id": m["id"], "result": {"decision": "decline"}})
def wait(id_):
    while True:
        line = p.stdout.readline()
        if not line: raise SystemExit("app-server exited; see stderr.log")
        log.write(line); log.flush(); m = json.loads(line)
        if m.get("id") == id_: return m
        handle(m)
wait(req("initialize", {"clientInfo": {"name": "bridge", "title": "bridge", "version": "0.1"}}))
send({"jsonrpc": "2.0", "method": "initialized"})
t0 = time.time()
r = wait(req("thread/start", {"cwd": os.getcwd(), "model": model, "sandbox": "workspace-write",
                              "approvalPolicy": "never", "approvalsReviewer": "auto_review"}))
tid = r["result"]["thread"]["id"]
wait(req("turn/start", {"threadId": tid, "input": [{"type": "text", "text": prompt}], "effort": effort}))
while True:
    line = p.stdout.readline()
    if not line: break
    log.write(line); log.flush(); m = json.loads(line); handle(m)
    if m.get("method") == "turn/completed":
        print("turn status:", m["params"]["turn"].get("status")); break
open(f"{out}/last.md", "w").write(last)
print(f"thread={tid} done in {time.time()-t0:.0f}s -> {out}/last.md")
p.terminate()
