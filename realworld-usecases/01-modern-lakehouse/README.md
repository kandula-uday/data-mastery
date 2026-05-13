# 🏗️ Modern Data Lakehouse with Databricks

A complete end-to-end data lakehouse implementation using the medallion architecture, showcasing real-world data engineering patterns.

## 🎯 Project Overview

Build a production-grade data lakehouse using:
- **Databricks Community Edition** (100% free)
- **Delta Lake** for ACID transactions
- **Public datasets** (NYC Taxi data, COVID-19 data)
- **Medallion Architecture** (Bronze → Silver → Gold)
- **dbt** for transformations
- **Streamlit** dashboard for visualization

## 🏛️ Architecture

```
📥 Raw Data Sources (CSV/JSON/APIs)
    ↓
🥉 Bronze Layer (Raw ingestion, Delta tables)
    ↓
🥈 Silver Layer (Cleaned, validated, conformed)
    ↓
🥇 Gold Layer (Business-level aggregates)
    ↓
📊 Analytics Layer (Streamlit Dashboard)
```

## 📂 Project Structure

```
01-modern-lakehouse/
├── README.md                 # This file
├── docs/
│   ├── architecture.md       # Detailed architecture docs
│   ├── day-by-day-plan.md    # 10-day implementation plan
│   └── setup-guide.md        # Step-by-step setup
├── notebooks/
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_transformation.py
│   ├── 03_gold_aggregation.py
│   └── 04_exploratory_analysis.ipynb
├── dbt_project/
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   ├── tests/
│   └── dbt_project.yml
├── src/
│   ├── data_ingestion/
│   │   ├── fetch_data.py
│   │   └── utils.py
│   ├── data_quality/
│   │   └── great_expectations_suite.py
│   └── config/
│       └── config.yaml
├── dashboard/
│   ├── app.py                # Streamlit dashboard
│   ├── pages/
│   └── requirements.txt
├── tests/
│   ├── test_transformations.py
│   └── test_data_quality.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
└── setup.sh
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Databricks Community Edition account (free)
- Git

### Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up Databricks token
cp .env.example .env
# Add your Databricks token to .env

# 3. Run setup script
bash setup.sh

# 4. Launch Databricks notebooks
# Upload notebooks/ folder to your Databricks workspace
```

## 📊 Dataset

**NYC Taxi Trip Data** (Jan-Dec 2023)
- ~50M records
- Trip details, fares, locations
- Public domain data

## 🎯 What You'll Learn

### Data Engineering
- ✅ Medallion architecture implementation
- ✅ Delta Lake table management
- ✅ Incremental processing patterns
- ✅ Data partitioning strategies
- ✅ Schema evolution handling

### Data Quality
- ✅ Great Expectations validation
- ✅ dbt tests (schema, data, custom)
- ✅ Anomaly detection

### Orchestration
- ✅ Databricks Jobs scheduling
- ✅ Dependency management
- ✅ Error handling & retry logic

### Analytics
- ✅ Real-time Streamlit dashboard
- ✅ Plotly visualizations
- ✅ Business metrics calculation

## 📅 10-Day Implementation Plan

### **Week 1: Foundation**
- **Day 1-2:** Setup Databricks, ingest raw data (Bronze)
- **Day 3-4:** Data cleaning & validation (Silver)
- **Day 5:** Business aggregations (Gold)

### **Week 2: Production-Ready**
- **Day 6-7:** dbt transformations & tests
- **Day 8:** Streamlit dashboard
- **Day 9:** CI/CD with GitHub Actions
- **Day 10:** Documentation & optimization

See [docs/day-by-day-plan.md](./docs/day-by-day-plan.md) for detailed tasks.

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Storage | Delta Lake | ACID transactions, time travel |
| Compute | Databricks | Distributed processing |
| Transformation | dbt | SQL-based transformations |
| Quality | Great Expectations | Data validation |
| Orchestration | Databricks Jobs | Workflow scheduling |
| Visualization | Streamlit + Plotly | Interactive dashboard |
| CI/CD | GitHub Actions | Automated testing |

## 📈 Key Metrics Dashboard

The Streamlit dashboard will display:
- 📊 Trip volume trends
- 💰 Revenue analytics
- 🗺️ Geographic heatmaps
- ⏱️ Peak hour analysis
- 🚕 Tip patterns

## 🧪 Testing Strategy

```python
# Unit tests for transformations
pytest tests/

# dbt tests
dbt test

# Great Expectations validation
great_expectations checkpoint run bronze_checkpoint
```

## 🔄 CI/CD Pipeline

GitHub Actions workflow:
1. ✅ Lint code (black, flake8)
2. ✅ Run unit tests
3. ✅ Validate dbt models
4. ✅ Deploy to Databricks
5. ✅ Run data quality checks

## 📚 Documentation

- [Architecture Overview](./docs/architecture.md)
- [Day-by-Day Implementation Plan](./docs/day-by-day-plan.md)
- [Setup Guide](./docs/setup-guide.md)
- [Best Practices](./docs/best-practices.md)

## 🎓 Learning Outcomes

After completing this project, you'll be able to:
- Design and implement medallion architecture
- Work with Delta Lake at scale
- Write production-grade dbt transformations
- Implement comprehensive data quality checks
- Build interactive analytics dashboards
- Set up CI/CD for data pipelines

## 🤝 Contributing

This is a learning portfolio project. Feel free to fork and adapt!

## 📄 License

MIT License - feel free to use for learning and portfolio purposes.

---

**Status:** 🟢 Active Development  
**Last Updated:** May 13, 2026  
**Estimated Completion:** May 23, 2026 (10 days)

---

⭐ **Next Steps:** Start with [Day 1 Setup Guide](./docs/day-by-day-plan.md#day-1)
