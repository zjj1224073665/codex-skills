# holt_common_lib

策略基础依赖库，提供常用的数据读取、因子/信号生成、绩效评估与数据库工具，适配上云与多环境配置。

## 功能说明
- 数据读取与处理：Postgres / ClickHouse / 本地 parquet 的宽表读取（`time x symbol`）、基础清洗与对齐。
- 资金费率读取：Binance funding rate 宽表读取（1h/8h）与本地缓存拼接。
- 因子/信号：CS 因子计算、因子 -> 信号（归一化/极值/偏多偏空等）。
- 因子中心：Alpha 元信息注册、信号入库、PnL 计算、绩效快照与 dashboard 查询。
- 绩效评估：日频/高频回测曲线、组合指标、集中度与相关性分析。
- 数据库工具：PostgreSQL 表结构同步、追加写入、索引创建；ClickHouse 客户端封装与批量写入。
- Glassnode：指标宽表读取，以及抓取需求 `_metadata` 的提交/查询。
- 配置化：路径与数据库配置通过 `config/` 与环境变量管理，减少硬编码与环境耦合。

## 因子中心
- 因子中心对应项目中的 Alpha Center / Factor Repository，核心代码在 `common_lib/alpha/alpha_repo.py` 和 `common_lib/io/clickhouse_alpha_center.py`。
- 目标是把一个 alpha 的完整生命周期沉淀到统一仓库：`register -> sync_signal -> calc_and_write_pnl -> calc_and_write_performance -> get_dashboard`。
- 主要表包括：`t_alpha_meta`（元信息）、`t_alpha_signal`（非零信号和 close）、`t_alpha_pnl`（小时级 PnL 分解）、`t_alpha_performance`（绩效快照）。
- 约定上，研究侧信号使用宽表 `index=time, columns=symbol, values=float`，常用 symbol 形态为 `BTCUSDT`；入库时会自动转成 repo 内部 symbol，并把 `candle_begin_time` 转成 `position_time`。
- 支持的 metadata frequency 为 `1h`、`5min`、`1min`；其中高频 alpha 的本地存储需要注意 `AlphaStorage` 默认会按 `1h` 重采样。
- 示例 notebook 见 `examples/new_alpha_onboarding.ipynb`，包含新因子定义、本地保存、元信息注册、信号同步、PnL/绩效计算和 dashboard 查询的完整流程。

## 核心约定（因子迁移时最常踩坑）
- 时间：统一以 UTC 读写，并在 pandas 中落地为 tz-naive 的 `DatetimeIndex`（常见做法是 `tz_localize(None)`）。
- 形状：大部分 reader 返回 `pd.DataFrame`，`index=time`，`columns=symbol`，`values=float`（缺失为 NaN）。
- Symbol：统一到 `BTCUSDT` 形式；会处理 `BTC-USDT`、`BINANCE_SPOT_*`、`BINANCE_SWAP_*`、`1000PEPE*` 等命名（见 `common_lib/utils/symbols.py`）。
- 缺失值：多数 reader 默认 `ffill` 且带 `ffill_limit`；常见黑名单 `BOBUSDT` 会被过滤。

## 目录结构
```
common_lib/
  alpha/     # AlphaBase / AlphaStorage（信号存储、增量更新）
  io/        # 数据库/文件 I/O
  calc/      # 通用计算与工具函数
  factors/   # 因子/信号逻辑
  eval/      # 绩效评估
  utils/     # 基础工具（BaseUtil）
config/      # 路径与数据库配置
```

