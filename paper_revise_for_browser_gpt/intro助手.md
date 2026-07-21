写英文introduction的时候，一定要遵循：研究动机 → 聚焦问题 → 前人工作综述 → 研究空白 → 应对方案 → 贡献。

语言一定要plain，不要用不常见的单词，不要用各种复杂的从句，一定要很plain，让人读起来感觉很容易懂，绝对不允许使用;结尾的句子

▎ 冗余细节：不要在引言部分重复罗列观测列表、成本公式或实现规则。这些特别细节的东西应该出现在后文


修改学术与技术写作，使新出现的术语、约束、指标、机制、变量和命名概念在读者不得不依赖它们之前，先获得动机说明和定义。适用场景：论文中突兀地引入行话；假设了一个未加解释的预算或限值；公式中的变量、下标、集合或单位未作说明；从背景直接跳到形式化模型；研究问题的来源不清楚

示例：

突兀的写法：

▎ 两条有轨电车线路共享一个总充电功率预算。

有动机铺垫的写法：

▎ 配备高功率车载储能的车辆在短暂的车站停站期间补充能量，因此每个充电桩都可能承受一个持续时间短、幅值大的负荷。当多辆车同时充电时，这些负荷相互叠加，可能超过供电设备的规划容量或运营商的合同需量。因此，运营商必须协调任一时刻的总电网侧充电功率。本文将规划中的最大总充电功率称为"总充电功率预算"；它是以千瓦（kW）为单位的功率限值，而非能量额度。当两条线路共享这一预算时，一条线路占用的功率会相应减少另一条线路可用的功率。

另外还有一个要注意的，不要总是用是xxx，而不是xxx这种表述：在全文中搜索对比性表达，包括：

- 英文：rather than、instead of、not、not ... but、as opposed to、does not、need not、neither ... nor。
- 中文：不是……而是……、而不是、而非、并非、不……而是……、无需……而……、不能……而应……。

将这些表达视为候选项，而非自动判定为错误。在下结论之前，需通读整段、相邻段落、首次出现的定义、公式、表格、图注、实验设置和局限性部分。搜索该表达在后文的使用情况，判断这个对比究竟解决了真实的歧义，还是仅仅重复了已有信息。

改写前先分类

将每处出现归入以下三类之一。

可直接定义的候选项

当正面从句已经承载了完整含义，而否定从句只是在指称一个想象出来的误解时，进行改写。常见情形包括：

- 一个量被正面定义后，又与另一个量作对比；
- 设计系数被拿来与货币价格作对比；
- 固定的索引映射被拿来与到达顺序作对比；
- 同一个软约束的解释在多个章节中重复出现。

承载边界的对比

在语义上保留该边界，但用正面方式表达。需要特别检查以下情形：

- 硬性物理限制 vs. 带惩罚的规划目标；
- 功率阈值 vs. 电量配额；
- 实测或标定值 vs. 明确的假设值；
- 经过的时间 vs. 事件索引；
- 货币价格 vs. 任意的目标函数单位；
- 模型输入 vs. 模型输出；
- 在线策略信息 vs. 基线方法所拥有的未来信息；
- 局部事件成本 vs. 非负的episode总量；
- 经过标定的预测 vs. 基于情景的模拟；
- 物理现象 vs. 建模层面的惩罚项。

如果正面改写无法清晰地承载这一区分，就保留一个简洁的对比句。准确性优先于文体上的统一。

当否定确实承担了必不可少的论证或逻辑作用时，予以保留，包括：

- 论证一个有充分支撑的研究空白；
- 指出前人工作缺乏某项特性；
- 定义一个不可行或被排除的条件；
- 报告缺失的数据、无法获得的测量值，或方法中确实缺失的组成部分；
- 在证明、公式或算法中区分互斥的情形；
- 引用审稿人的原话或原始文献。

不要机械地删除所有的 not、rather than、不是、而非。

