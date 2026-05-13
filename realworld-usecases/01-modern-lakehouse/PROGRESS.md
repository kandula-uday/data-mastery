# 🏗️ Modern Data Lakehouse - Implementation Progress

## ✅ Current Status: **Phase 1 Complete - Core Pipeline Built**

A production-ready data lakehouse implementation using the medallion architecture with Databricks Community Edition and Delta Lake.

---

## 🎯 What's Been Built

### **Core Data Pipeline (100% Complete)**
- ✅ **Bronze Layer**: Raw CSV ingestion with metadata tracking
- ✅ **Silver Layer**: Data cleaning, deduplication, and transformation
- ✅ **Gold Layer**: Business aggregations (daily metrics, route analysis, revenue tracking)
- ✅ **Delta Lake**: All layers using Delta format for ACID transactions
- ✅ **Managed Tables**: Production-ready table architecture in Databricks

### **Architecture**
```
NYC Taxi CSV Files
    ↓
🥉 Bronze Layer: bronze_raw_trips
   - Raw data ingestion
   - Metadata columns (ingested_at, source_file, batch_id)
   - Partitioned by pickup_date
    ↓
🥈 Silver Layer: silver_trips
   - Deduplication logic
   - Data quality filters (fare > 0, distance > 0, valid durations)
   - Calculated fields (trip_duration, tip_percentage)
   - Date/time parsing and enrichment
    ↓
🥇 Gold Layer: Business Analytics Tables
   - gold_daily_summary (trip counts, revenue per day)
   - gold_hourly_patterns (peak hours, location trends)
   - gold_top_routes (most popular pickup/dropoff combinations)
   - gold_revenue_metrics (payment type analysis)
```

---

## 📊 Implementation Details

### **Technologies Used**
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Compute Platform | Databricks Community Edition | Managed Spark clusters |
| Storage Format | Delta Lake | ACID transactions, time travel |
| Processing Engine | PySpark 3.4.1 | Distributed data processing |
| Table Management | Databricks Managed Tables | Automated storage & catalog |
| Data Source | NYC Taxi Dataset (CSV) | Real-world trip records |

### **Key Learning Outcomes**
✅ **Medallion Architecture** - Bronze/Silver/Gold layer design patterns  
✅ **Data Quality** - Handling duplicates, nulls, and invalid records  
✅ **PySpark Transformations** - groupBy, agg, window functions, filters  
✅ **Delta Lake Features** - ACID transactions, schema evolution, partitioning  
✅ **Deduplication Strategy** - Business key identification without unique IDs  
✅ **Metadata Tracking** - Augmented Bronze approach for data lineage  
✅ **API Integration** - Fetch data from Databricks for local development  

---

## 🚀 How to Run

### **Prerequisites**
1. Databricks Community Edition account
2. Python 3.11+ (for local development)
3. Git for version control

### **Setup Steps**
```bash
# 1. Clone the repository
git clone https://github.com/kandula-uday/data-mastery.git
cd data-mastery/realworld-usecases/01-modern-lakehouse

# 2. Set up Python environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure Databricks credentials
cp .env.example .env
# Edit .env with your Databricks token and cluster details

# 4. Test connection
python scripts/test_connection.py
```

### **Running the Pipeline in Databricks**

**Step 1: Bronze Layer**
```python
# In Databricks notebook
bronze = spark.read.format("csv") \
    .option("header", "true") \
    .load("dbfs:/databricks-datasets/nyctaxi/tripdata/yellow/...")

# Add metadata
bronze = bronze.withColumn("ingested_at", current_timestamp())
bronze.write.saveAsTable("bronze_raw_trips")
```

**Step 2: Silver Layer**
```python
# Transform
silver = transform_to_silver(spark.table("bronze_raw_trips"))
silver.write.saveAsTable("silver_trips")
```

**Step 3: Gold Layer**
```python
# Create business aggregates
create_gold_aggregates(spark.table("silver_trips"))
```

---

## 📁 Project Structure

