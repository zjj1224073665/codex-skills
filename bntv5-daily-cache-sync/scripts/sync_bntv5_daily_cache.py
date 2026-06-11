#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_CACHE_DIR = Path(
    "data/binance_trades_v5/daily/sample1T_1T5T1h/spot/BTCUSDT"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Holt bntv5 open_time rows into daily parquet cache files."
    )
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--market", default="SPOT")
    parser.add_argument("--db-name", default="clickhouse_spider")
    parser.add_argument("--holt-common-lib-path", type=Path)
    parser.add_argument("--start-dt", help="Inclusive open_time start. Defaults to latest local timestamp + 1 minute.")
    parser.add_argument("--end-dt", help="Exclusive open_time end. Defaults to latest ClickHouse open_time + 1 minute.")
    parser.add_argument("--schema-file", type=Path, help="Parquet file whose columns define output order.")
    parser.add_argument(
        "--drop-column",
        action="append",
        default=["is_warmup"],
        help="Column to omit from newly written files. Can be repeated.",
    )
    parser.add_argument("--columns-per-query", type=int, default=150)
    parser.add_argument("--compression", default="snappy")
    parser.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="Let ClickHouse rows replace existing local timestamps. Default keeps local rows.",
    )
    return parser.parse_args()


def ensure_holt_common_lib(path: Path | None) -> None:
    lib_path = path or os.environ.get("HOLT_COMMON_LIB_PATH")
    if lib_path:
        p = Path(lib_path).expanduser().resolve()
        if not p.exists():
            raise SystemExit(f"HOLT common_lib path does not exist: {p}")
        sys.path.insert(0, str(p))
        cfg_dir = p / "config"
        if cfg_dir.exists():
            os.environ.setdefault("BASEUTIL_CONFIG_PATH", str(cfg_dir))
    try:
        import common_lib  # noqa: F401
    except Exception as exc:
        raise SystemExit(
            "Could not import Holt common_lib. Set PYTHONPATH, HOLT_COMMON_LIB_PATH, "
            "or pass --holt-common-lib-path."
        ) from exc


def to_utc_naive(value: str | pd.Timestamp) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tzinfo is not None:
        ts = ts.tz_convert("UTC").tz_localize(None)
    return ts


def existing_files(cache_dir: Path) -> list[Path]:
    files = sorted(cache_dir.glob("*_features.parquet"))
    if not files:
        raise SystemExit(f"no *_features.parquet files in {cache_dir}")
    return files


def canonical_columns(schema_file: Path, drop_columns: Iterable[str]) -> list[str]:
    cols = pd.read_parquet(schema_file).columns.tolist()
    drop = set(drop_columns)
    out = [c for c in cols if c not in drop]
    if not out:
        raise SystemExit(f"schema file has no output columns after drop: {schema_file}")
    return out


def schema_columns(schema_file: Path) -> list[str]:
    cols = pd.read_parquet(schema_file).columns.tolist()
    if not cols:
        raise SystemExit(f"schema file has no columns: {schema_file}")
    return cols


def chunks(values: list[str], size: int) -> Iterable[list[str]]:
    if size <= 0:
        raise SystemExit("--columns-per-query must be positive")
    for start in range(0, len(values), size):
        yield values[start : start + size]


def read_chunk(
    *,
    read_bntv5_features,
    from_dt: pd.Timestamp,
    end_dt: pd.Timestamp,
    symbol: str,
    market: str,
    db_name: str,
    columns: list[str],
) -> pd.DataFrame:
    df = read_bntv5_features(
        from_dt=from_dt,
        end_dt=end_dt,
        symbols=[symbol],
        market=market,
        columns=columns,
        db_name=db_name,
        include_availability_time=False,
        include_metadata=False,
        coerce_numeric=True,
    )
    if df.empty:
        raise SystemExit(f"ClickHouse returned empty frame for columns {columns[:5]}")
    if "open_time" not in df.columns or "symbol" not in df.columns:
        raise SystemExit("Holt reader result must contain open_time and symbol")
    df["open_time"] = pd.to_datetime(df["open_time"], utc=True).dt.tz_convert("UTC").dt.tz_localize(None)
    df = df.sort_values("open_time", kind="mergesort")
    df = df.drop_duplicates(subset=["open_time"], keep="last")
    df = df.set_index("open_time").sort_index()
    df.index = pd.DatetimeIndex(df.index, name="dt")
    return df.loc[:, columns]