改写为正面定义在正面陈述句中包含相关的单位、聚合层级、时间尺度、适用范围、来源，或超出限值后的行为。

应用以下模式：

- 把"X 是 Y，而不是 Z"替换为"X 是 Y"，并把 Y 展开到消除歧义为止。
- 把"该模型不施加 A；而是由 B 决定 C"替换为"由 B 决定 C"。
- 把"该机制使用 A 而非 B"替换为直接定义 A 的那个事件、规则或输入。
- 把否定式的来源免责声明替换为正面的来源陈述。
- 把否定式的局限性陈述替换为正面陈述该研究的有效适用范围。
- 在首次正式使用处保留一次定义后，删除后续重复出现的对比。
- 删除非必要的前向指引，例如"见后文"或"如下文所述"，直接陈述要点。保留
示例：

▎ The budget is a soft target rather than a hard physical limit.
▎ （预算是一个软性目标，而非硬性物理限制。）

改写为：

▎ The budget is a penalized planning target, and temporary exceedance incurs a penalty.
▎ （预算是一个带惩罚的规划目标，临时超出会产生惩罚。）

▎ The exponent counts decision events rather than elapsed seconds.
改写为：

▎ The exponent is the decision-event index.
▎ （该指数即为决策事件索引。）

▎ These coefficients are design weights, not monetary prices.
▎ （这些系数是设计权重，而非货币价格。）

改写为：

▎ These coefficients are fixed design weights expressed in arbitrary objective units.
▎ （这些系数是以任意目标函数单位表示的固定设计权重。）

▎ 该预算约束总功率，而不是整个时段的总能量。

改写为：

▎ 总充电功率预算是运营商设定的总电网侧充电功率规划阈值，单位为 kW。

最后给你一个正确的introduction 示例：
\section{Introduction}
\IEEEPARstart{E}{lectricity} price forecasting (EPF) is a fundamental task in modern energy systems and it plays an important role in the decision-making process of different stakeholders. For example, power generation companies and retailers rely on EPF to make bidding strategies in energy markets and manage financial risks; load aggregators and even customers (e.g., customers participated in real-time pricing program\cite{lissa2021deep, athanasiadis2024holistic, li2024communication}) make energy management plans based on the EPF result. As a special time series forecasting problem, EPF is highly challenging as electricity prices are among the most volatile commodity prices - characterized by price spikes, multi-scale seasonality, and complex, nonlinear dependencies on a variety of influencing factors such as system demand, generation availability, and network constraints. 

EPF has been actively studied for decades. Early methods are based on statistical models (e.g., Auto-Regressive Integrated Moving Average model\cite{weron2014electricity} and Generalized Autoregressive Conditional Heteroskedasticity model\cite{garcia2005garch}) and machine learning techniques (e.g., Artificial Neural Networks\cite{amjady2006day}, Support Vector Machines\cite{shiri2015electricity}, and Random Forests\cite{alkawaz2022day}). The mainstream EPF research in the last a few years focuses on utilizing deep neural networks due to their ability of modeling complex, non-linear temporal patterns. \cite{marcjasz2023distributional} develops a deep learning-based probabilistic EPF technique. 
Recent deep learning-based EPF studies have further improved forecasting
  performance from different perspectives. \cite{marcjasz2023distributional}
  develops a probabilistic EPF method that predicts price distributions rather
  than point prices, showing that Johnson's $\boldsymbol{S}_{\boldsymbol{U}}$
  distribution can capture the heavy tails and skewness of electricity prices
  and improve BESS trading profits. \cite{zhang2020deep} proposes a hybrid
  framework with error compensation and probabilistic interval forecasting to
  better handle market volatility. \cite{li2022dense} designs a dense skip
  attention model for day-ahead EPF, using attention and deep temporal feature
  extraction to capture both feature-wise importance and temporal variations.
  
