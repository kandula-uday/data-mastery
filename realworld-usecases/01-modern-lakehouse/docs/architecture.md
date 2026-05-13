# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                             │
│  • NYC Taxi Trip Data (CSV)                                     │
│  • Public APIs                                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                             │
│  • Python scripts (batch ingestion)                             │
│  • Databricks notebooks                                         │
│  • Schema inference & validation                                │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                 🥉 BRONZE LAYER (Raw)                           │
│  Storage: Delta Lake                                            │
│  • Raw data as-is from source                                   │
│  • Append-only writes                                           │
│  • Metadata: ingestion_timestamp, source_file                   │
│  • Partitioned by: pickup_date                                  │
│  • Table: bronze.raw_trips                                      │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│          DATA QUALITY & VALIDATION                              │
│  • Great Expectations                                           │
│  • Schema validation                                            │
│  • Business rule checks                                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                 🥈 SILVER LAYER (Cleaned)                       │
│  Storage: Delta Lake                                            │
│  • Deduplicated records                                         │
│  • Type casting & standardization                               │
│  • Null handling & data cleaning                                │
│  • Business-friendly column names                               │
│  • Partitioned by: pickup_date                                  │
│  • Table: silver.trips                                          │
│  • Transformation: dbt models                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                 🥇 GOLD LAYER (Business)                        │
│  Storage: Delta Lake                                            │
│  • Aggregated metrics                                           │
│  • Business KPIs                                                │
│  • Tables:                                                       │
│    - gold.daily_summary                                         │
│    - gold.hourly_patterns                                       │
│    - gold.top_routes                                            │
│    - gold.revenue_metrics                                       │
│  • Optimized for analytics queries                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYTICS LAYER                              │
│  • Streamlit Dashboard                                          │
│  • Plotly visualizations                                        │
│  • Real-time filtering                                          │
│  • Databricks SQL Warehouse connection                          │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Storage & Compute
- **Delta Lake**: ACID transactions, time travel, schema evolution
- **Databricks**: Unified analytics platform
- **PySpark**: Distributed data processing

### Transformation
- **dbt (data build tool)**: SQL-based transformations
  - Models for Silver and Gold layers
  - Incremental materialization
  - Built-in testing framework

### Data Quality
- **Great Expectations**: Data validation framework
  - Expectation suites for each layer
  - Automated validation checkpoints
  - Data documentation generation

### Orchestration
- **Databricks Jobs**: Workflow scheduling
  - Bronze ingestion job (daily)
  - Silver transformation job (hourly)
  - Gold aggregation job (hourly)

### Visualization
- **Streamlit**: Interactive web application
- **Plotly**: Rich, interactive charts
- **Databricks SQL**: Query engine

### CI/CD
- **GitHub Actions**: Automated testing and deployment
- **pytest**: Unit testing
- **black & flake8**: Code quality

## Data Flow

### 1. Ingestion (Bronze)
```python
Raw CSV → Spark DataFrame → Delta Table (Bronze)
- Add metadata columns
- Partition by date
- Append mode
- No transformations
```

### 2. Cleaning (Silver)
```python
Bronze Delta → dbt models → Silver Delta
- Remove duplicates
- Validate data types
- Apply business rules
- Standardize formats
```

### 3. Aggregation (Gold)
```python
Silver Delta → dbt models → Gold Delta
- Calculate KPIs
- Create dimension tables
- Build fact tables
- Optimize for queries
```

### 4. Visualization
```python
Gold Delta → Databricks SQL → Streamlit
- Live dashboard updates
- Interactive filters
- Cached queries
```

## Key Design Patterns

### 1. **Medallion Architecture**
- **Bronze**: Raw, immutable data
- **Silver**: Cleaned, conformed data
- **Gold**: Business-level aggregates

### 2. **Incremental Processing**
```python
# Silver layer - process only new records
{% if is_incremental() %}
  WHERE pickup_datetime > (SELECT MAX(pickup_datetime) FROM {{ this }})
{% endif %}
```

### 3. **Schema Evolution**
```python
# Delta Lake handles schema changes
df.write
  .format("delta")
  .mode("append")
  .option("mergeSchema", "true")
  .save(path)
```

### 4. **Data Quality Gates**
```python
# Fail pipeline if validation fails
if not validation_result.success:
    raise DataQualityError("Silver layer validation failed")
```

## Performance Optimizations

### 1. **Partitioning**
- Partition by `pickup_date` for time-based queries
- Reduces data scanned per query

### 2. **Z-Ordering**
```python
OPTIMIZE silver.trips
ZORDER BY (pickup_location_id, dropoff_location_id)
```

### 3. **Caching**
```python
# Cache frequently accessed Gold tables
spark.sql("CACHE TABLE gold.daily_summary")
```

### 4. **Adaptive Query Execution**
```python
# Enabled by default in Databricks
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

## Security & Governance

### Access Control
- **Bronze**: Write by ingestion service only
- **Silver**: Read/Write by data engineers
- **Gold**: Read-only for analysts and dashboards

### Data Lineage
- Track data flow through metadata
- dbt docs show transformation lineage
- Delta Lake transaction log

### Audit Trail
- All changes logged in Delta transaction log
- Time travel to any previous version
- Who, what, when for all writes

## Scalability

### Current: 50M records
- Processing time: ~30 minutes (end-to-end)
- Storage: ~10 GB (Delta compressed)

### Scale to 500M records
- Add more compute (auto-scaling cluster)
- Partition optimization
- Incremental processing
- Expected processing: ~2 hours

### Scale to 5B records
- Multi-cluster approach
- Streaming ingestion with Kafka
- Pre-aggregation strategies
- Expected processing: Real-time streaming

## Disaster Recovery

### Backup Strategy
- Delta Lake transaction log
- Time travel up to 30 days
- Point-in-time recovery

### Recovery Process
```python
# Restore to specific version
df = spark.read
  .format("delta")
  .option("versionAsOf", 42)
  .load("/path/to/table")

# Or timestamp
df = spark.read
  .format("delta")
  .option("timestampAsOf", "2026-05-10")
  .load("/path/to/table")
```

## Monitoring & Alerting

### Key Metrics
- Ingestion success rate
- Data quality scores
- Processing latency
- Query performance

### Alerting
- Failed job notifications (Slack/Email)
- Data quality violations
- SLA breaches

## Cost Optimization

### Databricks
- Use job clusters (auto-terminate)
- Right-size cluster for workload
- Spot instances for non-critical jobs

### Storage
- Delta Lake compression
- Vacuum old versions
- Archive cold data

---

## References

- [Delta Lake Documentation](https://docs.delta.io/)
- [Databricks Lakehouse Platform](https://www.databricks.com/product/data-lakehouse)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Great Expectations](https://greatexpectations.io/)
