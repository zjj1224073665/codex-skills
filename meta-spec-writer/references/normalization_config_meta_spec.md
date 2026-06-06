# 可配置归一化 spec 改造

请修改本 repo 的 spec 文档，先只改 spec，不改代码和测试。

重点修改：

- `specs/02_position_engine.md`
- `specs/04_factor_interface.md`
- `specs/06_factor_runtime.md`
- `specs/07_pipeline.md`

必要时同步：

- `AGENTS.md`

## 目标

把当前单一 `rolling median/MAD -> k * score -> target_pos` 口径，彻底改成：

```text
FactorFunc 输出完整 1T score_raw
  -> PositionEngine 按 normalization_config 生成 position_intent
  -> execution rules 生成 position_raw
  -> Pipeline 按 hold_minutes 采样成 position_exec
  -> Backtester 只吃 position_exec
```

约束：
- Pipeline 前面已经规定score_raw 只允许“最前面一段连续前缀 NaN”，而且喂给
  PositionEngine 前会把这段前缀 NaN 转成 0.0。所以如果严格按现有 Pipeline 走，PositionEngine 实际看到的score_raw里面不会有nan
- 本次改造后，normalizer / PositionEngine 的输入口径固定为“不含 NaN”。`score_raw`
  的前缀 NaN 只允许存在于 FactorFunc 输出和 FactorResult 记录里；进入
  PositionEngine 前必须已经转成 0.0。如果实现者绕过 Pipeline 直接调用
  normalizer / PositionEngine 并传入 NaN，应直接视为非法输入，不要各方法各自定义
  NaN 排名、忽略或填充规则。
- FactorFunc 仍然只输出 score_raw。
- 每个因子可以声明自己的 `normalization_config`，但只能选择仓库内置的固定方法和参数档位。
- LLM 不能在 `source.py` 的因子函数里手写最终仓位、交易成本、PnL、turnover。
- 正式评估链路只走 `source.py -> FactorRuntime.compile_source(...) -> CompiledFactor -> Pipeline`。
  `normalization_config` 必须写在 `source.py` 顶层模块级变量里，由
  `FactorRuntime` 编译时提取并挂到 `CompiledFactor`。不要再让普通 Python
  callable 入口或 `FactorMeta`/`meta.json` 承载 normalization 配置。
- 删除 `Pipeline.evaluate_function(...)` / `Pipeline.evaluate_functions(...)`
  这两个普通 callable 入口：它们没有稳定的 `source.py` 顶层变量可读，容易绕过
  `FactorRuntime` 的配置提取边界，不再作为 Task 7 public API，也不要保留成
  Pipeline 上的测试 helper。
- 本次只实现归一化配置的结构化表达和评估口径；不在 Pipeline 里实现自动超参数搜索、自动择优或入池筛选逻辑。

## 新仓位前分数

新增统一中间量：

```text
position_intent
```

含义：标准化后的仓位前分数。

`position_intent` 是新口径里的语义名，用来说明“raw score 已经被归一化成仓位意图”。
正式输出 artifact 不需要新增 `position_intent` 列；继续使用既有的 `target_pos`
列来表达这个值。

取值范围：

```text
long_flat:  [0, 1]
long_short: [-1, 1]
```

新口径下：

```text
target_pos = position_intent
```

也就是说，`target_pos` 在新口径里不再表示 `clip(k * score, ...)` 的结果，
而是直接表示按 `normalization_config` 得到的仓位意图。

新口径不允许使用：

```text
target_pos = clip(k * score, ...)
```

废弃旧的全局 `k * score` 仓位映射。新口径不再使用 `k` 把标准化 score 转成仓位。

废弃旧的全局 `z_cap`。z-score / median-MAD 类方法如果需要控制满仓速度，只使用各自 config 里的 `saturation_z`。

执行层不变：

```text
position_intent
  -> no-trade band / max_step
  -> position_raw
  -> hold_minutes 采样
  -> position_exec
```

## 每个因子的 normalization 声明

每个因子可以声明一份 `normalization_config`。这份声明是评估元信息，不是因子里的可执行仓位逻辑。

`normalization_config` 的声明入口固定为：

- `source.py` 顶层模块级变量。

