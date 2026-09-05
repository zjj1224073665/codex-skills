我检索了 OpenReview；部分 PDF 页面有验证拦截，因此采用同一论文的正式会议页面或 arXiv 版本。下面尽量直接套用顶会论文中的现成句式。

### 1. 英文译文

```latex
Catenary-free trams store energy onboard and recharge during station dwell times. Figure~\ref{fig:architecture} illustrates the overall architecture of the system considered in this paper. Multiple tram lines operate within a common urban area, and their stations draw power from a shared distribution network. When a tram stops, its pantograph connects to the station-side charging interface, which is connected to the urban distribution grid via a traction substation. For each stop, the control center receives a request and returns a control command.
```

### 2. 逐句溯源表

| 译文 | 来源论文 | 套用的原句或片段 |
|---|---|---|
| Catenary-free trams store energy onboard and recharge during station dwell times. | 无符合条件的 AI 顶会来源；该句为结合轨道交通术语后的自写句。 | 无 |
| Figure~\ref{fig:architecture} illustrates the overall architecture of the system considered in this paper. | [EquiformerV2: Improved Equivariant Transformer for Scaling to Higher-Degree Representations](https://arxiv.org/abs/2306.12059)，ICLR 2024。 | “Figure 1 illustrates the overall architecture of EquiformerV2 and the differences from Equiformer.” |
| Multiple tram lines operate within a common urban area, and their stations draw power from a shared distribution network. | [Strategic Classification With Externalities](https://arxiv.org/abs/2410.08032)，ICLR 2025。 | “multi-agent interactions in a shared environment” |
| When a tram stops, its pantograph connects to the station-side charging interface, which is connected to the urban distribution grid via a traction substation. | 无符合条件的 AI 顶会来源；该句中的轨道供电术语为自写。 | 无 |
| For each stop, the control center receives a request and returns a control command. | [UIS-Digger: Towards Comprehensive Research Agent Systems for Real-world Unindexed Information Seeking](https://arxiv.org/abs/2603.08117)，ICLR 2026；另参考 [Contextual Decision-Making with Knapsacks Beyond the Worst Case](https://proceedings.neurips.cc/paper_files/paper/2024/hash/a0e1c2c40fc245b5fe7251ea33fbb045-Abstract-Conference.html)，NeurIPS 2024。 | “via a request-response message system”; “selects an action in each round upon observing a random request” |

### 3. 只能自行组织的词句

主要包括：

- `catenary-free trams`
- `store energy onboard`
- `station dwell times`
- `tram lines`
- `urban area`
- `stations draw power`
- `shared distribution network`
- `pantograph`
- `station-side charging interface`
- `urban distribution grid`
- `traction substation`
- `control center`
- `control command`

这些词句属于该轨道交通系统的具体技术内容；在检索到的近期 ICLR/NeurIPS/ICML 论文中，没有找到可以直接套用且语义对应的完整表达。