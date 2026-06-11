# 事件强度仓位执行 profile spec 改造

请修改本 repo 的文档，范围包括下方列出的 spec 文件和 repo 根目录 `AGENTS.md`、`CLAUDE.md`。`src/` 和测试保持不变。

这是一份一次性提示词。目标是给 **事件强度因子** 补清楚执行层语义：

```text
score_raw
  -> normalization_config 生成 target_pos / position_intent
  -> 执行 profile 生成 position_raw
  -> hold_minutes 采样 / 继承生成 position_exec
  -> Backtester 使用 position_exec
```

这里的重点是 `target_pos -> position_raw -> position_exec`。`score_raw -> target_pos` 继续由 `normalization_config` 负责。

## 需要修改的文件

重点修改：

- `specs/02_position_engine.md`
- `specs/07_pipeline.md`
- `specs/04_factor_interface.md`

同步修改：

- repo 根目录 `AGENTS.md`、`CLAUDE.md`

保持不变：

- `specs/06_factor_runtime.md`
- `src/`
- 测试

原因：这次改的是 `target_pos -> position_raw -> position_exec` 的执行层语义。`specs/06_factor_runtime.md` 只负责把 `source_code` 编译成 callable、校验签名、提取 `normalization_config`。

`normalization_config` 白名单方法保持现状。本次 meta spec 不扩展 normalization method，也不新增连续超参数搜索空间。

## 背景

这次改造是给 `strategy_review_UptrendPullbackReclaim_1T_new.md` 里那类因子做基建。

这类因子更像 long-flat 下的非负事件强度：

- 因子内部已经有 rolling median、quantile、clip、event gate、EWM 等逻辑。
- `score_raw` 通常非负。
- `score_raw` 本身已经包含事件强度和平滑记忆。
- 有效仓位形态包括 0、0 到 1 之间的连续强度，以及 0 到 1 之间的分段强度。

这类因子执行后经常呈现：

```text
常驻轻仓多头 + 买盘接管事件时加仓
```

长期轻仓多头主要来自几件事叠加：

```text
非负慢衰减事件分数
  + 外层 normalization 把中等偏强状态映射成小仓位
  + long_flat 只保留正仓位
  + no-trade band 影响小幅减仓 / 清仓
  + max_step 影响退出或加仓速度
  + hold_minutes 只在目标 bar 更新真实执行仓位
```

这次 spec 需要把执行层语义说清楚：

- no-trade band 是否启用。
- max_step 是否启用。
- `target_pos == 0` 时，在不同执行口径下如何处理。
- `position_raw` 是平滑跟随 target，还是直接等于 target。
- `hold_minutes` 如何把完整 1T 的 `position_raw` 变成真实回测用的 `position_exec`。

## 目标口径

新增一个全局评估概念：

```text
position_profile
```

合法值固定为：

```text
"smooth"
"event_intensity"
```

`position_profile` 是评估级全局配置，与每个因子的 `normalization_config` 分开管理。这里说的“两种 config”就是 `position_profile` 的两个固定取值：

- `smooth`：保持当前连续强度型评估口径。
- `event_intensity`：新增事件强度直接执行口径，用来支持事件强度因子的直接执行语义。

一次 Pipeline 评估使用一个 `position_profile`。同一批因子需要比较 smooth 和 event_intensity 两种口径时，上层分别跑两次 Pipeline。

默认 profile：

```text
position_profile = "smooth"
```

## smooth profile

`smooth` 是当前连续强度型策略的默认口径。它保留当前默认的 no-trade band / max_step 执行语义，作为默认兼容口径。

语义：

```text
score_raw
  -> normalization_config 生成 target_pos
  -> no-trade band / max_step 生成完整 1T position_raw
  -> hold_minutes 采样成 position_exec
  -> Backtester 使用 position_exec
```

默认 profile 参数固定为：

```text
hold_minutes = 15
band = 0.10
max_step = 0.15
```

`hold_minutes=1` 合法，表示每根 1T bar 都是允许执行仓位变化的 bar。

`smooth` profile 下，`band` 和 `max_step` 是执行层工具，按默认 smooth 口径生成平滑的 `position_raw`。`target_pos == 0` 也按同一套 no-trade band / max_step 语义处理。

例子：

```text
current_pos = 0.05
target_pos = 0
band = 0.10

smooth 口径继续使用 no-trade band / max_step 计算下一根 position_raw。
```

也就是说：

```text
smooth profile:
  使用 no-trade band
  使用 max_step
  target_pos == 0 使用同一套平滑执行规则
```

## event_intensity profile