`meta.json` / `FactorMeta` 只记录因子身份、来源、生成/训练复现信息等元数据，
不定义 `normalization_config` 字段。包含该字段的 artifact 不合法，应直接报错。

`normalization_config` 的提取边界必须稳定。推荐由 `FactorRuntime` 在编译
`source.py` 时读取模块级 `normalization_config` 并挂到 `CompiledFactor`，再由
Pipeline 从 `CompiledFactor` 读取；不要让不同实现各自新造路径名，也不要在
评估阶段靠 `func.__globals__` 这类隐式方式临时偷读。

`normalization_config` 必须是 `source.py` 顶层的静态字面量 dict。编译阶段应使用
AST 或等价静态解析读取，不应通过执行模块代码求值。只允许字符串、数字、布尔值、
`None`、list 和 dict 这类基础字面量；不允许函数调用、变量引用、环境变量、随机数、
条件表达式、推导式或任何运行时生成配置。非静态字面量、未知字段、白名单外 method、
越档参数都应直接报错。

`CompiledFactor` 是正式评估前的标准因子对象，至少要能稳定承载：

- `func`：编译出来的可执行因子函数
- `source_code`：原始源码字符串，供静态泄漏检查和复现使用
- `func_name`：因子函数名
- `meta`：因子身份、来源、生成/训练复现信息
- `normalization_config`：从 `source.py` 顶层模块级变量读取到的配置；缺失时为 `None`

Pipeline 正式入口只从 `CompiledFactor.normalization_config` 读取 normalization 声明。
`FactorMeta` / `meta.json` 里如果出现 `normalization_config` 字段，应视为非法
artifact，直接报错；不要做“两处一致性校验”，因为新口径下只有 `source.py`
顶层这一处声明入口。

例子：

```python
normalization_config = {
    "method": "rolling_tsrank_entry",
    "window": 1440,
    "entry_rank": 0.80,
}
```

`FactorFunc` 仍然只输出完整 1T `score_raw`。`source.py` 可以声明模块级 `normalization_config`，但不能在因子函数里手写 `position_intent`、`target_pos`、最终仓位、交易成本、PnL 或 turnover。

Pipeline 对每个因子分别从 `CompiledFactor` 读取它的 `normalization_config`。批量评估时，一批因子可以有不同 normalization；共享的仍然是 `features`、`prices`、`spread`、`target_index` 和泄漏检测得到的 full-run `score_raw`。position / backtest 阶段按每个因子的 normalization 配置分别生成仓位。

`long_flat` / `long_short` 的方向模式仍然使用全局 `PositionEngineConfig.mode`，不是每个因子的 `normalization_config` 字段。也就是说，`normalization_config` 只决定“raw score 怎么变成 position_intent”，不决定本轮评估是 long-flat 还是 long-short。

如果因子没有声明 `normalization_config`，默认使用：

```python
normalization_config = {
    "method": "rolling_median_mad",
    "window": 1440,
    "saturation_z": 4.0,
}
```

默认和读取规则固定如下：

- `source.py` 顶层缺失 `normalization_config` 时，使用上面的默认配置。
- `source.py` 顶层存在 `normalization_config` 时，只读取这一份，并按白名单和固定参数档位校验。
- `meta.json` / `FactorMeta` 不定义 `normalization_config` 字段；如果出现该字段，artifact 不合法，直接报错。
- `FactorRuntime.compile_candidate(...)` 如果需要支持 candidate-like 对象的
  normalization 选择，也必须要求上游把配置写进 `candidate.source_code` 的
  `source.py` 顶层变量；不要从 `candidate.normalization_config` 填入
  `FactorMeta`。
- 普通 callable 评估入口必须删除。需要评估函数时，应先把源码交给
  `FactorRuntime.compile_source(...)` 得到 `CompiledFactor`，再交给 Pipeline。

`eps` 固定为实现常量：

```python
eps = 1e-8
```

`eps` 不进入 `normalization_config`，也不开放给 LLM 选择；CPU / GPU / 流式实现都用同一个固定值。

## normalization 白名单

只允许下面 5 类。

### 1. `rolling_zscore`

```text
z = (raw - rolling_mean(raw, W)) / [rolling_std(raw, W) + eps]

long_short: position_intent = clip(z / saturation_z, -1, 1)
long_flat:  position_intent = clip(z / saturation_z,  0, 1)
```
 min_periods=1

