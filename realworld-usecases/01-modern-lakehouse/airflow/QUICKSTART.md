# 🚀 Airflow Quick Start Guide

Get your Airflow orchestration running in 5 minutes!

## ⚡ Super Fast Setup

```bash
# 1. Navigate to airflow directory
cd /Users/udayshankar/Documents/ML\ Projects/data-mastery/realworld-usecases/01-modern-lakehouse/airflow

# 2. Make setup script executable
chmod +x setup_airflow.sh

# 3. Run setup (installs everything)
./setup_airflow.sh

# 4. Set your Databricks token
export DATABRICKS_TOKEN="dapi_your_token_here"
source venv/bin/activate
airflow variables set DATABRICKS_TOKEN "$DATABRICKS_TOKEN"
```

## 🎬 Start Airflow

**Terminal 1 (Webserver):**
```bash
cd airflow
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)
airflow webserver --port 8080
```

**Terminal 2 (Scheduler):**
```bash
cd airflow
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)
airflow scheduler
```

## 🌐 Access UI

1. Open: **http://localhost:8080**
2. Login:
   - Username: `admin`
   - Password: `admin`
3. Find DAG: `lakehouse_taxi_pipeline`
4. Toggle **ON** (unpause the DAG)
5. Click **▶️ Trigger DAG** to run

## 📊 What You'll See

```
┌─────────────────────────────────────────┐
│     Lakehouse Taxi Pipeline DAG         │
├─────────────────────────────────────────┤
│                                         │
│  start_pipeline                         │
│       ↓                                 │
│  [bronze_layer] ← Task Group           │
│   ├─ check_data_source                 │
│   ├─ ingest_bronze_data                │
│   └─ validate_bronze_data              │
│       ↓                                 │
│  [silver_layer] ← Task Group           │
│   ├─ transform_silver_data             │
│   └─ validate_silver_data              │
│       ↓                                 │
│  [gold_layer] ← Task Group             │
│   ├─ dbt_deps                          │
│   ├─ dbt_run                           │
│   ├─ dbt_test                          │
│   └─ dbt_docs_generate                 │
│       ↓                                 │
│  send_pipeline_summary                 │
│       ↓                                 │
│  end_pipeline                          │
│                                         │
└─────────────────────────────────────────┘
```

## ✅ Success Indicators

After triggering the DAG, all tasks should show:
- 🟢 **Green** = Success
- 🔴 **Red** = Failed (check logs)
- 🟡 **Yellow** = Running
- ⚪ **Gray** = Not started

## 🧪 Test Single Task

```bash
# Test any task without running full DAG
airflow tasks test lakehouse_taxi_pipeline bronze_layer.ingest_bronze_data 2026-05-14
```

## 📝 View Logs

1. Click on any task in the UI
2. Click **Log** button
3. See real-time execution output

## 🔧 Common Commands

```bash
# List all DAGs
airflow dags list

# List tasks in a DAG
airflow tasks list lakehouse_taxi_pipeline

# Pause/Unpause DAG
airflow dags pause lakehouse_taxi_pipeline
airflow dags unpause lakehouse_taxi_pipeline

# Trigger DAG manually
airflow dags trigger lakehouse_taxi_pipeline

# View task logs
airflow tasks logs lakehouse_taxi_pipeline bronze_layer.ingest_bronze_data 2026-05-14
```

## 🎯 Next Steps

1. ✅ Run the DAG and watch it execute
2. 📊 Check task logs for Bronze/Silver/Gold execution
3. 🧪 Verify dbt tests all pass (40/40)
4. 📸 Take screenshots for your portfolio!
5. 🚀 Schedule it to run daily

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| DAG not showing | Check syntax: `python dags/lakehouse_taxi_pipeline.py` |
| Import errors | Set `PYTHONPATH` to project root |
| dbt fails | Check `DATABRICKS_TOKEN` variable |
| Can't login | Default: admin/admin |
| Port 8080 busy | Change port: `airflow webserver --port 8081` |

## 📚 Learn More

- **Full README:** `airflow/README.md`
- **DAG Code:** `airflow/dags/lakehouse_taxi_pipeline.py`
- **Airflow Docs:** https://airflow.apache.org/

---

**You're all set! 🎉**

Happy orchestrating! 🚀
