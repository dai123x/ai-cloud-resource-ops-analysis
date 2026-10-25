CREATE TABLE resource_usage (
  date TEXT,
  team TEXT,
  instance_id TEXT,
  gpu_type TEXT,
  gpu_allocated INTEGER,
  gpu_used_equiv REAL,
  gpu_utilization REAL,
  cpu_allocated INTEGER,
  cpu_utilization REAL,
  runtime_hours REAL,
  gpu_price_per_hour REAL,
  cost REAL
);