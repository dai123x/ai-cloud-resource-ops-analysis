# AI / 云资源利用率与成本分析

以 56 天的模拟 GPU/CPU 使用与费用记录，演示 SQLite/SQL 提取、pandas 分组分析、低利用率资源识别与容量建议。全部数据为合成数据，不能直接作为真实环境的成本或缩容依据。

## 运行

在本仓库根目录安装依赖并运行：

```bash
python -m pip install -r requirements.txt
python src/analyze.py
```

程序读取 `data/resource_ops.db` 中的 `resource_usage` 表，生成或覆盖 `output/team_summary.csv` 与 `output/capacity_forecast.csv`。数据库与同批原始记录 `data/resource_usage.csv` 一并保留。运行前可自行备份已有输出。

## 文件

- `src/analyze.py`：利用率、费用、闲置成本估算及容量建议。
- `sql/01_schema.sql`、`sql/02_analysis.sql`：表结构及 SQL 分析示例。
- `data/`：模拟 CSV 与对应 SQLite 数据库。
- `output/`：原压缩包中的保存结果；重跑结果以当前环境输出为准。
- `requirements.txt`：pandas 与 NumPy 依赖。

容量建议使用最近 14 天 GPU 配额均值并加 15% 缓冲；闲置成本为阈值规则下的估算，未结合 SLA、排队时长、显存、可回收性或实际账单，不等于可兑现节省。

原 `MiniMax_云资源运营_Python_SQL项目.zip` 保留作为来源归档。本轮展开的代码、SQL、数据和保存输出与压缩包逐文件一致，便于直接浏览、审阅和运行。
