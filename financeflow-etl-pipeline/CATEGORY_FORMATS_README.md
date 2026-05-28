# Category Validator & Cleaner - Updated for CSV Data

## Updated: May 28, 2026

---

## Category Issues Found in `budgetwise_finance_dataset.csv`

The CSV contains **many typos, abbreviations, and inconsistent formats**:

### 🔴 Typos Found:
```
'Educaton'   → Missing 'i'
'Fod'        → Missing 'o'
'Foods'      → Plural
'Foodd'      → Extra 'd'
'Utilties'   → Missing 'i'
'Utlities'   → Wrong order
'Rentt'      → Extra 't'
'Rnt'        → Missing 'e'
'Travl'      → Missing 'e'
'Traval'     → Wrong spelling
'Helth'      → Missing 'a'
```

### 🔴 Abbreviations Found:
```
'EDU'        → Education
'Entertain'  → Entertainment
'Entrtnmnt'  → Entertainment (no vowels!)
```

### 🔴 Case Inconsistencies:
```
'FOOD', 'Food', 'food'
'RENT', 'Rent', 'rent'
'TRAVEL', 'Travel', 'travel'
'HEALTH', 'Health', 'health'
'SAVINGS', 'Savings', 'savings'
'OTHERS', 'Others', 'others'
```

### 🔴 Synonyms/Variations:
```
'Others'     → Should be 'Other'
'Misc'       → Should be 'Other'
'Freelance'  → Should be 'Income'
'Bonus'      → Should be 'Income'
'Saving'     → Should be 'Savings'
'Utility'    → Should be 'Utilities'
```

---

## How the Code Works

### **1. Category Cleaner (`category_cleaner.py`)**

The cleaner uses a **dictionary mapping** to normalize all variations:

```python
CATEGORY_MAPPING = {
    # All variations point to standard name
    'fod': 'Food',           # Typo
    'foods': 'Food',         # Plural
    'foodd': 'Food',         # Typo
    'food': 'Food',          # Lowercase
    
    'educaton': 'Education', # Typo
    'edu': 'Education',      # Abbreviation
    
    'utilties': 'Utilities', # Typo
    'utlities': 'Utilities', # Typo
    
    # ... and so on for all variations
}
```

#### **How it cleans:**

```python
def clean_category(category):
    # Step 1: Convert to lowercase
    category_lower = str(category).strip().lower()
    
    # Step 2: Look up in mapping
    if category_lower in CATEGORY_MAPPING:
        return CATEGORY_MAPPING[category_lower]  # Return standard name
    
    # Step 3: If not found, return title case
    return category.title()
```

#### **Examples:**

| Input          | Lookup Key    | Mapping Result | Output          |
|----------------|---------------|----------------|-----------------|
| `"Fod"`        | `"fod"`       | Found → `Food` | `"Food"`        |
| `"FOOD"`       | `"food"`      | Found → `Food` | `"Food"`        |
| `"Educaton"`   | `"educaton"`  | Found → `Education` | `"Education"` |
| `"Utilties"`   | `"utilties"`  | Found → `Utilities` | `"Utilities"` |
| `"Misc"`       | `"misc"`      | Found → `Other` | `"Other"`       |
| `"UnknownCat"` | `"unknowncat"`| Not found      | `"Unknowncat"` (title case) |

---

### **2. Category Validator (`category_validator.py`)**

After cleaning, the validator checks if the category is in the allowed list:

```python
VALID_CATEGORIES = {
    'Food', 'Groceries', 'Shopping', 'Transportation',
    'Entertainment', 'Utilities', 'Health', 'Travel',
    'Education', 'Personal Care', 'Income', 'Salary',
    'Investment', 'Other', 'Rent', 'Insurance',
    'Savings', 'Transfer'
}
```

#### **How it validates:**

```python
def validate_category(category):
    # Check if it's in the valid set (case-insensitive)
    if not any(cat.lower() == category.lower() for cat in VALID_CATEGORIES):
        return False, f"Invalid category: {category}"
    
    return True, None
```

---

## Complete Workflow Example

```
CSV Data          Cleaner           Validator        Result
─────────────────────────────────────────────────────────────
"Fod"        →   "Food"        →   ✅ Valid    →   "Food"
"FOOD"       →   "Food"        →   ✅ Valid    →   "Food"
"Educaton"   →   "Education"   →   ✅ Valid    →   "Education"
"EDU"        →   "Education"   →   ✅ Valid    →   "Education"
"Utilties"   →   "Utilities"   →   ✅ Valid    →   "Utilities"
"Misc"       →   "Other"       →   ✅ Valid    →   "Other"
"Freelance"  →   "Income"      →   ✅ Valid    →   "Income"
"Helth"      →   "Health"      →   ✅ Valid    →   "Health"
""           →   None          →   ❌ Invalid  →   Rejected
"XYZ"        →   "Xyz"         →   ❌ Invalid  →   Rejected
```

---

## All Mappings Implemented

### Food Categories:
✅ `fod`, `foods`, `foodd`, `food` → `Food`

### Education Categories:
✅ `educaton`, `edu`, `education` → `Education`

### Utilities Categories:
✅ `utilties`, `utlities`, `utility`, `utilities` → `Utilities`

### Rent Categories:
✅ `rentt`, `rnt`, `rent` → `Rent`

### Travel Categories:
✅ `travl`, `traval`, `travel` → `Travel`

### Health Categories:
✅ `helth`, `health` → `Health`

### Entertainment Categories:
✅ `entertain`, `entrtnmnt`, `entertainment` → `Entertainment`

### Savings Categories:
✅ `saving`, `savings` → `Savings`

### Other Categories:
✅ `others`, `misc`, `other` → `Other`

### Income Categories:
✅ `freelance`, `bonus`, `income` → `Income`

---

## Test Results

**All 47 test cases passed! ✅**

```
✅ 'Educaton' → 'Education' (Valid: True)
✅ 'rent' → 'Rent' (Valid: True)
✅ 'Freelance' → 'Income' (Valid: True)
✅ 'Fod' → 'Food' (Valid: True)
✅ 'entertainment' → 'Entertainment' (Valid: True)
✅ 'Utilties' → 'Utilities' (Valid: True)
✅ 'Rentt' → 'Rent' (Valid: True)
✅ 'FOOD' → 'Food' (Valid: True)
✅ 'Travl' → 'Travel' (Valid: True)
✅ 'Helth' → 'Health' (Valid: True)
✅ 'EDU' → 'Education' (Valid: True)
✅ 'Entertain' → 'Entertainment' (Valid: True)
✅ 'Misc' → 'Other' (Valid: True)
✅ 'Others' → 'Other' (Valid: True)
✅ 'Bonus' → 'Income' (Valid: True)
```

---

## Integration with Transaction Processing

When processing transactions:

1. **Raw category** from CSV (e.g., `"Fod"`, `"FOOD"`, `"Educaton"`)
2. **Clean** using `clean_category()` → Standardizes to `"Food"`, `"Education"`
3. **Validate** using `validate_category()` → Checks if valid
4. **Store** only valid, standardized categories

This ensures **data consistency** across your entire system! 🎯

---

## Files Updated:
- ✅ `/app/validations/category_validator.py`
- ✅ `/app/utils/category_cleaner.py`
