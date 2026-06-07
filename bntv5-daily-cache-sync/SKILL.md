---
name: bntv5-daily-cache-sync
description: Sync 1T bntv5 feature rows from Holt common_lib / ClickHouse into this project's daily parquet cache format, especially data/binance_trades_v5/daily/sample1T_1T5T1h/spot/SYMBOL; use when asked to update latest local BTCUSDT/ETHUSDT spot data, preserve canonical column order, or backfill ClickHouse open_time windows.
---

# BNTV5 Daily Cache Sync

Use this skill when updating the local 1T feature parquet cache from Holt
common_lib / ClickHouse.

## Key Rules

- Prefer Holt common_lib:
  `common_lib.io.read_bntv5_features` and `latest_bntv5_open_time`.
- Holt readers return `open_time` semantics. Do not subtract one minute.
- Only subtract one minute when reading raw `spider.bntv5_features.timestamp_ms`
  directly.
- Final parquet index must be UTC tz-naive `DatetimeIndex(name="dt")`.
- Use the existing local parquet schema as canonical column order.
- ClickHouse has missing 1T minutes sometimes. This is normal. Do not fill
  those gaps from ClickHouse, do not reindex to create fake rows, and do not
  ffill/bfill/interpolate missing feature rows.
- Existing local rows may include user-repaired values. Never use ClickHouse to
  overwrite an existing local timestamp unless the user explicitly asks.
- Daily files in this project often include both endpoints: a full UTC day has
  `00:00` through next-day `00:00`, so 1441 rows. Files sourced only from
  ClickHouse may have fewer rows when ClickHouse has missing minutes or the
  current day is incomplete.
- Write through a temp file and atomically replace the target parquet.
- Do not print ClickHouse credentials or config contents.

## Workflow

1. Inspect the target cache directory and find the latest
   `YYYY-MM-DD_features.parquet`.
2. Read its columns as canonical schema.
3. Query `latest_bntv5_open_time(symbols=[symbol], market=market)`.
4. By default, read from the latest existing local timestamp plus one minute,
   through `latest_open_time + 1 minute`. This avoids using ClickHouse to
   rewrite user-repaired local history.
5. For wide all-feature syncs, query in column chunks and join by `open_time`.
6. Upsert by timestamp with local rows winning over remote rows.
7. Report ClickHouse missing minutes for audit only. Do not fill them.
8. Write one parquet per affected day:
   `YYYY-MM-DD_features.parquet`.
9. Re-read written files and verify row counts, index name/range.

## Script

Run the bundled script from the repo root:

```bash
python scripts/sync_bntv5_daily_cache.py \
  --cache-dir data/binance_trades_v5/daily/sample1T_1T5T1h/spot/BTCUSDT \
  --symbol BTCUSDT \
  --market SPOT \
  --holt-common-lib-path /path/to/holt_common_lib \
  --db-name clickhouse_spider \
```

If the target data directory is permission-restricted, rerun with approved
filesystem/network permissions rather than changing the cache format.
