# 🚀 Quick Start Guide - FinanceFlow ETL Pipeline

## 5-Minute Setup

### Step 1: Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/data-mastery.git
cd data-mastery/financeflow-etl-pipeline

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Pipeline
```bash
python test_transaction_processing.py
```

### Step 3: Check the Results
```bash
# Valid records
ls -lh data/processed/

# Invalid records
ls -lh data/invalid/
```

---

## 📊 What You'll See

```
============================================================
TRANSACTION PROCESSING SUMMARY
============================================================
Timestamp:        2026-05-28 12:59:41
Total Records:    15,900
Valid Records:    12,851
Invalid Records:  3,049
Duplicate Records: 1,729
Success Rate:     80.82%
============================================================
```

---

## 🔍 View the Output

### Valid Records
```python
import pandas as pd

df = pd.read_csv('data/processed/processed_transactions_<timestamp>.csv')
print(df.head())
```

### Invalid Records
```python
df_invalid = pd.read_csv('data/invalid/invalid_transactions_<timestamp>.csv')
print(df_invalid[['transaction_id', 'failure_reasons']].head())
```

---

## 🎯 Run Individual Components

### Test Date Validation
```bash
python tests/test_date_formats.py
```

### Test Amount Validation
```bash
python tests/test_amount_formats.py
```

### Test Category Validation
```bash
python tests/test_category_formats.py
```

---

## 💡 Use in Your Code

```python
from app.services.transaction_processing_service import process_transaction_file

# Process your own CSV file
result = process_transaction_file('path/to/your/data.csv')

print(f"Valid: {result['valid_records']}")
print(f"Invalid: {result['invalid_records']}")
print(f"Success Rate: {result['success_rate']}%")
```

---

## 🛠️ Customize for Your Data

### 1. Update Date Formats
Edit `app/utils/date_cleaner.py` to add your date formats:
```python
date_formats = [
    '%Y-%m-%d',      # Your format here
    '%m/%d/%Y',
    # Add more formats
]
```

### 2. Update Category List
Edit `app/validations/category_validator.py`:
```python
VALID_CATEGORIES = {
    'YourCategory1',
    'YourCategory2',
    # Add your categories
}
```

### 3. Adjust Amount Limits
Edit `app/validations/amount_validator.py`:
```python
if amount_float > 100000000:  # Change this limit
    return False, f"Amount exceeds maximum limit"
```

---

## 📚 Next Steps

1. ✅ Read the full [README.md](README.md)
2. ✅ Check [PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) for detailed documentation
3. ✅ Explore the code in `app/` directory
4. ✅ Run all tests in `tests/` directory
5. ✅ Customize for your own data

---

## 🆘 Troubleshooting

### Issue: Module not found
```bash
# Make sure you're in the project root directory
cd financeflow-etl-pipeline

# Set PYTHONPATH (if needed)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: File not found
```bash
# Make sure the data file exists
ls data/raw/budgetwise_finance_dataset.csv
```

### Issue: Pandas not installed
```bash
pip install pandas
```

---

## 🎉 You're Ready!

The ETL pipeline is now ready to process your financial transaction data!

**Questions?** Check the [full documentation](README.md) or open an issue on GitHub.