% Instead of forecasting exact electricity prices, the method uses deep perceptron to predict the probabilistic distribution of prices, providing richer probabilistic information to stakeholders to make risk-aware energy management decisions. Specifically, the authors demonstrate that the four-parameter Johnson's $\boldsymbol{S}_{\boldsymbol{U}}$ distribution can well capture the heavy tails and skewness of electricity prices, leading to an 8\% increase in per-transaction profits in energy management of a real battery energy storage system (BESS). \cite{zhang2020deep} proposes a hybrid deep learning EPF framework. The method incorporates an error compensation module, enabling it to learn from previous forecasting mistakes and correct the current electricity price prediction. The authors combine this correction mechanism with probabilistic interval forecasting to generate price intervals, capturing the high volatility inherent in the electricity market. \cite{li2022dense} proposes a dense skip attention model specifically designed for day-ahead EPF. The model assigns different weights to important energy market-related features, and it separates short-term feature fluctuations from long-term trends using a neural network structure that is backboned by advanced residual unshared convolutional neural networks with gated recurrent units. Validated on North European electricity market data, the developed EPF method is shown to effectively handle temporal and feature-wise variability in electricity markets. 

Despite the demonstrated effectiveness of deep learning models in EPF, the deep learning-based models are black-boxes in nature and lack interpretability. This could hinder the practical deployment of EPF, as the decision-makers may need to understand the driving force behind the forecasting result. For example, it has been publicly reported that the black-box nature of deep learning models has caused non-trivial concerns to modern energy market participants\cite{powermag_ai_growth,wexler2024doubleedged,endgame2025blackbox}. The issue of lacking interpretability would be more obvious when the real-time electricity price data and the historical data used for training the EPF model do not satisfy the independent identical distribution (I.I.D.) condition due to the complex dynamics in energy markets. Therefore, it is necessary to develop interpretable EPF tools to provide not only accurate electricity price forecasting, but also information that can explain the logic and rationale of generating the forecasts. Such an interpretable function could enhance communication and understanding between the real-world decision maker and the EPF model, and could provide guidelines for the decision-maker to better perform portfolio and risk management in the changing market environment. Up to date, only a handful of paper are found to develop interpretable EPF solutions: in \cite{uniejewski2021regularized}, the authors develop a regularized probabilistic EPF technique. Instead of indiscriminately using all available energy market data (this could introduce noises), the method uses an automated filter to select only the most informative features while discarding the rest. By revealing exactly which signals drive the forecast, the method not only ensures the model is easy to understand but also preserves high EPF accuracy. \cite{tschora2022electricity} develops an interpretable machine learning framework for day-ahead EPF. The method uses Shapley additive explanations to calculate the precise contribution of every input feature. It shows exactly how much each feature, like wind forecasts or foreign prices, pushed the predicted electricity price up or down. With this mechanism, the system can learn the actual, interpretable market logic, such as the balancing act between gas prices and electricity imports. \cite{melgar2024novel} introduces a real-time ensemble learning mechanism for EPF. Unlike conventional approaches that often train a fixed model, the method combines a model trained from long-term, historical electricity market data with a dynamic, lightweight model that is continuously updated by real-time market data streams. With this design, the system is capable of instantly detecting abnormal price variations. Moreover, it offers built-in explainability by showing users the historical feature patterns that drive the generation of price forecasts, achieving lower error rates than conventional deep learning models.

The work in \cite{uniejewski2021regularized,tschora2022electricity,melgar2024novel} makes preliminary attempts on enhancing interpretability of EPF. While these efforts, as useful references in this emerging research direction, have made encouraging progress on enabling interpretability for EPF, they are associated with non-trivial shortcomings. First, the current interpretable EPF methods \cite{tschora2022electricity} primarily focus on providing post-hoc explanations from the price predictions that have been generated. Technically, this is achieved by calculating Shapley values of the predictions. While these methods can identify which features had the largest impact on the forecast, they can hardly reveal the internal forecasting-making rationale, meaning they do not explain how the model actually used those features to produce the forecast. Second, while some current methods (e.g., \cite{uniejewski2021regularized} and \cite{melgar2024novel}) generate price predictions by mining effective feature patterns from historical data, their lack of transparency limits their ability to explain the actual driving factors behind the price signals. Third, existing methods typically treat the absolute error between predicted and actual prices as their sole optimization objective. However, in practical trading and risk management, predicting the correct price trend is often just as critical as forecasting exact values. A model optimizing only for absolute error might minimize the numerical gap but still predict the wrong price direction. Therefore, incorporating the price variation trend into the forecasting objective is essential, yet this remains unaddressed in the current literature.

