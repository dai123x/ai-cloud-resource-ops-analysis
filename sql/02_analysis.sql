-- 1. Team-level utilization and cost
SELECT team,
       ROUND(AVG(gpu_utilization)*100,2) AS avg_gpu_util_pct,
       ROUND(SUM(cost),2) AS total_cost
FROM resource_usage
GROUP BY team
ORDER BY total_cost DESC;

-- 2. Idle / low-utilization resources
SELECT date, team, instance_id, gpu_type, gpu_allocated,
       ROUND(gpu_utilization*100,2) AS gpu_util_pct, cost
FROM resource_usage
WHERE gpu_utilization < 0.20
ORDER BY cost DESC;

-- 3. Daily cost trend
SELECT date, ROUND(SUM(cost),2) AS daily_cost
FROM resource_usage
GROUP BY date
ORDER BY date;

-- 4. 7-day rolling cost using a window function
WITH daily AS (
  SELECT date, SUM(cost) AS daily_cost
  FROM resource_usage GROUP BY date
)
SELECT date,
       ROUND(daily_cost,2) AS daily_cost,
       ROUND(AVG(daily_cost) OVER (
         ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ),2) AS rolling_7d_avg
FROM daily;