`event_intensity` 是事件强度因子的直接执行口径。它只决定 `target_pos -> position_raw` 的执行方式，不决定本轮评估是 long-flat 还是 long-short。

`target_pos` 支持连续或分段强度，例如：

```text
target_pos: [0.00, 0.25, 0.70, 1.00, 0.40, 0.00]
```

语义：

```text
score_raw
  -> normalization_config 生成 target_pos
  -> 完整 1T 的 position_raw 直接等于 target_pos
  -> hold_minutes 采样成 position_exec
  -> Backtester 使用 position_exec
```

也就是完整 1T 原始仓位：

```text
position_raw[t] = target_pos[t]
```

`event_intensity` profile 信任 normalization 已经给出了本分钟想要的仓位强度，执行层直接承接这个强度。

实现口径固定为：复用现有 execution rules，并由 `position_profile` 内部固定派生：

```text
band = 0
max_step = 2
```

这组参数在 `long_flat` 和 `long_short` 下都足够表达直接跟随：

- `band=0` 表示任意非零 gap 都不会被 no-trade band 挡掉。
- `max_step=2` 覆盖合法仓位范围内的最大单步跳变；`long_flat` 最大跳变是 `1`，`long_short` 最大跳变是 `2`。

因此外部语义等价于：

```text
position_raw[t] = target_pos[t]
```

规则：

- `target_pos` 支持连续或分段仓位，范围由全局 `PositionEngineConfig.mode` 决定：`long_flat` 为 `[0, 1]`，`long_short` 为 `[-1, 1]`。
- 内部等价于 `band=0`，不让 no-trade band 挡掉事件强度变化。
- 内部等价于 `max_step=2`，允许一步到达任意合法 `target_pos`。
- `target_pos == 0` 时，`position_raw` 直接为 0。
- `target_pos` 从 0.70 降到 0.25 时，`position_raw` 直接到 0.25。
- `target_pos` 从 0.25 升到 0.80 时，`position_raw` 直接到 0.80。

例子：

```text
target_pos:   [0.00, 0.25, 0.70, 0.40, 0.00]
position_raw: [0.00, 0.25, 0.70, 0.40, 0.00]
```

这里第 5 根 bar 的 `target_pos=0` 表示 normalization 已经给出退出意图。仓位直接归零。

## profile 与执行规则

no-trade band 和 max_step 不作为单独的 Pipeline 公开配置暴露。公开选择只有：

```text
position_profile = "smooth" | "event_intensity"
```

profile 固定语义：

```text
smooth:
  内部使用 band=0.10
  内部使用 max_step=0.15

event_intensity:
  内部使用 band=0
  内部使用 max_step=2
  position_raw = target_pos
```

`PipelineConfig` 继续承载 `position_engine_config`，但它只表达不会和 `position_profile` 冲突的全局字段，例如 `mode`。`band` / `max_step` 由 `position_profile` 固定派生，不允许调用方通过 `position_engine_config` 单独覆盖。

进入 Pipeline 评估时，`position_profile` 是 `band` / `max_step` 的唯一来源。底层 `PositionEngineConfig` 即使仍保留 `band` / `max_step` 字段，Pipeline 也必须用 profile 派生值覆盖它们。

## normalization 和 target_pos

`FactorFunc` 输出完整 1T `score_raw`。

从 `score_raw` 到 `target_pos` 通过 `normalization_config` 的白名单方法完成。`target_pos`、最终仓位、交易成本、PnL 和 turnover 都是评估层下游产物。

事件强度因子的 `score_raw` 表达事件强度。`target_pos` 支持连续或分段仓位，范围由全局 `PositionEngineConfig.mode` 决定：`long_flat` 为 `[0, 1]`，`long_short` 为 `[-1, 1]`。是否产生非零 `target_pos` 由 normalization 的门槛、分段或强度映射决定。执行层按 profile 执行 `target_pos`。

本次不扩展 normalization 白名单。事件强度因子的 `target_pos` 形态由现有白名单方法表达。

## hold_minutes 语义

`hold_minutes` 的含义固定是“隔多少根 1T bar 允许真实执行仓位变化一次”。它表示执行仓位更新频率。

事件触发后的持有时间属于另一类语义。本次不定义这个语义。后续改造应另起字段，例如：

```text
event_ttl_minutes
hold_after_signal_minutes
```

`event_intensity` profile 支持任意正整数 `hold_minutes`：

- `hold_minutes=1`：每根 1T bar 都是允许执行仓位变化的 bar，`position_exec == position_raw`。
- `hold_minutes>1`：仍然按 target bar 采样 `position_raw`，非 target bar 继承上一根 `position_exec`。