```
01-modern-lakehouse/
├── notebooks/
│   ├── 01_bronze_ingestion.py          ✅ Complete
│   ├── 02_silver_transformation.py     ✅ Complete
│   └── 03_gold_aggregation.py          ✅ Complete
├── scripts/
│   ├── test_connection.py              ✅ Databricks SQL connector test
│   └── fetch_and_process_locally.py    ✅ Local dev with API
├── docs/
│   ├── architecture.md                 ✅ Architecture documentation
│   ├── day-by-day-plan.md             ✅ Implementation guide
│   ├── virtual-environments-explained.md ✅ Setup concepts
│   └── corporate-databricks-setup.md   ✅ Enterprise guide
├── data/
│   └── processed/                      ✅ Local testing data
├── dashboard/
│   └── app.py                          ⏳ Planned (Streamlit)
├── tests/
│   └── test_transformations.py         ⏳ Planned (pytest)
├── .github/workflows/
│   └── ci.yml                          ⏳ Planned (CI/CD)
├── requirements.txt                     ✅ Complete
├── .env.example                         ✅ Complete
└── README.md                            ✅ This file
```

---

## 🎓 Key Challenges & Solutions

### **Challenge 1: Dataset Path Not Found**
**Problem**: Databricks sample paths varied between Community/Enterprise editions  
**Solution**: Explored DBFS with `dbutils.fs.ls()`, found actual data locations

### **Challenge 2: Column Name Mismatches**
**Problem**: Expected `tpep_pickup_datetime` but dataset had `Trip_Pickup_DateTime`  
**Solution**: Always check schema first with `.printSchema()`, adapt to actual column names

### **Challenge 3: DBFS Write Permissions**
**Problem**: `/FileStore/` path blocked in Community Edition  
**Solution**: Switched to managed tables with `.saveAsTable()` - better practice anyway!

### **Challenge 4: Deduplication Without Unique IDs**
**Problem**: No trip_id or taxi medallion to identify duplicates  
**Solution**: Composite business key using timestamp + location + distance + passengers

### **Challenge 5: Local Spark Setup Complexity**
**Problem**: Java version conflicts, missing metastore for local testing  
**Solution**: Use Databricks SQL API to fetch sample data, process with pandas locally

---

## 📈 Data Pipeline Metrics

**Bronze Layer**
- Source: Databricks sample NYC Taxi dataset
- Records ingested: ~50,000+ trips
- Partitioning: By pickup_date
- Schema: 22 columns (original + metadata)

**Silver Layer**
- Duplicates removed: ~1-2% of records
- Invalid records filtered: ~5-10% (negative fares, zero distance)
- Transformations: 8 new calculated fields
- Data quality: 100% fare > 0, distance > 0, valid durations

**Gold Layer**
- 4 aggregate tables created
- Daily summaries: 31+ days of data
- Hourly patterns: 24 hours × multiple locations
- Top routes: Top 100 most popular routes

---

## 🔮 Next Steps (Phase 2)

### **Planned Enhancements**
- [ ] **Streamlit Dashboard**: Interactive visualization of Gold layer metrics
- [ ] **Unit Tests**: pytest suite for transformation logic
- [ ] **CI/CD Pipeline**: GitHub Actions for automated testing
- [ ] **Data Quality Checks**: Great Expectations integration
- [ ] **Incremental Loading**: Append mode with watermarking
- [ ] **dbt Integration**: SQL-based transformations
- [ ] **Schema Evolution**: Handle source schema changes gracefully

---

## 📚 Documentation

- [Architecture Deep Dive](docs/architecture.md)
- [Day-by-Day Implementation Plan](docs/day-by-day-plan.md)
- [Virtual Environments Explained](docs/virtual-environments-explained.md)
- [Corporate Databricks Setup](docs/corporate-databricks-setup.md)

---

## 🤝 Contributing

This is a learning project, but feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📝 License

This project is for educational purposes. The NYC Taxi dataset is publicly available.

---

## 🙏 Acknowledgments

- NYC Taxi & Limousine Commission for the open dataset
- Databricks for free Community Edition
- Delta Lake community for excellent documentation

---

## 📧 Contact

**Uday Shankar Kandula**  
GitHub: [@kandula-uday](https://github.com/kandula-uday)

---

**⭐ If this helped you learn data engineering, please star the repo!**