To overcome the above identified shortcomings in interpretable EPF research, this paper proposes a new interpretable EPF framework backboned by code-level SR\cite{li2022competition} and generative artificial intelligence\cite{naveed2025comprehensive}. Unlike the traditional SR technique that is limited to searching for simple mathematical expressions, code-level SR attempts to generate executable codes capable of implementing sophisticated multi-step logic, conditional branches, and complex feature engineering. By shifting the paradigm to this code-level approach, the proposed framework—titled the Generative Evolutionary Multi-objective Optimizer for EPF (GEMO-EPF)—ensures both accuracy and interpretability for EPF tasks.

The specific innovations brought by GEMO-EPF are threefold:

(1) It is the first code-level SR-driven EPF system and thus pioneers the research of interpretable EPF -- an area that is not well explored in academia. GEMO-EPF relies on a population-based, multi-objective evolutionary strategy and three large language models (LLMs). The LLMs are assigned different roles and act as the Tuner, the Innovator, and the Assembler, respectively. The Tuner refines parameters of the system; the Innovator introduces new interpretable electricity-market mechanisms; and the Assembler combines elite forecasting functions through linear or multi-timescale blending. The LLMs work together to generate candidate computer codes representing EPF logics, and an outer layer multi-objective evolution strategy is applied to select the best code and generate the forecast. The well-structured EPF codes eventually generated by GEMO-EPF contain highly human-readable information and can support the stakeholders to perform human analysis and decision-making in energy markets, thus bridging the gap between complexity and transparency in EPF.

(2) It integrates a new EPF paradigm by treating an EPF task as a multi-objective optimization problem that simultaneously minimizes the errors of point price forecasts and forecasted price variation directions. Compared with the existing work (e.g., \cite{marcjasz2023distributional, zhang2020deep, li2022dense,        
  uniejewski2021regularized, tschora2022electricity,     
  melgar2024novel}) that focuses on point forecasts of electricity price, the new EPF paradigm treats price variation direction as a first-class forecasting objective. This has practical implications because in energy-market applications such as arbitrage, bidding, and risk management, correctly predicting the direction of electricity price variation could be as important as predicting the exact price value.

(3) As a core component of GEMO-EPF, we propose a new multi-objective evolution strategy tailored to time series energy data forecasting tasks. The strategy selects high-quality solutions from a population of candidate solutions based on the signal-correlation metric. Compared with the conventional approach\cite{deb2002fast} that relies on the crowding distance to make the solution selection, the proposed strategy can effectively remove redundant forecasting solutions that generate highly correlated forecasting signals and encourages the retained population to contain complementary forecasting logics. In this way, it can well preserve the solution diversity in the Pareto front. While this new strategy is particularly useful for the EPF problem studied in this paper (because highly correlated forecasting signals often capture the same market pattern, which may create concentrated risk exposure when the market enters a new regime), it is also expected to provide more generic support for other energy data forecasting applications.

The rest of this paper is organized as follows. Section II formulates the EPF problem and introduces the supporting technique. Section III presents the implementation details of the proposed GEMO-EPF framework. Numerical experiment results are reported and discussed in Section IV. Section V concludes this paper and draws future research. This paper uses the following notation: vectors are bold lower case $\mathbf{x}$; matrices are bold upper case $\mathbf{A}$; sets are in calligraphic font $\mathcal{S}$; and scalars are non-bold $\alpha$.
