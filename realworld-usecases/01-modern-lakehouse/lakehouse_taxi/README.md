# 🎯 dbt Project: Lakehouse Taxi Analytics

## 📋 Project Overview

This dbt project transforms taxi trip data using the **medallion architecture**, creating production-ready Gold layer analytics tables in Databricks Delta Lake.

### **Architecture**

```
Bronze Layer (Raw Data)
    ↓
Silver Layer (Cleaned Data)  
    ↓
🎯 dbt Gold Layer (Business Metrics) ← YOU ARE HERE
    ↓
Dashboard & Analytics
```

---

## 🏗️ What We Built

### **4 Gold Layer Models**

| Model | Type | Purpose | Key Metrics |
|-------|------|---------|-------------|
| `gold_daily_summary` | Incremental | Daily business metrics | Revenue, trips, tips, distances |
| `gold_hourly_patterns` | Incremental | Demand patterns by hour | Peak hours, revenue distribution |
| `gold_top_routes` | Table | Most popular routes | Route profitability, rankings |
| `gold_revenue_by_payment` | Incremental | Payment method analysis | Payment trends, tip behavior |

---

## ✅ Key Features Implemented

### 1. **Incremental Materialization** ⚡
```sql
{{ config(
    materialized='incremental',
    unique_key='pickup_date',
    incremental_strategy='merge'
) }}

{% if is_incremental() %}
  WHERE pickup_date > (SELECT MAX(pickup_date) FROM {{ this }})
{% endif %}
```

**Benefit:** Only processes new data, saves compute costs!

### 2. **Data Quality Tests** 🧪

**40 automated tests** across all models:
- `unique` - Ensures no duplicates
- `not_null` - Required fields validation
- `accepted_range` - Bounds checking (e.g., tip_percentage 0-100%)
- `accepted_values` - Enum validation (e.g., time periods)
- `recency` - Data freshness checks

### 3. **Comprehensive Documentation** 📚
- Column descriptions
- Business logic comments
- Use case documentation
- Lineage tracking

### 4. **Delta Lake Optimization** 🚀
```sql
{{ config(
    file_format='delta',
    partition_by=['pickup_date']
) }}
```

---

## 🚀 How to Use

### **Development Workflow**
```bash
# Run specific model
dbt run --select gold_daily_summary

# Run model and tests
dbt build --select gold_daily_summary

# Run all Gold models
dbt run --select gold.*

# Test specific model
dbt test --select gold_revenue_by_payment

# Generate documentation
dbt docs generate
dbt docs serve
```

---

## 🎓 Portfolio Highlights

✅ **dbt Core Concepts:**
- Materialization strategies (incremental, table, view)
- Jinja templating for dynamic SQL
- Sources and models architecture
- Configuration management

✅ **Data Engineering Best Practices:**
- Incremental processing patterns
- 40+ automated data quality tests
- Documentation generation
- DAG dependency management

✅ **Production Patterns:**
- Idempotent transformations
- Merge strategies for updates
- Error handling with severity levels
- Performance optimization with partitioning

---

**Built with:** dbt Core 1.11.8, dbt-databricks 1.11.8, Delta Lake 🚀
