// Method 3: @openai/codex-sdk (ESM). npm install @openai/codex-sdk  (use --cache ./npmcache if ~/.npm is not writable)
// Usage: node codex_sdk.mjs PROMPT_FILE OUT_DIR
import { Codex } from "@openai/codex-sdk";
import fs from "node:fs";
const [promptFile, out] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const thread = new Codex().startThread({
  model: "gpt-5.6-luna", modelReasoningEffort: "xhigh",
  sandboxMode: "workspace-write", workingDirectory: process.cwd(), skipGitRepoCheck: true,
  networkAccessEnabled: true, webSearchMode: "live", approvalPolicy: "never",
});
const log = fs.createWriteStream(`${out}/events.jsonl`);
const { events } = await thread.runStreamed(fs.readFileSync(promptFile, "utf8"));
let last = "";
for await (const ev of events) {
  log.write(JSON.stringify(ev) + "\n");
  if (ev.type === "item.completed" && ev.item.type === "agent_message") last = ev.item.text;
  if (ev.type === "turn.failed") console.error("FAILED", JSON.stringify(ev));
}
fs.writeFileSync(`${out}/last.md`, last);
console.log(`thread=${thread.id} -> ${out}/last.md`);