## 核心 API（因子迁移常用入口）
| 场景 | API（新库推荐入口） | 备注 |
| --- | --- | --- |
| 环境/路径 | `from BaseUtil import baseutil as BU` | 读取 `config/paths.yml` + 环境变量覆盖 |
| Binance Kline（CH，通用） | `from common_lib.io import read_binance_kline` | `market_type=spot/swap`；支持 1m/5m/1h 等 |
| Binance Future Kline（CH，直读 5m/1h） | `common_lib/io/clickhouse_binance_kline_io.py:read_binance_future_kline` | 直接读 `t_binance_future_kline`，`argMax` 去重 |
| Binance Metrics（CH） | `from common_lib.io import read_binance_metrics` | 读 `t_binance_metrics`；支持 `ignore_zero=True` |
| Binance Funding Rate（CH） | `from common_lib.io import read_binance_funding_rate` | 读 `t_binance_funding_rate`；支持 `1h/8h` 与本地缓存 |
| Trades Raw Features（CH，1h） | `from common_lib.io import read_binance_trades_feature_wide_1h` | 传入 legacy PG feature 名（如 `spot_all_sell_sum`） |
| Trades Raw Features（CH，批量） | `from common_lib.io import read_binance_trades_features_wide_1h_batch` | 复用同一个 CH client，减少重复连接 |
| Sweep Features（CH，宽表） | `from common_lib.io import read_sweep_features_wide_one / read_sweep_features_wide_batch` | offline 名 -> realtime 列名映射内置 |
| Universe Mask（CH） | `from common_lib.io import UniverseMaskLoader` | member-rows 模型；返回宽表（`time x symbol`） |
| Glassnode（CH） | `from common_lib.io import read_glassnode_metric` | 指标宽表读取（支持 list assets/coins/v_cols） |
| Glassnode 需求（_metadata） | `submit_glassnode_request(s) / list_glassnode_requests` | 提交或查询抓取需求 |
| 因子计算（trades CS） | `common_lib/factors/CS_func.py:tradesCSFactorCalculatorBinance` | `data_source` 支持 `clickhouse/pgsql/nas` 等 |
| 因子 -> 信号 | `common_lib/factors/CS_func.py:Factor2Sig` | vanilla / extreme / focus_on_top/bottom |
| 评估（日频） | `common_lib/eval/performance_eval.py:draw_curve / PortfolioMetrics` | 适用于 1h 信号 |
| 评估（高频） | `common_lib/eval/performance_eval_hf.py:draw_curve_hf / PortfolioMetrics` | 适用于 5T/5m 信号 |
| Alpha 存储 | `from common_lib.alpha import AlphaBase, AlphaStorage` | `append`/`upsert` 支持滚动窗口重算 |

## 新老代码映射关系
为保持兼容性，顶层文件仍可按旧路径导入，内部已转到新包结构。

| 旧入口 | 新位置 |
| --- | --- |
| `BaseUtil.py` | `common_lib/utils/baseutil.py` |
| `functions.py` | `common_lib/calc/functions.py` |
| `CS_func.py` | `common_lib/factors/CS_func.py` |
| `db_func.py` | `common_lib/io/db_func.py` |
| `performance_eval.py` | `common_lib/eval/performance_eval.py` |
| `performance_eval_hf.py` | `common_lib/eval/performance_eval_hf.py` |

## 老环境功能 -> 新库对应关系（面向因子迁移）
这里的“老环境”主要指旧代码习惯从顶层 `functions.py / CS_func.py / db_func.py` 直接调用；新库仍保留兼容导入，但推荐在迁移代码里直接引用 `common_lib.*` 的实现位置，避免混淆数据源与行为差异。

| 老环境常见用法（兼容仍可用） | 新库推荐入口 | 说明 |
| --- | --- | --- |
| `from functions import read_bn_basic / read_bn_basic_nas` | `common_lib/io/db_func.py:read_bn_basic / read_bn_basic_nas` | 读取 legacy `basic_1h` 宽表（PG 或 NAS parquet） |
| `from functions import read_bn_basic_5T / read_bn_basic_5T_nas` | `common_lib/io/db_func.py:read_bn_basic_5T / read_bn_basic_5T_nas` | 读取 legacy `basic_5T` 宽表 |
| `from functions import read_binance_trades_features(_nas)` | `common_lib/io/db_func.py:read_binance_trades_features(_nas)` | 旧 trades features 宽表读法（PG/NAS）；推荐迁移到 CH raw features 见下一行 |
| `read_binance_trades_features_*`（以 trades raw 特征为输入） | `common_lib/io/clickhouse_binance_trades_features_io.py:read_binance_trades_feature_wide_1h` | ClickHouse `features` 表：按 legacy PG name 映射到 CH 列名，输出 1h 宽表 |
| `read_binance_trades_features_combine_pgch` | `common_lib/io/db_func.py:read_feature_wide_1h_mixed_pg_ch` | 过渡期 PG+CH 拼接读取（按 cut 时间分段） |
| `read_ch_feature_wide_1h_on_the_hour` | `common_lib/io/clickhouse_binance_trades_features_io.py:read_binance_trades_feature_wide_1h` | 推荐使用更明确的 trades raw reader（同语义：整点快照 -> candle_begin_time） |
| `tradesCSFactorCalculatorBinance(..., data_source='nas'/'pgsql_old')` | `... data_source='clickhouse' 或 'pgsql'` | 新环境优先 ClickHouse；`pgsql` 为 PG+CH 混合过渡读法 |
| `MaskLoader(mask_dir=... parquet)` | `common_lib/io/clickhouse_universe_io.py:MaskLoader` | Universe 上云：member-rows 模型（CH），返回宽表（也可 `from common_lib.io import UniverseMaskLoader`） |
| `from functions import clean_symbol / align_signals_to_binance` | `common_lib/utils/symbols.py` | 统一 symbol 命名与信号对齐（建议迁移时显式调用） |
| `from performance_eval import draw_curve` | `common_lib/eval/performance_eval.py:draw_curve` | 日频/小时级信号回测曲线 |
| `from performance_eval_hf import draw_curve_hf` | `common_lib/eval/performance_eval_hf.py:draw_curve_hf` | 高频（5T/5m）信号回测曲线 |

