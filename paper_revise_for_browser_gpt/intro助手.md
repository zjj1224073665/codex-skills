写英文introduction的时候，一定要遵循：研究动机 → 聚焦问题 → 前人工作综述 → 研究空白 → 应对方案 → 贡献。

前人工作综述 → 研究空白 这里，需要先说这个问题之前大家是怎么解决的，后来是怎么解决的，最近是怎么解决的，然后这些解决方法遗留了什么gap，为了解决这个gap有哪些人提出了什么方法，但是解决得还不够好
比如：EPF has been actively studied for decades. Early methods are based on statistical models (e.g., Auto-Regressive Integrated Moving Average model\cite{weron2014electricity} and Generalized Autoregressive Conditional Heteroskedasticity model\cite{garcia2005garch}) and machine learning techniques (e.g., Artificial Neural Networks\cite{amjady2006day}, Support Vector Machines\cite{shiri2015electricity}, and Random Forests\cite{alkawaz2022day}). The mainstream EPF research in the last a few years focuses on utilizing deep neural networks due to their ability of modeling complex, non-linear temporal patterns. \cite{marcjasz2023distributional} develops a deep learning-based probabilistic EPF technique. 
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

Despite the demonstrated effectiveness of deep learning models in EPF, the deep learning-based models are black-boxes in nature and lack interpretability. This could hinder the practical deployment of EPF, as the decision-makers may need to understand the driving force behind the forecasting result. For example, it has been publicly reported that the black-box nature of deep learning models has caused non-trivial concerns to modern energy market participants\cite{powermag_ai_growth,wexler2024doubleedged,endgame2025blackbox}. The issue of lacking interpretability would be more obvious when the real-time electricity price data and the historical data used for training the EPF model do not satisfy the independent identical distribution (I.I.D.) condition due to the complex dynamics in energy markets. Therefore, it is necessary to develop interpretable EPF tools to provide not only accurate electricity price forecasting, but also information that can explain the logic and rationale of generating the forecasts. Such interpretability could enhance communication and understanding between real-world decision makers and EPF models, and could provide guidelines for decision makers to better perform portfolio and risk management in the changing market environment. Up to date, only a handful of paper are found to develop interpretable EPF solutions: in \cite{uniejewski2021regularized}, the authors develop a regularized probabilistic EPF technique. Instead of indiscriminately using all available energy market data (this could introduce noises), the method uses an automated filter to select only the most informative features while discarding the rest. By revealing exactly which signals drive the forecast, the method not only ensures the model is easy to understand but also preserves high EPF accuracy. \cite{tschora2022electricity} develops an interpretable machine learning framework for day-ahead EPF. The method uses Shapley additive explanations to calculate the precise contribution of every input feature. It shows exactly how much each feature, like wind forecasts or foreign prices, pushed the predicted electricity price up or down. With this mechanism, the system can learn the actual, interpretable market logic, such as the balancing act between gas prices and electricity imports. \cite{melgar2024novel} introduces a real-time ensemble learning mechanism for EPF. Unlike conventional approaches that often train a fixed model, the method combines a model trained from long-term, historical electricity market data with a dynamic, lightweight model that is continuously updated by real-time market data streams. With this design, the system is capable of instantly detecting abnormal price variations. Moreover, it offers built-in explainability by showing users the historical feature patterns that drive the generation of price forecasts, achieving lower error rates than conventional deep learning models.

The work in \cite{uniejewski2021regularized,tschora2022electricity,melgar2024novel} makes preliminary attempts on enhancing interpretability of EPF. While these efforts, as useful references in this emerging research direction, have made encouraging progress on enabling interpretability for EPF, they are associated with non-trivial shortcomings. First, the current interpretable EPF methods \cite{tschora2022electricity} primarily focus on providing post-hoc explanations from the price predictions that have been generated. Technically, this is achieved by calculating Shapley values of the predictions. While these methods can identify which features had the largest impact on the forecast, they can hardly reveal the internal forecasting-making rationale, meaning they do not explain how the model actually used those features to produce the forecast. Second, while some current methods (e.g., \cite{uniejewski2021regularized} and \cite{melgar2024novel}) generate price predictions by mining effective feature patterns from historical data, their lack of transparency limits their ability to explain the actual driving factors behind the price signals. Third, existing methods typically treat the absolute error between predicted and actual prices as their sole optimization objective. However, in practical trading and risk management, preserving the co-movement between forecasted and realized price changes can be as important as forecasting exact price values. A model optimized only for point-forecast error may achieve a small numerical discrepancy while failing to preserve the linear association between forecasted and realized price changes. Therefore, incorporating the price variation trend into the forecasting objective is essential, yet this remains unaddressed in the current literature.

语言一定要plain，不要用不常见的单词，不要用各种复杂的从句，一定要很plain，让人读起来感觉很容易懂，绝对不允许使用;结尾的句子

▎ 冗余细节：不要在引言部分重复罗列术语定义、观测列表、成本公式或实现规则。这些特别细节的东西应该出现在后文method部分


新出现的术语、约束、指标、机制、变量和命名概念在读者不得不依赖它们之前，先获得动机说明和定义。适用场景：论文中突兀地引入行话；假设了一个未加解释的预算或限值；公式中的变量、下标、集合或单位未作说明；从背景直接跳到形式化模型；研究问题的来源不清楚

示例：

突兀的写法：