`rolling_std` 必须明确用 `ddof=0`，也就是分母用当前窗口里的有效样本数 `n`，不是 `n-1`。窗口里只有 1 个有效值时，`std=0`，所以这一项的 zscore 应为 0。这样 CPU / GPU / pandas / numpy 实现不会因为默认标准差口径不同而跑出不同仓位。

正常连续因子，没什么极端值，用它。。

### 2. `rolling_winsor_zscore`

这里的截尾必须按“当前窗口”现场计算。不要先对整条时间序列生成一列“截尾后的 raw”，再拿那列去做 rolling mean/std。

对每个时间点 `t`，流程固定为：

```text
window = raw[t-W+1 : t]，包含当前 t，只用过去和当前，不看未来

q_low = 当前 window 的低分位数
q_high = 当前 window 的高分位数

把当前 window 里的每个值都限制在 [q_low, q_high] 里面，得到 clipped_window。

z = (clipped_window 最后一项 - mean(clipped_window)) / (std(clipped_window) + eps)

long_short: position_intent = clip(z / saturation_z, -1, 1)
long_flat:  position_intent = clip(z / saturation_z,  0, 1)
```

`q_low` / `q_high` 的分位数计算使用 pandas `quantile` 默认的 `linear` interpolation 口径。CPU / GPU 实现也必须复刻这个口径，不要各自使用不同的 quantile 默认值。

这里的 `std(clipped_window)` 同样必须用 `ddof=0`。不要使用 pandas `std()` 的默认 `ddof=1`。

例子：

```text
raw = [0, 0, 100, 100]
W = 3

算最后一个 100 时，当前 window 是 [0, 100, 100]。
先用 [0, 100, 100] 自己算 q_low / q_high。
再用这同一对 q_low / q_high，把 [0, 100, 100] 三个值一起限制到 [q_low, q_high] 里面。
最后只用这个处理后的当前 window 算 mean/std/z。
```

这类方法适合连续因子，但偶尔有离群尖刺。它表达的是：每一分钟都用当时能看到的最近窗口，把这个窗口里的极端值先压住，再做 zscore。

### 3. `rolling_median_mad`

```text
z = (raw - rolling_median(raw, W)) / (rolling_mad(raw, W) + eps)

long_short: position_intent = clip(z / saturation_z, -1, 1)
long_flat:  position_intent = clip(z / saturation_z,  0, 1)
```

`rolling_mad` 使用原始 MAD：

```text
median(|x - rolling_median|)
```

不要乘 `1.4826` 或其它正态分布校准系数。这里的 MAD 就按上面这个原始定义直接作为分母。

规则：

- rolling window 包含当前 bar，只看 `raw[t-W+1 : t]`，不看未来。
- `min_periods=1`；窗口不足 `W` 时，用已有数据算。
- 窗口里只有 1 个有效值时，`mad=0`，所以这一项的 zscore 应为 0。

分布很脏、肥尾、异常值多，用中位数和 MAD 做 robust 标准化。

### 4. `rolling_tsrank_centered`

```text
rank = 当前 raw 在过去 W 根里的百分位排名，范围 [0, 1]

long_short: position_intent = 2 * rank - 1
long_flat:  position_intent = clip(2 * rank - 1, 0, 1)
```

适合只相信排序、不相信 raw 绝对尺度的因子。

注意：`long_flat` 下 `rank > 0.5` 就会有小多仓。事件型多头因子优先用 `rolling_tsrank_entry`。

tsrank 的排名规则固定如下：

- 每个时间点 `t` 只看 `raw[t-W+1 : t]`，窗口包含当前 `t`，不看未来。
- 窗口不足 `W` 时，用已有数据算。
- 并列值用平均排名。比如窗口 `[1, 2, 2, 4]`，当前值是 `2`，两个 `2` 并列，占第 2、3 名，按它们的平均位置算。
- 百分位排名必须按下面公式固定：

```text
rank = (avg_rank_1based - 1) / (n_valid - 1)
```

其中 `avg_rank_1based` 是从 1 开始数的平均名次，`n_valid` 是当前窗口里的样本数。例子：窗口 `[1, 2, 2, 4]`，当前值是 `2`，平均名次是 `(2 + 3) / 2 = 2.5`，所以 `rank = (2.5 - 1) / (4 - 1) = 0.5`。

