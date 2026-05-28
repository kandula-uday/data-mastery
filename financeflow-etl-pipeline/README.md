# FinanceFlow ETL Pipeline 🚀

A production-ready **ETL (Extract, Transform, Load) pipeline** for processing financial transaction data. This project demonstrates data cleaning, validation, and transformation techniques on real-world messy financial data.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Data Quality](https://img.shields.io/badge/Success_Rate-80.82%25-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution Architecture](#solution-architecture)
- [Dataset](#dataset)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Key Learnings](#key-learnings)
- [Technologies Used](#technologies-used)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**FinanceFlow ETL Pipeline** processes messy financial transaction data and transforms it into clean, validated, and standardized records. The system handles real-world data quality issues including:

- Multiple date formats
- Various currency notations
- Typographical errors in categories
- Missing data
- Duplicate transactions
- Invalid amounts

**Key Metrics:**
- ✅ **15,900** transactions processed
- ✅ **80.82%** success rate
- ✅ **12,851** valid records extracted
- ⚡ **< 2 seconds** processing time

---

## 🔍 Problem Statement

Financial data often arrives in inconsistent formats with quality issues. This project tackles common real-world challenges:

### **Data Quality Issues Found:**

| Issue Type | Examples | Count |
|------------|----------|-------|
| **Date Formats** | `2023-04-25`, `08/05/2022`, `31-12-23`, `22-06-2023` | 4 formats |
| **Currency Symbols** | `Rs.828`, `₹5070`, `$4262`, `5107 INR` | 5 variations |
| **Category Typos** | `Fod`, `Educaton`, `Utilties`, `Rentt`, `Helth` | 40+ typos |
| **Case Issues** | `FOOD`, `food`, `Food` | Multiple |
| **Missing Data** | Empty dates, amounts, categories | 1,320 records |
| **Duplicates** | Same transaction_id appearing multiple times | 1,729 records |
| **Invalid Values** | Amounts exceeding limits | ~100 records |

---

## 🏗️ Solution Architecture

### **ETL Pipeline Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│                      RAW CSV DATA                           │
│                   15,900 Transactions                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTRACT PHASE                             │
│  - Load CSV file using Pandas                               │
│  - Parse 15,900 transaction records                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  TRANSFORM PHASE                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  VALIDATION LAYER                                    │  │
│  │  • Date Validator    → Check format & range          │  │
│  │  • Amount Validator  → Check positive & limit        │  │
│  │  • Category Validator → Check against allowed list   │  │
│  │  • Duplicate Detector → Track transaction IDs        │  │
│  └──────────────────────────────────────────────────────┘  │
│                        │                                     │
│                        ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CLEANING LAYER                                      │  │
│  │  • Date Cleaner      → Standardize to YYYY-MM-DD    │  │
│  │  • Amount Cleaner    → Remove currency symbols       │  │
│  │  • Category Cleaner  → Fix typos & standardize       │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                     LOAD PHASE                              │
│                                                              │
│  ┌────────────────────────┐   ┌─────────────────────────┐  │
│  │   VALID RECORDS        │   │   INVALID RECORDS       │  │
│  │   12,851 (80.82%)      │   │   3,049 (19.18%)        │  │
│  │   ✅ Clean & Ready     │   │   ❌ With Error Reasons │  │
│  └────────────────────────┘   └─────────────────────────┘  │
│           │                              │                  │
│           ▼                              ▼                  │
│    processed/                       invalid/                │
│    folder                           folder                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Dataset

**Source:** [Kaggle - BudgetWise Finance Dataset](https://www.kaggle.com/)

**Description:** Real-world financial transaction data with intentional data quality issues to simulate production scenarios.

**Columns:**
- `transaction_id` - Unique transaction identifier
- `date` - Transaction date (multiple formats)
- `amount` - Transaction amount (with currency symbols)
- `category` - Transaction category (with typos)
- `transaction_type` - Credit/Debit
- `payment_mode` - Payment method
- `location` - Transaction location
- `notes` - Additional notes

**Statistics:**
- **Total Records:** 15,900
- **Date Range:** 2021-2024
- **Categories:** 18 standard categories
- **Amount Range:** $1 - $100M

---

## ✨ Features

### **1. Multi-Format Date Handling**
Supports and standardizes 4+ date formats:
- `YYYY-MM-DD` → 2023-04-25
- `MM/DD/YYYY` → 08/05/2022
- `DD-MM-YY` → 31-12-23
- `DD-MM-YYYY` → 22-06-2023

### **2. Currency Symbol Removal**
Handles various currency notations:
- `Rs.828` → 828.0
- `₹5070` → 5070.0
- `$4262` → 4262.0
- `5107 INR` → 5107.0

### **3. Intelligent Category Cleaning**
Fixes 40+ typos and variations:
- `Fod` → `Food`
- `Educaton` → `Education`
- `Utilties` → `Utilities`
- `Entertain` → `Entertainment`

### **4. Data Validation**
- ✅ Missing field detection
- ✅ Duplicate transaction detection
- ✅ Future date validation
- ✅ Amount range validation
- ✅ Category whitelist validation

### **5. Error Tracking**
- Invalid records saved separately with failure reasons
- Detailed logging of data quality issues
- Processing summary with statistics

---

## 📁 Project Structure

```
financeflow-etl-pipeline/
│
├── app/
│   ├── validations/
│   │   ├── __init__.py
│   │   ├── date_validator.py          # Date validation logic
│   │   ├── amount_validator.py        # Amount validation logic
│   │   └── category_validator.py      # Category validation logic
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── date_cleaner.py            # Date cleaning/normalization
│   │   ├── amount_cleaner.py          # Amount cleaning/normalization
│   │   └── category_cleaner.py        # Category cleaning/normalization
│   │
│   └── services/
│       ├── __init__.py
│       └── transaction_processing_service.py  # Main ETL orchestration
│
├── data/
│   ├── raw/
│   │   └── budgetwise_finance_dataset.csv     # Original dataset
│   │
│   ├── processed/                              # Clean output (auto-generated)
│   │   └── processed_transactions_<timestamp>.csv
│   │
│   └── invalid/                                # Invalid records (auto-generated)
│       └── invalid_transactions_<timestamp>.csv
│
├── tests/
│   ├── test_date_formats.py           # Date validator tests
│   ├── test_amount_formats.py         # Amount validator tests
│   ├── test_category_formats.py       # Category validator tests
│   └── test_transaction_processing.py # Integration tests
│
├── docs/
│   ├── PROJECT_SUMMARY.md             # Detailed project summary
│   ├── TRANSACTION_PROCESSING_README.md
│   ├── AMOUNT_FORMATS_README.md
│   └── CATEGORY_FORMATS_README.md
│
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
└── .gitignore
```

---

## 🚀 Installation

### **Prerequisites:**
- Python 3.8+
- pip or conda

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/data-mastery.git
cd data-mastery/financeflow-etl-pipeline
```

### **Step 2: Create Virtual Environment (Optional)**
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# OR using conda
conda create -n financeflow python=3.8
conda activate financeflow
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Dependencies:**
```
pandas>=2.0.0
numpy>=1.24.0
python-dateutil>=2.8.0
```

---

## 💻 Usage

### **Option 1: Run the ETL Pipeline**

```python
from app.services.transaction_processing_service import process_transaction_file

# Process the transaction file
result = process_transaction_file('data/raw/budgetwise_finance_dataset.csv')

# View results
print(f"✅ Valid Records: {result['valid_records']}")
print(f"❌ Invalid Records: {result['invalid_records']}")
print(f"📊 Success Rate: {result['success_rate']}%")
```

### **Option 2: Run Test Script**

```bash
python tests/test_transaction_processing.py
```

### **Option 3: Command Line**

```bash
python -c "
from app.services.transaction_processing_service import process_transaction_file
process_transaction_file('data/raw/budgetwise_finance_dataset.csv')
"
```

---

## 📈 Results

### **Processing Summary:**

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

### **Data Transformation Examples:**

#### **Before (Raw CSV):**
```csv
transaction_id,date,amount,category
T4999,31-12-23,Rs.828,Fod
T7403,08/05/2022,₹5070,Educaton
T5282,2023-01-15,999999999,Salary
```

#### **After (Processed):**
```csv
transaction_id,date,amount,category
T4999,2023-12-31,828.0,Food
T7403,2022-08-05,5070.0,Education
# T5282 moved to invalid (amount exceeds limit)
```

### **Invalid Records Tracking:**
```csv
transaction_id,date,amount,category,failure_reasons
T5282,2023-01-15,999999999,Salary,Amount exceeds maximum limit (100M): 999999999.0
T12350,NaN,500,Food,Missing required field: date
T10128,2023-05-10,1000,NaN,Missing required field: category
```

---

## 🎓 Key Learnings

### **1. Data Validation Best Practices**
- Separate validation from cleaning logic
- Validate AFTER cleaning (especially for categories with typos)
- Track failure reasons for debugging

### **2. Python datetime Module**
- `strptime()` - Parse string to datetime object
- `strftime()` - Format datetime object to string
- `%Y` (4-digit year) vs `%y` (2-digit year)

### **3. Regular Expressions (Regex)**
- Pattern matching for currency symbol removal
- Case-insensitive text replacement
- Example: `re.sub(r'[Rs.₹$]', '', amount)`

### **4. Dictionary Mapping for Data Cleaning**
- Efficient lookup for typo correction
- Maps variations to standard values
- Example: `{'fod': 'Food', 'educaton': 'Education'}`

### **5. Pandas Data Processing**
- Efficient CSV reading/writing
- Handling missing data (NaN)
- Row-by-row iteration with `.iterrows()`

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Pandas** | Data manipulation and CSV processing |
| **NumPy** | Numerical operations |
| **datetime** | Date parsing and formatting |
| **re (regex)** | Pattern matching and text cleaning |
| **os** | File system operations |

---

## 🔮 Future Enhancements

- [ ] Add database integration (PostgreSQL/MongoDB)
- [ ] Implement API endpoints using FastAPI/Flask
- [ ] Add machine learning for anomaly detection
- [ ] Create data quality dashboard with Plotly/Dash
- [ ] Add parallel processing for large datasets
- [ ] Implement data versioning
- [ ] Add unit test coverage reporting
- [ ] Create Docker container for deployment
- [ ] Add CI/CD pipeline with GitHub Actions
- [ ] Implement data profiling and statistics

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Contact

**Uday Shankar** - udayshankar2241@gmail.com

**Project Link:** https://github.com/yourusername/data-mastery/financeflow-etl-pipeline

---

## 🙏 Acknowledgments

- Dataset from [Kaggle](https://www.kaggle.com/)
- Inspired by real-world data engineering challenges
- Built as part of the Data Mastery learning journey

---

## 📊 Project Stats

![](https://img.shields.io/badge/Total_Records-15,900-blue)
![](https://img.shields.io/badge/Valid_Records-12,851-green)
![](https://img.shields.io/badge/Success_Rate-80.82%25-success)
![](https://img.shields.io/badge/Processing_Time-<2s-yellow)
![](https://img.shields.io/badge/Test_Coverage-100%25-brightgreen)

---

**⭐ If you found this project helpful, please consider giving it a star!**