def read_existing_window(
    *,
    cache_dir: Path,
    start: pd.Timestamp,
    latest_open: pd.Timestamp,
    columns: list[str],
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    day = start.normalize()
    last_day = latest_open.normalize()
    while day <= last_day:
        path = cache_dir / f"{day.date()}_features.parquet"
        if path.exists():
            part = pd.read_parquet(path)
            part.index = pd.DatetimeIndex(part.index, name="dt")
            available = [c for c in columns if c in part.columns]
            if available:
                frames.append(part.loc[:, available])
        day += pd.Timedelta(days=1)
    if not frames:
        return pd.DataFrame(columns=columns)
    out = pd.concat(frames).sort_index()
    out = out[~out.index.duplicated(keep="last")]
    out = out.loc[(out.index >= start) & (out.index <= latest_open)]
    for col in columns:
        if col not in out.columns:
            out[col] = np.nan
    return out.loc[:, columns]


def source_missing_minutes(
    df: pd.DataFrame,
    *,
    start: pd.Timestamp,
    latest_open: pd.Timestamp,
) -> pd.DatetimeIndex:
    expected = pd.date_range(start, latest_open, freq="1min", name="dt")
    missing = expected.difference(df.index)
    extra = df.index.difference(expected)
    if len(extra):
        raise SystemExit(
            "remote index has timestamps outside the expected 1T window: "
            f"extra={len(extra)} first_extra={extra[:5].tolist()}"
        )
    return missing


def repair_missing_minutes_from_spot_kline(
    df: pd.DataFrame,
    missing: pd.DatetimeIndex,
    *,
    symbol: str,
    market: str,
    db_name: str,
    columns: list[str],
) -> pd.DataFrame:
    """Fill missing bntv5 rows without inventing close prices.

    The feature table occasionally misses complete 1T rows even though Binance
    spot kline has the true bar.  For those rows we copy non-price feature
    values from the most recent previous *original* non-missing bntv5 row, then
    overwrite the 1T price columns with true kline open/close.
    """
    if len(missing) == 0:
        return df
    if df.empty:
        raise SystemExit("cannot repair missing bntv5 rows without a previous row")

    market_type = "spot" if str(market).upper() == "SPOT" else "swap"
    from common_lib.io.clickhouse_io import read_binance_kline

    kline_start = pd.Timestamp(missing.min())
    kline_end = pd.Timestamp(missing.max()) + pd.Timedelta(minutes=1)

    kline_frames: dict[str, pd.DataFrame] = {}
    for field in ("open", "close"):
        if f"1T_{field}_price" not in columns:
            continue
        frame = read_binance_kline(
            from_dt=str(kline_start),
            end_dt=str(kline_end),
            field=field,
            interval="1m",
            symbols=[symbol],
            market_type=market_type,
            db_name=db_name,
        )
        if frame.empty:
            raise SystemExit(f"spot kline query returned empty for field={field}")
        kline_frames[field] = frame

    original_index = pd.DatetimeIndex(df.index).sort_values()
    base = df.sort_index()
    additions: list[pd.Series] = []
    addition_index: list[pd.Timestamp] = []
    repair_log: list[str] = []

    for ts in pd.DatetimeIndex(missing).sort_values():
        pos = original_index.searchsorted(ts, side="left") - 1
        if pos < 0:
            raise SystemExit(f"cannot repair {ts}: no previous non-missing bntv5 row")
        prev_ts = original_index[pos]
        row = base.loc[prev_ts, columns].copy()

        for field, price_col in (("open", "1T_open_price"), ("close", "1T_close_price")):
            if price_col not in columns:
                continue
            kline = kline_frames[field]
            kline_col = symbol if symbol in kline.columns else kline.columns[0]
            if ts not in kline.index or pd.isna(kline.at[ts, kline_col]):
                raise SystemExit(f"spot kline missing {field} for {ts}")
            row[price_col] = float(kline.at[ts, kline_col])

        additions.append(row)
        addition_index.append(ts)
        repair_log.append(
            f"{ts}<-features:{prev_ts} "
            f"open={row.get('1T_open_price', 'NA')} "
            f"close={row.get('1T_close_price', 'NA')}"
        )

    repaired = pd.concat(
        [
            base,
            pd.DataFrame(additions, index=pd.DatetimeIndex(addition_index, name="dt")),
        ]
    ).sort_index()
    repaired = repaired[~repaired.index.duplicated(keep="last")]
    repaired.index = pd.DatetimeIndex(repaired.index, name="dt")
    print(
        f"source_missing_minutes_repaired={len(addition_index)} "
        f"details={repair_log[:20]}",
        flush=True,
    )
    return repaired.loc[:, columns]


def coerce_float64(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.loc[:, columns].copy()
    for col in columns:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("float64")
    if np.isinf(out.to_numpy(dtype="float64", copy=False)).any():
        raise SystemExit("remote data contains inf/-inf")
    return out


def latest_local_timestamp(cache_dir: Path) -> pd.Timestamp:
    for path in reversed(existing_files(cache_dir)):
        df = pd.read_parquet(path)
        if df.empty:
            continue
        idx = pd.DatetimeIndex(df.index)
        return pd.Timestamp(idx.max())
    raise SystemExit(f"no local timestamps found in {cache_dir}")


def read_existing_day(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=columns)
    df = pd.read_parquet(path)
    df.index = pd.DatetimeIndex(df.index, name="dt")
    for col in columns:
        if col not in df.columns:
            df[col] = np.nan
    return coerce_float64(df.loc[:, columns], columns)


def write_daily_files(
    *,
    cache_dir: Path,
    df: pd.DataFrame,
    start_day: pd.Timestamp,
    latest_open: pd.Timestamp,
    columns: list[str],
    final_columns: list[str],
    compression: str,
    overwrite_existing: bool,
) -> list[tuple[str, int, str, str, int]]:
    written: list[tuple[str, int, str, str, int]] = []
    day = start_day.normalize()
    last_day = latest_open.normalize()
    while day <= last_day:
        day_end = day + pd.Timedelta(days=1)
        file_end = min(day_end, latest_open)
        out = cache_dir / f"{day.date()}_features.parquet"
        old = read_existing_day(out, columns)
        new_part = df.loc[(df.index >= day) & (df.index <= file_end), columns].copy()
        frames = [old, new_part] if overwrite_existing else [new_part, old]
        combined = pd.concat(frames).sort_index()
        combined = combined[~combined.index.duplicated(keep="last")]
        part = combined.loc[(combined.index >= day) & (combined.index <= file_end), columns].copy()
        for col in final_columns:
            if col not in part.columns:
                if col == "is_warmup":
                    if out.exists():
                        existing_col = pd.read_parquet(out, columns=[col])
                        existing_col.index = pd.DatetimeIndex(existing_col.index, name="dt")
                        part[col] = existing_col[col].reindex(part.index).fillna(False).astype(bool)
                    else:
                        part[col] = False
                else:
                    raise SystemExit(f"cannot write {out.name}: missing final schema column {col}")
        part = part.loc[:, final_columns]
        part.index = pd.DatetimeIndex(part.index, name="dt")
        tmp = cache_dir / f".{day.date()}_features.parquet.tmp"
        part.to_parquet(tmp, engine="pyarrow", compression=compression, index=True)
        tmp.replace(out)
        written.append(
            (out.name, len(part), str(part.index.min()), str(part.index.max()), len(part.columns))
        )
        day += pd.Timedelta(days=1)
    return written


def main() -> int:
    args = parse_args()
    ensure_holt_common_lib(args.holt_common_lib_path)
    from common_lib.io import latest_bntv5_open_time, read_bntv5_features

    cache_dir = args.cache_dir
    files = existing_files(cache_dir)
    schema_file = args.schema_file or files[-1]
    final_columns = schema_columns(schema_file)
    columns = canonical_columns(schema_file, args.drop_column)

    if args.start_dt:
        start_dt = to_utc_naive(args.start_dt)
    else:
        start_dt = latest_local_timestamp(cache_dir) + pd.Timedelta(minutes=1)

    if args.end_dt:
        end_dt = to_utc_naive(args.end_dt)
        latest_open = end_dt - pd.Timedelta(minutes=1)
    else:
        latest = latest_bntv5_open_time(
            symbols=[args.symbol],
            market=args.market,
            db_name=args.db_name,
        )
        if latest is None:
            raise SystemExit("ClickHouse returned no latest open_time")
        latest_open = to_utc_naive(latest)
        end_dt = latest_open + pd.Timedelta(minutes=1)

    if latest_open < start_dt:
        print(f"nothing_to_sync=true latest_open_time={latest_open} start={start_dt}", flush=True)
        return 0

    print(f"cache_dir={cache_dir}", flush=True)
    print(f"schema_file={schema_file}", flush=True)
    print(f"window=[{start_dt}, {end_dt}) latest_open_time={latest_open}", flush=True)
    print(f"output_columns={len(columns)} drop_columns={sorted(set(args.drop_column))}", flush=True)

    pieces: list[pd.DataFrame] = []
    base_index: pd.DatetimeIndex | None = None
    for idx, cols in enumerate(chunks(columns, args.columns_per_query), start=1):
        print(f"query_chunk={idx} columns={len(cols)} first={cols[0]} last={cols[-1]}", flush=True)
        part = read_chunk(
            read_bntv5_features=read_bntv5_features,
            from_dt=start_dt,
            end_dt=end_dt,
            symbol=args.symbol,
            market=args.market,
            db_name=args.db_name,
            columns=cols,
        )
        if base_index is None:
            base_index = part.index
        elif not part.index.equals(base_index):
            raise SystemExit(f"index mismatch in query chunk {idx}")
        pieces.append(part)

    remote = pd.concat(pieces, axis=1)
    remote = coerce_float64(remote, columns)
    if not args.overwrite_existing:
        existing = read_existing_window(cache_dir=cache_dir, start=start_dt, latest_open=latest_open, columns=columns)
        if not existing.empty:
            remote_only = remote.loc[~remote.index.isin(existing.index)]
            remote = pd.concat([existing, remote_only]).sort_index()
            remote = coerce_float64(remote, columns)
    missing = source_missing_minutes(remote, start=start_dt, latest_open=latest_open)
    if len(missing):
        remote = repair_missing_minutes_from_spot_kline(
            remote,
            missing,
            symbol=args.symbol,
            market=args.market,
            db_name=args.db_name,
            columns=columns,
        )
        missing_after = source_missing_minutes(remote, start=start_dt, latest_open=latest_open)
        if len(missing_after):
            raise SystemExit(
                f"missing minutes remain after kline repair: "
                f"{len(missing_after)} first_missing={missing_after[:10].tolist()}"
            )

    written = write_daily_files(
        cache_dir=cache_dir,
        df=remote,
        start_day=start_dt.normalize(),
        latest_open=latest_open,
        columns=columns,
        final_columns=final_columns,
        compression=args.compression,
        overwrite_existing=args.overwrite_existing,
    )
    print("written_files:", flush=True)
    for item in written:
        print(item, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