- 如果窗口里只有当前这一个有效值，`rank = 0.5`，表示中性，不因为样本太少直接给满分或零分。

### 5. `rolling_tsrank_entry`

专门用于非负事件强度因子。

这个方法只支持全局 `PositionEngineConfig.mode="long_flat"`。它表达的是“事件强度高才开多仓”，没有天然的做空含义；如果本轮评估的全局 mode 是 `long_short`，应直接视为非法 config。

```text
rank = 当前 raw 在过去 W 根里的百分位排名，范围 [0, 1]

if rank < entry_rank:
    position_intent = 0
else:
    position_intent = (rank - entry_rank) / (1 - entry_rank)
```

例子：

```text
entry_rank = 0.80

rank = 0.70 -> position_intent = 0
rank = 0.80 -> position_intent = 0
rank = 0.90 -> position_intent = 0.5
rank = 1.00 -> position_intent = 1.0
```

`rolling_tsrank_entry` 使用和 `rolling_tsrank_centered` 完全相同的 tsrank 排名规则。

这类方法表达的是：普通偏强不开仓，进入高分位才开仓。

## 固定参数档位

不要开放连续超参数搜索。

### `window`

单位是 1T bar：

```text
720     # 12小时
1440    # 1天
4320    # 3天
10080   # 7天
```

默认：

```text
1440
```

### `saturation_z`

只用于 z-score / median-MAD 类方法。

含义：多少个标准化单位对应满仓。

允许值：

```text
2.0
3.0
4.0
```

默认：

```text
4.0
```

例子：

```text
saturation_z = 4.0

z = 0 -> position_intent = 0
z = 2 -> position_intent = 0.5
z = 4 -> position_intent = 1.0
```

### winsor 分位数

只用于 `rolling_winsor_zscore`。

字段名固定为：

```text
winsor_quantiles
```

允许值：

```text
[0.01, 0.99]
[0.02, 0.98]
```

默认：

```text
[0.01, 0.99]
```

### `entry_rank`

只用于 `rolling_tsrank_entry`。

允许值：

```text
0.70
0.80
0.90
```

默认：

```text
0.80
```

## LLM 选择规则

LLM 只能选择白名单方法加参数。

LLM 不允许：

- 自由发明 normalization method
- 自由搜索连续超参数

## 批量 / GPU 评估要求

批量评估时，同一批因子可以有不同的 `normalization_config`。CPU fallback 和 GPU
batch 后端都必须按每个因子自己的配置生成 `target_pos`、`position_raw` 和
`position_exec`，不能假设整批因子共享同一个 normalization method、window 或参数。

具体实现方式由实现者决定：可以逐因子算，可以按相同 config 分组算，也可以用其它
batch/GPU router。spec 只冻结语义：在相同 `score_raw`、prices、spread、
fee、`PositionEngineConfig.mode`、execution rules、`hold_minutes` 和 `cost_mode` 下，
批量路径里每个因子的结果必须和“这个因子单独按自己的 `normalization_config` 跑”
一致。

## Pipeline 正式入口

Task 7 的 public API 不再包含普通 callable 入口。正式入口只保留：

- `evaluate_compiled_factor(compiled_factor, features=None)`：评估一个已经由
  `FactorRuntime.compile_source(...)` 产出的 `CompiledFactor`
- `evaluate_compiled_factors(compiled_factors, features=None)`：批量评估一批
  `CompiledFactor`；这是 LLM 一轮生成很多因子时的主入口
- `evaluate_factor(factor_name)`：从 registry 按名字加载已落盘因子，内部编译成
  `CompiledFactor` 后评估
- `evaluate_all()`：从 registry 发现全部因子，内部批量编译成 `CompiledFactor`
  后评估

研究生成链路一律使用：

```text
LLM 生成 source.py
  -> FactorRuntime.compile_source(...)
  -> Pipeline.evaluate_compiled_factors(...)
```

registry 入口只用于已落盘因子的按名复评或全量复评。必须从 spec 和 Pipeline
public API 中删除 `evaluate_function(...)` / `evaluate_functions(...)`；它们绕过
`source.py` 顶层 `normalization_config` 的正式提取路径。