▎ 两条有轨电车线路共享一个总充电功率预算。

有动机铺垫的写法：

▎ 在多线网交汇的城市公共交通系统中，不同线路往往共享同一配电网络。从运营商的全局视角来看，供电系统承受的并非单一线路的独立用电，而是多条线路在同一时刻叠加形成的“净负荷”——即所有同时充电的车辆总负荷，减去参与 V2G 回送的车辆所释放的抵消功率。受限于馈线物理容量、变压器额定功率或购电合同，运营商必须将这一净负荷严格控制在有限的共享需量预算之内。在共享需量预算的约束下，各线路的充电和能量回送行为不再相互独立，而是会相互挤占有限的供电容量。因此，要充分发挥大规模车网互动的潜力并保障电网安全，就必须突破单线运行的局限，在统一的框架下对跨线路的能源交互进行全局协调。

另外还有一个要注意的，不要总是用是xxx，而不是xxx这种表述：在全文中搜索对比性表达，包括：

- 英文：rather than、instead of、not、not ... but、as opposed to、does not、need not、neither ... nor。
- 中文：不是……而是……、而不是、而非、并非、不……而是……、无需……而……、不能……而应……。


最后给你一个正确的introduction 示例：
研究动机 → 聚焦问题：
Electricity price forecasting (EPF) is a fundamental task in modern energy systems and it plays an important role in the decision-making process of different stakeholders. For example, power generation companies and retailers rely on EPF to make bidding strategies in energy markets and manage financial risks; load aggregators and even customers (e.g., customers participated in real-time pricing program\cite{lissa2021deep, athanasiadis2024holistic, li2024communication}) make energy management plans based on the EPF result. As a special time series forecasting problem, EPF is highly challenging as electricity prices are among the most volatile commodity prices - characterized by price spikes, multi-scale seasonality, and complex, nonlinear dependencies on a variety of influencing factors such as system demand, generation availability, and network constraints.


应对方案 → 贡献。
To overcome the above identified shortcomings in interpretable EPF research, this paper proposes a new interpretable EPF framework backboned by code-level SR\cite{li2022competition} and generative artificial intelligence\cite{naveed2025comprehensive}. Unlike the traditional SR technique that is limited to searching for simple mathematical expressions, code-level SR attempts to generate executable codes capable of implementing sophisticated multi-step logic, conditional branches, and complex feature engineering. By shifting the paradigm to this code-level approach, the proposed framework---titled the Generative Evolutionary Multi-objective Optimizer for EPF (GEMO-EPF)---ensures both accuracy and interpretability for EPF tasks.

The specific innovations brought by GEMO-EPF are threefold:

(1) It is the first code-level SR-driven EPF system and thus pioneers the research of interpretable EPF -- an area that is not well explored in academia. GEMO-EPF relies on a population-based, multi-objective evolutionary strategy and three large language models (LLMs). The LLMs are assigned different roles and act as the Tuner, the Innovator, and the Assembler, respectively. The Tuner refines parameters of the system; the Innovator introduces new interpretable electricity-market mechanisms; and the Assembler combines elite EPF code solutions through linear or multi-timescale blending. The LLMs work together to generate candidate computer codes representing EPF logics, and an outer layer multi-objective evolution strategy is applied to select the best code and generate the forecast. The well-structured EPF codes eventually generated by GEMO-EPF contain highly human-readable information and can support the stakeholders to perform human analysis and decision-making in energy markets, thus bridging the gap between complexity and transparency in EPF.

(2) It integrates a new EPF paradigm by treating an EPF task as a multi-objective optimization problem that minimizes point-price forecasting errors and maximizes the correlation between forecasted and realized price movements. Compared with the existing work (e.g., \cite{marcjasz2023distributional, zhang2020deep, li2022dense,
  uniejewski2021regularized, tschora2022electricity,     
  melgar2024novel}) that focuses on point forecasts of electricity price, the new EPF paradigm treats the correlation between forecasted and realized price movements as a first-class forecasting objective. This has practical implications because, in applications such as arbitrage, bidding, and risk management, strengthening the linear alignment between forecasted price movements with realized market movements can be as important as predicting the future price value accurately.

(3) As a core component of GEMO-EPF, we propose a new multi-objective evolution strategy tailored to time series energy data forecasting tasks. The strategy selects high-quality solutions from a population of candidate solutions based on the signal-correlation metric. Compared with the conventional approach\cite{deb2002fast} that relies on the crowding distance to make the solution selection, the proposed strategy can effectively remove redundant forecasting solutions that generate highly correlated forecasting signals and encourages the retained population to contain complementary forecasting logics. In this way, it can well preserve the solution diversity in the Pareto front. While this new strategy is particularly useful for the EPF problem studied in this paper (because highly correlated forecasting signals often capture the same market pattern, which may create concentrated risk exposure when the market enters a new regime), it is also expected to provide more generic support for other energy data forecasting applications.

The rest of this paper is organized as follows. Section 2 formulates the EPF problem and introduces the supporting technique. Section 3 presents the implementation details of the proposed GEMO-EPF framework. Numerical experiment results are reported and discussed in Section 4. Section 5 concludes this paper and draws future research.

This paper uses the following notation: vectors are bold lower case $\mathbf{x}$; matrices are bold upper case $\mathbf{A}$; sets are in calligraphic font $\mathcal{S}$; and scalars are non-bold $\alpha$.
