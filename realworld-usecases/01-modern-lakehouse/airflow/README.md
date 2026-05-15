# 🚀 Airflow Orchestration for Lakehouse Taxi Pipeline

Complete Apache Airflow orchestration for the medallion architecture data lakehouse.

## 📊 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAKEHOUSE TAXI PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐                                                │
│  │ NYC Taxi API │                                                │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌─────────────────┐                                             │
│  │  🟤 BRONZE LAYER │  ← Task Group: bronze_layer                │
│  │  Raw Ingestion   │     ├─ check_data_source                   │
│  │  (Delta Lake)    │     ├─ ingest_bronze_data                  │
│  └────────┬─────────┘     └─ validate_bronze_data                │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────┐                                             │
│  │  ⚪ SILVER LAYER │  ← Task Group: silver_layer                │
│  │  Data Cleaning   │     ├─ transform_silver_data               │
│  │  (Delta Lake)    │     └─ validate_silver_data                │
│  └────────┬─────────┘                                             │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────┐                                             │
│  │  🟡 GOLD LAYER   │  ← Task Group: gold_layer                  │
│  │  dbt Models      │     ├─ dbt_deps (install packages)         │
│  │  (4 models)      │     ├─ dbt_run (run models)                │
│  └────────┬─────────┘     ├─ dbt_test (40 tests)                 │
│           │               └─ dbt_docs_generate                    │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────┐                                             │
│  │ 📊 SUMMARY      │  ← send_pipeline_summary                    │
│  │ & Notifications  │                                             │
│  └─────────────────┘                                             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 What This DAG Does

### **Bronze Layer** (Raw Data Ingestion)
- ✅ Checks NYC Taxi API availability
- ✅ Ingests raw taxi trip data
- ✅ Validates data was successfully loaded
- 📊 **Output:** `default.bronze_raw_trips` table

### **Silver Layer** (Data Cleaning)
- ✅ Reads from Bronze layer
- ✅ Removes nulls, duplicates, invalid records
- ✅ Validates fare amounts and distances
- ✅ Standardizes formats
- 📊 **Output:** `default.silver_trips` table

### **Gold Layer** (Business Metrics via dbt)
- ✅ Installs dbt packages (`dbt-utils`)
- ✅ Runs 4 Gold models:
  - `gold_daily_summary` - Daily KPIs
  - `gold_hourly_patterns` - Time-based demand
  - `gold_top_routes` - Route profitability
  - `gold_revenue_by_payment` - Payment analytics
- ✅ Runs 40 automated data quality tests
- ✅ Generates documentation and lineage DAG
- 📊 **Output:** 4 Gold tables ready for dashboards

### **Reporting**
- ✅ Sends pipeline execution summary
- ✅ Reports record counts and status

## 🚀 Quick Start

### **1. Install Airflow**

```bash
cd airflow
chmod +x setup_airflow.sh
./setup_airflow.sh
```

This will:
- Create a Python virtual environment
- Install Apache Airflow 2.9.1
- Initialize the Airflow database
- Create admin user (username: `admin`, password: `admin`)

### **2. Set Databricks Token**

```bash
# Option A: Set in environment
export DATABRICKS_TOKEN="dapi1234567890abcdef"

# Option B: Set as Airflow variable
source venv/bin/activate
airflow variables set DATABRICKS_TOKEN "dapi1234567890abcdef"
```

### **3. Start Airflow**

**Terminal 1 - Webserver:**
```bash
cd airflow
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)
airflow webserver --port 8080
```

**Terminal 2 - Scheduler:**
```bash
cd airflow
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)
airflow scheduler
```

### **4. Access Airflow UI**

1. Open: http://localhost:8080
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. Find DAG: `lakehouse_taxi_pipeline`
4. Toggle it **ON** (unpause)
5. Click **Trigger DAG** to run immediately

## 📅 Schedule