## 配置说明
- `config/paths.yml`：路径配置（`root_path`、`input_path`、`output_path` 等）
- `config/db_config.yml`：数据库配置（本地私有文件，包含敏感信息，已在 `.gitignore` 中忽略，禁止提交到 git）
- `config/db_config.example.yml`：占位示例配置（可提交），使用方法：复制为 `config/db_config.yml`，然后去问 holt 获取数据库连接方式/账号信息，再在本地填写或通过环境变量注入
- `config/scp_config.yml`：SCP/SFTP 远端拉数配置（本地私有文件，已在 `.gitignore` 中忽略，禁止提交到 git）
- `config/scp_config.example.yml`：SCP 配置示例（可提交），使用方法：复制为 `config/scp_config.yml` 后本地填写

支持环境变量覆盖：
```
BASEUTIL_PATHS_CONFIG=/root/holt_common_lib/config/paths.yml
BASEUTIL_ROOT_PATH=/mnt/nas/holt
BASEUTIL_CONFIG_PATH=/mnt/nas/holt/prod/config
```

## 快速使用
```python
from BaseUtil import baseutil as BU
from functions import read_bn_basic   # legacy 兼容入口（推荐迁移后改用 common_lib.* 直导入）
```

## Examples
- `examples/new_alpha_onboarding.ipynb`：新因子接入因子中心的详细示例，覆盖 `AlphaBase`、`AlphaStorage`、`AlphaRepo` 与 Alpha Center 的完整调用链。
- `examples/new_alpha_onboarding_hf.ipynb`：高频新因子接入示例，重点说明 `5min` / `1min` alpha 的本地存储、close 读取、PnL 入库和常见坑位。
- `examples/glassnode_subscription_and_reading.ipynb`：演示 Glassnode URL 需求注册、`_metadata` 查询，以及底层表落库后的本地宽表读取。
- `examples/market_features_readers.ipynb`：演示 sweep features 与 trades features 的单个和批量读取方式。
- `examples/demo_alpha_template.py`：可直接复制改造的新因子模板脚本，包含本地信号生成、因子中心注册、signal/PnL/performance 写入流程。

## 监控脚本（monitors）
- 入口：`monitors/run_all.py`（统一调度 kline / metrics / funding rate / glassnode / symbol presence）
- Webhook：通过环境变量配置，禁止硬编码
```
export HOLT_LARK_WEBHOOK="https://open.larksuite.com/open-apis/bot/v2/hook/xxxx"
python monitors/run_all.py --run-once
```

## 最近更新
- 修复 `common_lib/io/clickhouse_io.py` 中 spot 行情时间戳单位为毫秒，避免读取为空。
- 统一 kline 查询时间戳为毫秒并简化聚合逻辑。
- 增加 `5T` 作为 `5m` 的别名，便于 5 分钟级别读取。
- Glassnode 默认库切换为 `clickhouse_rds_glassnode`，并在宽表生成前对 `(t, asset)` 重复行去重。

## Glassnode 需求提交
```python
from common_lib.io import submit_glassnode_request, submit_glassnode_requests, list_glassnode_requests

url = "https://api.glassnode.com/v1/metrics/breakdowns/mvrv_by_age?a=BTC&c=native&i=1h"
submit_glassnode_request(url=url, date="2026-01-30", update_freq="1h")

items = [
    {"url": url, "date": "2026-01-30", "update_freq": "1h"},
]
submit_glassnode_requests(items)

rows = list_glassnode_requests(url_like="%/metrics/breakdowns/%", date_from="2026-01-20", limit=50)
```
