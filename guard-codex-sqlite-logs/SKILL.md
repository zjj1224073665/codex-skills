---
name: guard-codex-sqlite-logs
description: Diagnose, stop, verify, and reverse excessive Codex writes to logs_2.sqlite and its WAL. Use when Codex CLI, Desktop, or IDE processes cause sustained disk writes, SSD-wear concerns, UI lag, a large ~/.codex/logs_2.sqlite-wal, unexpected TRACE logging despite RUST_LOG, or when a user asks to install or remove the block_log_inserts SQLite trigger.
---

# Guard Codex SQLite Logs

Use `scripts/codex_sqlite_log_guard.sh` for repeatable diagnostics and trigger management. Preserve normal session/state databases and modify only the `logs` table trigger in `logs_2.sqlite`.

## Workflow

1. Run `status` before changing anything:

   ```bash
   scripts/codex_sqlite_log_guard.sh status
   ```

2. Explain the evidence. Distinguish retained file size from write activity: SQLite may reuse a fixed-size WAL while repeatedly inserting and pruning rows. Treat `TRACE` share, `sqlite_sequence`, WAL metadata, open processes, and a timed sample as separate signals.

3. Obtain user authorization before `block` or `unblock`. Do not copy a multi-gigabyte diagnostic database merely as a precaution unless the user requests it; that creates the write load being avoided. The database is not canonical conversation history, but diagnostic rows can contain protocol payloads or conversation-derived content.

4. Block inserts when authorized:

   ```bash
   scripts/codex_sqlite_log_guard.sh block
   ```

   This creates an idempotent `BEFORE INSERT` trigger using `RAISE(IGNORE)`. It disables persisted feedback logs but does not disable normal Codex session and state writes.

5. Verify over an active-use window:

   ```bash
   scripts/codex_sqlite_log_guard.sh verify --seconds 20
   ```

   Confirm the trigger remains present and `MAX(id)`, `sqlite_sequence`, and WAL metadata stay unchanged. A quiet system cannot demonstrate avoided writes, but trigger presence guarantees matching inserts are ignored.

6. Report the exact result and caveats:
   - Codex updates or database recreation can remove the trigger.
   - Existing database and WAL space is not reclaimed by the trigger.
   - Do not run `VACUUM`, delete `*-wal`/`*-shm`, or force a checkpoint while Codex processes hold the database open. Treat cleanup as a separate, explicitly authorized operation after all Codex processes are closed.

7. Remove the workaround only when authorized:

   ```bash
   scripts/codex_sqlite_log_guard.sh unblock
   ```

## Database Location

The script defaults to:

```text
${CODEX_SQLITE_HOME:-${CODEX_HOME:-$HOME/.codex}}/logs_2.sqlite
```

Use `--db /absolute/path/logs_2.sqlite` when `sqlite_home` in `config.toml` overrides the environment or when inspecting a fixture.

## Interpretation Guardrails

- `5 MiB/s` sustained for one year is about `165 TB`, not `640 TB`; state units and assumptions explicitly.
- Linux `/proc/<pid>/io` measures process-level writes, while block-device counters cover the entire device. Neither is lifetime NVMe SMART TBW.
- A TBW rating is a warranty endurance threshold, not an exact instant-of-failure point.
- Never assume `/tmp` is memory-backed. Verify with `findmnt -T /tmp` on Linux or the platform equivalent before recommending tmpfs.
- `RUST_LOG=warn` may not suppress a separately filtered SQLite sink; inspect database contents and behavior rather than assuming the environment variable is sufficient.

## Script Actions

- `status`: inspect file sizes, trigger state, log-level distribution, SQLite page/freelist data, IDs, and open processes.
- `block`: create `block_log_inserts` after validating the `logs` table.
- `verify`: compare IDs and WAL metadata across a timed interval.
- `unblock`: drop only `block_log_inserts`.

If `sqlite3` is unavailable, report that prerequisite and request authorization before installing packages.
