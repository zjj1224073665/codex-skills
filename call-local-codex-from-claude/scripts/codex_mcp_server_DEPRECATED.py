import json, subprocess, sys, time
SP="/private/tmp/claude-501/-Users-junjiezhao-Documents-EvoSci-papers/c3e9997c-ef6d-424a-bf26-f0b6e4561a84/scratchpad"
prompt=open(f"{SP}/prompt.md").read()
p = subprocess.Popen(["codex","mcp-server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(f"{SP}/m2_err.log","w"), text=True)
def send(o): p.stdin.write(json.dumps(o)+"\n"); p.stdin.flush()
send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"claude-code-bridge","version":"0"}}})
p.stdout.readline()
send({"jsonrpc":"2.0","method":"notifications/initialized"})
t0=time.time()
send({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"codex","arguments":{
  "prompt":prompt,"sandbox":"workspace-write","approval-policy":"never","cwd":SP,
  "config":{"sandbox_workspace_write":{"network_access":True},"web_search":"live"}}}})
log=open(f"{SP}/m2_events.jsonl","w")
while True:
    line=p.stdout.readline()
    if not line: break
    log.write(line); log.flush()
    m=json.loads(line)
    if m.get("id")==2:
        res=m.get("result",{})
        txt="\n".join(c.get("text","") for c in res.get("content",[]))
        open(f"{SP}/m2_last.md","w").write(txt)
        print("DONE in %.0fs, threadId=%s"%(time.time()-t0, res.get("structuredContent",{}).get("threadId") if isinstance(res.get("structuredContent"),dict) else None))
        break
p.terminate()
