# Amount Validator & Cleaner - Updated for CSV Formats

## Updated: May 28, 2026

---

## Amount Formats Found in `budgetwise_finance_dataset.csv`

The CSV contains amounts in various formats:

### 1. **Plain Numbers**
```
3888, 649, 13239, 6299, 2287, etc.
```

### 2. **Rs. Prefix** (Rupees with period)
```
Rs.828, Rs.5554, Rs.864, Rs.5756, Rs.9705
```

### 3. **₹ Symbol** (Indian Rupee symbol)
```
₹5070, ₹2553, ₹4189, ₹41573, ₹999999, ₹32146, ₹6141
```

### 4. **$ Symbol** (Dollar sign)
```
$4262, $7619, $8380
```

### 5. **INR Suffix** (Indian Rupee text)
```
5107 INR, 1380 INR, 4641 INR, 7397 INR
```

### 6. **Large Numbers**
```
999999999, 999999, 855881
```

---

## Updated `amount_validator.py`

### What It Does:

1. **Cleans the input** by removing:
   - `Rs.` or `Rs` prefix
   - Currency symbols: `₹`, `$`, `€`, `£`, `¥`
   - Text: `INR`
   - Commas and spaces

2. **Validates**:
   - ✅ Not null/empty
   - ✅ Numeric after cleaning
   - ✅ Positive (> 0)
   - ✅ Within reasonable range (≤ 100 million)

### Example Processing:

| Input         | Cleaned Value | Valid? | Result    |
|---------------|---------------|--------|-----------|
| `3888`        | `3888.0`      | ✅     | 3888.0    |
| `Rs.828`      | `828.0`       | ✅     | 828.0     |
| `₹5070`       | `5070.0`      | ✅     | 5070.0    |
| `$4262`       | `4262.0`      | ✅     | 4262.0    |
| `5107 INR`    | `5107.0`      | ✅     | 5107.0    |
| `999999999`   | `999999999.0` | ❌     | Exceeds max limit |
| `0`           | `0.0`         | ❌     | Must be positive |
| `-500`        | `-500.0`      | ❌     | Must be positive |
| `''`          | -             | ❌     | Amount is missing |

---

## Updated `amount_cleaner.py`

### What It Does:

1. **Removes** all currency symbols and text
2. **Converts** to float
3. **Rounds** to 2 decimal places
4. **Returns** clean numeric value

### Regex Patterns Used:

```python
# Remove "Rs." or "Rs" (case insensitive)
re.sub(r'Rs\.?', '', amount_str, flags=re.IGNORECASE)

# Remove currency symbols
re.sub(r'[€£¥₹$]', '', amount_str)

# Remove "INR" text (case insensitive)
re.sub(r'INR', '', amount_str, flags=re.IGNORECASE)
```

---

## Test Results

All formats from your CSV now work correctly:

```
✅ '3888'       → Valid: True,  Cleaned: 3888.0
✅ 'Rs.828'     → Valid: True,  Cleaned: 828.0
✅ '₹5070'      → Valid: True,  Cleaned: 5070.0
✅ '$4262'      → Valid: True,  Cleaned: 4262.0
✅ '5107 INR'   → Valid: True,  Cleaned: 5107.0
✅ '₹999999'    → Valid: True,  Cleaned: 999999.0
❌ '999999999'  → Valid: False, Error: Exceeds max limit (100M)
❌ '0'          → Valid: False, Error: Must be positive
❌ ''           → Valid: False, Error: Amount is missing
```

---

## Integration with Transaction Processing

The transaction processing service will now:

1. **Validate** amounts using `validate_amount()` - checks format and range
2. **Clean** amounts using `clean_amount()` - normalizes to standard float
3. **Store** cleaned amounts in standardized format

All currency symbols and text are removed, leaving only the numeric value for consistent processing and storage.

---

## Files Updated:
- ✅ `/app/validations/amount_validator.py`
- ✅ `/app/utils/amount_cleaner.py`
