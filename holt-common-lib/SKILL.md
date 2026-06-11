---
name: holt-common-lib
description: Use when working with /home/junjiezhao/Documents/holt_common_lib, including its ClickHouse db_config/paths setup, Binance/Glassnode data readers, legacy factor/performance utilities, Alpha Center tables, or workflows to register, sync, evaluate, query, or debug any alpha/factor in Holt's Alpha Center.
---

# Holt Common Lib

## Core Rule

Treat `/home/junjiezhao/Documents/holt_common_lib` as a shared strategy utility library. It is not tied to any single strategy project.

When this skill is used, first inspect the local library and its README. Do not rely on copied examples as the source of truth when the code is available.

Before importing it from another repo, set:

```bash
export PYTHONPATH=/home/junjiezhao/Documents/holt_common_lib
export MPLCONFIGDIR=/tmp/matplotlib
```

Do not print, commit, or expose `config/db_config.yml`; it contains real credentials and is gitignored.

## Local Setup Notes

- The active local repo is `/home/junjiezhao/Documents/holt_common_lib`.
- The local `config/paths.yml` should normally point `config_path` at `/home/junjiezhao/Documents/holt_common_lib/config`, so the library reads `/home/junjiezhao/Documents/holt_common_lib/config/db_config.yml`.
- On this machine, `config/db_config.yml` is expected to exist as a private gitignored file. Treat its contents as sensitive.
- ClickHouse connections use the native driver path in `common_lib/io/clickhouse_io.py` and normally connect to port `9000`.
- As of the last smoke test, the local ClickHouse config used the company public ClickHouse endpoint and `SELECT 1` succeeded for the configured ClickHouse keys. Re-test instead of assuming if behavior changes.

## Connection Diagnosis

When the user asks whether the database is configured or why ClickHouse does not connect, check in this order:

1. Confirm `config/db_config.yml` exists, is gitignored, and has the expected database keys without printing secrets.
2. Confirm each needed key has `host`, `port`, `user`, `password`, and `database`; report only key presence and endpoint/port if needed.
3. Confirm the code is reading the intended config path via `BaseUtil` / `config/paths.yml`.
4. Test DNS resolution for the endpoint.
5. Test TCP connectivity to the endpoint and port.
6. Run a minimal ClickHouse query such as `SELECT 1` and optionally `SELECT currentDatabase()`.

Interpretation:

- DNS failure: local/network DNS problem or endpoint typo.
- TCP timeout/refused before authentication: network path, firewall, security group, IP whitelist, wrong endpoint, or wrong port.
- Authentication/permission error: credentials or database/user grants.
- Successful `SELECT 1`: the basic connection is usable; test a small reader next.

## Primary Reference

Read `references/holt-common-lib-readme.md` for the library overview, core APIs, config rules, Alpha Center notes, examples, and migration mapping. It is copied from `/home/junjiezhao/Documents/holt_common_lib/README.md`.

If the copied reference seems stale, read the live README at `/home/junjiezhao/Documents/holt_common_lib/README.md` and inspect the implementation directly.

## Use For

- Data readers in `common_lib.io`, including Binance kline, funding, metrics, sweep/trades features, universe masks, and Glassnode.
- Legacy Holt factor, signal, and performance utilities.
- Alpha Center / Factor Repository workflows with `AlphaRepo` or `AlphaCenterClient`.
- Adapting outputs from another research repo into Holt's repository format.

## Safety Checks

- Never add `config/db_config.yml` to git.
- Check `git status --short --ignored` if touching config.
- Preserve the source strategy's intended frequency and execution semantics when moving signals into Alpha Center.
- Confirm signal and close DataFrame shape before writing: wide `pd.DataFrame`, `index=time`, `columns=symbol`, `values=float`.
- If writing to ClickHouse or Alpha Center, validate with a small read-back and clean up temporary smoke-test rows.

## 策略meta命名
策略meta命名必须是 alpha_zjj_ts或者cs（就是时序或者截面）_BTCUSDT（币种，除了BTC也可以是其他的）_uptrendpullback1T（策略名）