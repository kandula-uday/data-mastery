# 🚀 Setup Guide

Complete step-by-step guide to get the project running.

## Prerequisites

### Required
- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Databricks Community Edition** (free account)

### Recommended
- **VS Code** with Python extension
- **DBeaver** or similar SQL client (for exploring data)
- **Postman** (for API testing)

---

## Step 1: Databricks Setup (15 minutes)

### 1.1 Create Account
1. Go to [Databricks Community Edition](https://community.cloud.databricks.com/login.html)
2. Sign up with your email (100% free, no credit card)
3. Verify your email

### 1.2 Create Cluster
1. In Databricks workspace, go to **Compute** → **Create Cluster**
2. Cluster settings:
   ```
   Cluster Name: lakehouse-cluster
   Cluster Mode: Single Node
   Databricks Runtime: 13.3 LTS (includes Apache Spark 3.4.1)
   Node Type: (default - auto-selected)
   Terminate after: 120 minutes of inactivity
   ```
3. Click **Create Cluster** (takes ~5 minutes to start)

### 1.3 Generate Access Token
1. Click your profile (top right) → **User Settings**
2. Go to **Access Tokens** tab
3. Click **Generate New Token**
   ```
   Comment: Local Development
   Lifetime: 90 days
   ```
4. **Copy the token immediately** (you won't see it again!)

---

## Step 2: Local Environment Setup (10 minutes)

### 2.1 Clone Repository
```bash
cd ~/Documents/Projects
git clone https://github.com/your-username/data-mastery.git
cd data-mastery/realworld-usecases/01-modern-lakehouse
```

### 2.2 Create Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\activate
```

### 2.3 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your preferred editor
```

Add your Databricks credentials:
```env
# .env
DATABRICKS_HOST=https://community.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef...
DATABRICKS_CLUSTER_ID=1234-567890-abc123
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
```

To find your cluster ID:
1. Go to Databricks → **Compute** → click your cluster
2. Copy the Cluster ID from the URL or cluster details

---

## Step 3: Data Setup (20 minutes)

### 3.1 Create Data Directories
```bash
# Local data directory
mkdir -p data/raw data/processed data/sample

# Databricks DBFS directories (run in Databricks notebook)
# Will create in Step 4
```

### 3.2 Download Sample Data
We'll use NYC Taxi data. For testing, download a sample:

**Option A: Small Sample (100K rows - recommended for testing)**
```bash
# Download sample
curl -o data/raw/yellow_tripdata_2023-01.parquet \
  https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet

# Preview locally
python scripts/preview_data.py data/raw/yellow_tripdata_2023-01.parquet
```

**Option B: Full Dataset (50M rows - for production)**
```bash
# Download all of 2023 (12 files, ~5GB)
bash scripts/download_full_dataset.sh
```

---

## Step 4: Databricks Workspace Setup (15 minutes)

### 4.1 Create Directories in DBFS
Create a notebook in Databricks and run:

```python
%python
# Create directory structure
dbutils.fs.mkdirs("dbfs:/FileStore/lakehouse/bronze/")
dbutils.fs.mkdirs("dbfs:/FileStore/lakehouse/silver/")
dbutils.fs.mkdirs("dbfs:/FileStore/lakehouse/gold/")

# Verify
display(dbutils.fs.ls("dbfs:/FileStore/lakehouse/"))
```

### 4.2 Upload Sample Data
```python
%python
# Upload from local (if file is small)
# Or use Databricks UI: Data → Create Table → Upload File

# Verify upload
display(spark.read.parquet("dbfs:/FileStore/lakehouse/bronze/yellow_tripdata_2023-01.parquet"))
```

### 4.3 Import Notebooks
1. In Databricks, go to **Workspace** → **Users** → your email
2. Right-click → **Import**
3. Upload all notebooks from `notebooks/` folder

Notebooks to import:
- `01_bronze_ingestion.py`
- `02_silver_transformation.py`
- `03_gold_aggregation.py`
- `04_exploratory_analysis.ipynb`

---

## Step 5: Test Connection (5 minutes)

### 5.1 Test from Local Machine
```bash
python scripts/test_connection.py
```

Expected output:
```
✓ Databricks connection successful
✓ Cluster status: RUNNING
✓ Can read from DBFS
✓ Spark session created
```

### 5.2 Run First Notebook
1. Open `01_bronze_ingestion.py` in Databricks
2. Attach to your cluster
3. Run all cells
4. Verify Bronze table created:
   ```sql
   %sql
   SHOW TABLES IN bronze;
   SELECT COUNT(*) FROM bronze.raw_trips;
   ```

---

## Step 6: dbt Setup (Optional - Day 6)

### 6.1 Initialize dbt Project
```bash
cd dbt_project

# Install dbt for Databricks
pip install dbt-databricks

# Initialize profiles
dbt init
```

### 6.2 Configure profiles.yml
Edit `~/.dbt/profiles.yml`:
```yaml
lakehouse_taxi:
  target: dev
  outputs:
    dev:
      type: databricks
      host: community.cloud.databricks.com
      http_path: /sql/1.0/warehouses/your-warehouse-id
      token: "{{ env_var('DATABRICKS_TOKEN') }}"
      schema: silver
      threads: 4
```

### 6.3 Test dbt Connection
```bash
dbt debug
dbt run --select staging
```

---

## Step 7: Streamlit Dashboard (Optional - Day 8)

### 7.1 Create Secrets File
```bash
mkdir -p ~/.streamlit
cat > ~/.streamlit/secrets.toml << EOF
[databricks]
host = "community.cloud.databricks.com"
http_path = "/sql/1.0/warehouses/your-warehouse-id"
token = "your-token-here"
EOF
```

### 7.2 Run Dashboard Locally
```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

Opens in browser at `http://localhost:8501`

---

## Troubleshooting

### Issue: "Cluster not found"
**Solution:** Update `DATABRICKS_CLUSTER_ID` in `.env`
```bash
# Get cluster ID from Databricks UI
# Compute → Your Cluster → URL or Details tab
```

### Issue: "Token authentication failed"
**Solution:** Generate a new token
```bash
# Databricks → User Settings → Access Tokens → Generate New Token
# Update DATABRICKS_TOKEN in .env
```

### Issue: "Module not found"
**Solution:** Ensure virtual environment is activated
```bash
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Issue: "Cannot connect to Databricks SQL Warehouse"
**Solution:** Create SQL Warehouse (for Streamlit)
1. Databricks → **SQL** → **SQL Warehouses**
2. Create new warehouse (free tier: X-Small)
3. Copy HTTP Path from details
4. Update in `.env` and `secrets.toml`

### Issue: "Data file not found"
**Solution:** Verify DBFS path
```python
# In Databricks notebook
display(dbutils.fs.ls("dbfs:/FileStore/lakehouse/bronze/"))
```

---

## Verification Checklist

Before starting Day 1 implementation:

- [ ] Databricks account created and cluster running
- [ ] Local Python environment set up (3.9+)
- [ ] Dependencies installed (`pip list`)
- [ ] `.env` file configured with valid credentials
- [ ] Test connection script passes
- [ ] Sample data downloaded
- [ ] Databricks notebooks imported
- [ ] DBFS directories created

---

## Next Steps

✅ Setup complete! Now you're ready to start:

👉 **Go to [Day 1 of the Implementation Plan](./day-by-day-plan.md#day-1)**

---

## Useful Commands

```bash
# Activate environment
source venv/bin/activate

# Update dependencies
pip install --upgrade -r requirements.txt

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 src/

# dbt commands
dbt run
dbt test
dbt docs generate
dbt docs serve

# Streamlit
streamlit run dashboard/app.py
```

---

## Resources

- [Databricks Community Edition](https://community.cloud.databricks.com/)
- [NYC Taxi Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Delta Lake Docs](https://docs.delta.io/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Streamlit Docs](https://docs.streamlit.io/)

---

Need help? Check the [Troubleshooting](#troubleshooting) section or open an issue on GitHub.