- **Frequency:** Daily at 2:00 AM UTC
- **Catchup:** Disabled (won't backfill historical runs)
- **Max Active Runs:** 1 (prevents overlapping executions)
- **Retries:** 2 attempts with 5-minute delay

## 🗂️ Project Structure

```
airflow/
├── dags/
│   └── lakehouse_taxi_pipeline.py    ← Main DAG definition
├── plugins/                           ← Custom operators (empty for now)
├── logs/                              ← Task execution logs
├── venv/                              ← Python virtual environment
├── airflow.cfg                        ← Airflow configuration
├── airflow.db                         ← SQLite metadata database
├── requirements.txt                   ← Python dependencies
├── setup_airflow.sh                   ← Automated setup script
├── .env                               ← Environment variables
└── README.md                          ← This file
```

## 🔧 Configuration

### **Airflow Variables**

Set these in Airflow UI (Admin → Variables) or via CLI:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABRICKS_TOKEN` | Databricks Personal Access Token | `dapi1234...` |

### **Connection Configuration**

The DAG uses:
- **dbt profiles.yml** for Databricks connection
- **Environment variable** `DATABRICKS_TOKEN` for authentication
- **Task dependencies** ensure correct execution order

### **Task Groups**

The DAG is organized into logical task groups:

1. **bronze_layer** - 3 tasks
2. **silver_layer** - 2 tasks
3. **gold_layer** - 4 tasks (dbt)

This makes the Airflow UI cleaner and more readable.

## 🎨 Airflow UI Features

### **Graph View**
- Visual representation of task dependencies
- See task status at a glance
- Click tasks to view logs

### **Grid View**
- Historical DAG runs
- Task duration over time
- Success/failure patterns

### **Gantt Chart**
- Task execution timeline
- Identify bottlenecks
- Optimize parallelization

### **Task Logs**
- Real-time streaming logs
- Download logs for debugging
- Filter by log level

## 🧪 Testing the DAG

### **1. Test DAG Syntax**

```bash
python dags/lakehouse_taxi_pipeline.py
```

No output = syntax is correct!

### **2. Test Import**

```bash
airflow dags list
```

Should show `lakehouse_taxi_pipeline` in the list.

### **3. Test Individual Task**

```bash
# Test bronze ingestion
airflow tasks test lakehouse_taxi_pipeline bronze_layer.ingest_bronze_data 2026-05-14

# Test silver transformation
airflow tasks test lakehouse_taxi_pipeline silver_layer.transform_silver_data 2026-05-14

# Test dbt run
airflow tasks test lakehouse_taxi_pipeline gold_layer.dbt_run 2026-05-14
```

### **4. Run Full DAG**

```bash
# Trigger via CLI
airflow dags trigger lakehouse_taxi_pipeline

# Or use the UI (recommended)
```

## 📊 Monitoring & Observability

### **Key Metrics to Monitor**

1. **Task Duration**
   - Bronze ingestion: ~2-3 minutes
   - Silver transformation: ~3-5 minutes
   - Gold dbt run: ~5-10 minutes

2. **Data Volume**
   - Bronze records inserted
   - Silver records processed vs. rejected
   - Gold table sizes

3. **Data Quality**
   - dbt test pass rate (should be 40/40)
   - Data freshness checks
   - Schema validation

### **Alerts & Notifications**

The DAG can be extended to send alerts via:
- Email (configure SMTP in `airflow.cfg`)
- Slack (use Slack webhook)
- PagerDuty (for critical failures)

Example Slack notification:

```python
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

send_slack = SlackWebhookOperator(
    task_id='send_slack_notification',
    slack_webhook_conn_id='slack_webhook',
    message=':white_check_mark: Lakehouse pipeline completed!',
    username='Airflow Bot',
)
```

## 🔥 Troubleshooting

### **Issue: DAG not appearing in UI**

```bash
# Check for syntax errors
python dags/lakehouse_taxi_pipeline.py

# Check DAG bag
airflow dags list-import-errors
```

### **Issue: Tasks failing with "Import Error"**

Make sure `PYTHONPATH` includes the project root:

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/01-modern-lakehouse"
```

### **Issue: dbt tasks failing**

1. Check `DATABRICKS_TOKEN` is set:
   ```bash
   airflow variables get DATABRICKS_TOKEN
   ```

2. Test dbt connection:
   ```bash
   cd ../lakehouse_taxi
   dbt debug --profiles-dir .
   ```

3. Check dbt logs in Airflow UI

### **Issue: Database locked (SQLite)**

SQLite is single-threaded. For production, use PostgreSQL:

```bash
# Install PostgreSQL
brew install postgresql

# Update airflow.cfg
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost/airflow
```

## 🚀 Production Deployment

### **Recommended Setup**

1. **Executor:** CeleryExecutor or KubernetesExecutor
2. **Database:** PostgreSQL or MySQL
3. **Message Broker:** Redis or RabbitMQ (for Celery)
4. **Storage:** S3/GCS for logs (remote logging)
5. **Monitoring:** Prometheus + Grafana
6. **Secrets:** AWS Secrets Manager or HashiCorp Vault

### **Docker Deployment**

```bash
# Use official Airflow Docker image
docker-compose up
```

See [Airflow Docker documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

### **Cloud Options**

- **AWS:** Amazon Managed Workflows for Apache Airflow (MWAA)
- **GCP:** Cloud Composer
- **Azure:** Azure Data Factory (alternative)
- **Astronomer:** Managed Airflow platform

## 📚 Learning Resources

- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [dbt + Airflow Integration](https://docs.getdbt.com/docs/deploy/airflow)

## 🎯 Next Steps

1. ✅ **Run the pipeline** - Test end-to-end execution
2. 🔔 **Add notifications** - Slack/email alerts
3. 📊 **Add monitoring** - Track task duration trends
4. 🧪 **Add data quality sensors** - Wait for data before processing
5. 🔄 **Add backfill logic** - Handle historical data processing
6. 🚀 **Deploy to production** - Use managed Airflow service

## 📝 Notes

- The current DAG uses **runner scripts** (`bronze_ingestion_runner.py`, `silver_transformation_runner.py`) as wrappers
- For production, consider using **Databricks Jobs API** to run notebooks directly
- The Gold layer uses **dbt CLI** - ensure `DATABRICKS_TOKEN` is set
- Task groups improve UI readability for complex DAGs

---

**Built with ❤️ for data pipeline orchestration**

Last Updated: May 14, 2026