例子：完整 1T index 从 `00:00` 开始，`hold_minutes=15` 时 target bar 仍然是：

```text
00:14, 00:29, 00:44, 00:59, ...
```

这表示真实执行仓位只在这些 bar 变化。

## Pipeline 语义

`PipelineConfig` 应明确承载：

```text
position_profile
hold_minutes
position_engine_config
```

`position_profile="smooth"`：

- `hold_minutes` 按现有规则生成 `target_index`。
- 先完整 1T 计算 `position_raw`。
- 再按 `target_index` 采样成 `position_exec`。
- 非 target bar 继承上一根 `position_exec`。
- no-trade band / max_step 使用当前 smooth 执行语义。

`position_profile="event_intensity"`：

- `hold_minutes` 支持任意正整数。
- 先完整 1T 计算 `target_pos`。
- `position_raw` 直接等于 `target_pos`。
- 再按 `target_index` 采样成 `position_exec`。
- `hold_minutes=1` 时，`target_index` 等于完整 1T index，`position_exec == position_raw`。
- `hold_minutes>1` 时，`target_index` 按第 `N, 2N, 3N...` 根 1T bar 生成，非 target bar 继承上一根 `position_exec`。
- features 保持完整 1T 数据，FactorFunc 在完整 1T index 上运行。

无论哪个 profile：

- FactorFunc 都看完整连续 1T features。
- `score_raw` 都是完整 1T index。
- `target_pos` / `position_raw` 都保留完整 1T index。
- Backtester 使用 `position_exec` 计算 turnover、cost、PnL。
- `default_shift=0` 保持不变。
- 成本公式和 `cost_mode` 合法集合保持不变。
- spread 加载、对齐、NaN 校验保持不变。
- 年化因子保持不变。

## 批量和 GPU 语义

CPU 单因子、CPU batch fallback、GPU batch 后端共享同一套 profile 语义。

批量评估时：

- 同一批因子共享同一个 `position_profile`。
- 每个因子仍然保留自己的 `normalization_config`。
- 共享的准备工作仍然是 features、prices、spread、target_index、泄漏检测得到的 full-run score按因子分别保留，并在该因子的position/backtest阶段复用。
- GPU batch 后端在 smooth 和 event_intensity profile 下都使用同一套执行语义。

等价要求：

```text
同一个因子在同一个 profile 下的 CPU 单因子结果
==
同一个因子在同一个 profile 下的 CPU batch / GPU batch 结果
```

这里的结果至少包括：

- `target_pos`
- `position_raw`
- `position_exec`
- turnover
- cost
- pnl
- metrics

## 实现口径汇总

spec 里应明确写清：

- `event_intensity` 支持连续或分段 `target_pos`。
- normalization 白名单方法保持现状。
- `smooth` 保持当前连续强度型执行口径。
- `event_intensity` 下内部派生 `band=0`。
- `event_intensity` 下内部派生 `max_step=2`。
- `event_intensity` 下 `position_raw` 直接等于 `target_pos`。
- no-trade band 和 max_step 不作为单独 public config；具体参数由 `position_profile` 固定派生。
- `hold_minutes` 表示真实执行仓位更新频率。
- FactorFunc 输出 `score_raw`，评估层生成 `target_pos`、仓位、成本、PnL 和 turnover。
- 同一次 Pipeline batch 使用一个 `position_profile`。
- CPU 和 GPU 对同一个 profile 使用同一套执行口径。

## 小例子

### smooth profile

```text
position_profile = "smooth"
hold_minutes = 15
smooth profile 使用 no-trade band / max_step

target_pos:   [0.00, 0.05, 0.20, 0.20, 0.00]
position_raw: 按现有 no-trade band / max_step 语义平滑变化
```

### event_intensity profile, hold_minutes=1

```text
position_profile = "event_intensity"
hold_minutes = 1
event_intensity profile 内部使用 band=0 / max_step=2

target_pos:     [0.00, 0.25, 0.70, 0.40, 0.00]
position_raw:   [0.00, 0.25, 0.70, 0.40, 0.00]
position_exec:  [0.00, 0.25, 0.70, 0.40, 0.00]
```

### event_intensity profile, hold_minutes=3

```text
position_profile = "event_intensity"
hold_minutes = 3
event_intensity profile 内部使用 band=0 / max_step=2

target bars:    第 3, 6, 9... 根 1T bar
position_raw:   每分钟等于 target_pos
position_exec:  只在 target bar 取 position_raw，非 target bar 继承上一根 position_exec
```
