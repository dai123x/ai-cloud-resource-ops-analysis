import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "resource_ops.db"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

with sqlite3.connect(DB) as conn:
    df = pd.read_sql_query("SELECT * FROM resource_usage", conn)

df["date"] = pd.to_datetime(df["date"])
df["idle_flag"] = df["gpu_utilization"] < 0.20
df["estimated_idle_cost"] = np.where(
    df["idle_flag"], df["cost"] * (1 - df["gpu_utilization"]), 0
)

team = (df.groupby("team")
          .agg(avg_gpu_util=("gpu_utilization","mean"),
               total_cost=("cost","sum"),
               idle_records=("idle_flag","sum"),
               estimated_idle_cost=("estimated_idle_cost","sum"))
          .reset_index())
team["avg_gpu_util_pct"] = (team["avg_gpu_util"]*100).round(2)
team["total_cost"] = team["total_cost"].round(2)
team["estimated_idle_cost"] = team["estimated_idle_cost"].round(2)
team.to_csv(OUT/"team_summary.csv", index=False)

daily = df.groupby("date").agg(
    gpu_allocated=("gpu_allocated","sum"),
    avg_gpu_util=("gpu_utilization","mean"),
    daily_cost=("cost","sum")
).reset_index()
daily["rolling_7d_cost"] = daily["daily_cost"].rolling(7,min_periods=1).mean()
daily["rolling_7d_gpu"] = daily["gpu_allocated"].rolling(7,min_periods=1).mean()

# Simple transparent capacity forecast: recent 14-day mean + 15% buffer
recent = daily.tail(14)
forecast_gpu = int(np.ceil(recent["gpu_allocated"].mean()*1.15))
forecast = pd.DataFrame([{
    "method":"14-day mean + 15% buffer",
    "recommended_gpu_capacity":forecast_gpu,
    "recent_mean_allocated_gpu":round(recent["gpu_allocated"].mean(),2)
}])
forecast.to_csv(OUT/"capacity_forecast.csv", index=False)

print("=== Team summary ===")
print(team[["team","avg_gpu_util_pct","total_cost","idle_records","estimated_idle_cost"]].to_string(index=False))
print("\nRecommended GPU capacity:", forecast_gpu)
