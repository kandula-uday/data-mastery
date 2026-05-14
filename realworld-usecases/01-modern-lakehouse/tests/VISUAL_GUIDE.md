# 📊 Visual Guide: What We're Testing

## 🎯 Your Silver Transformation - What Gets Tested

```
┌─────────────────────────────────────────────────────────────────┐
│                      BRONZE LAYER (Raw Data)                    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Trip 1: fare=$10, distance=2.5, pickup=10:00            │ │
│  │ Trip 2: fare=$10, distance=2.5, pickup=10:00  ← DUPLICATE│ │
│  │ Trip 3: fare=-$5, distance=1.0, pickup=11:00  ← INVALID  │ │
│  │ Trip 4: fare=$12, distance=0.0, pickup=12:00  ← INVALID  │ │
│  │ Trip 5: fare=$15, distance=3.2, pickup=13:00            │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ transform_to_silver()
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSFORMATION LOGIC                         │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ 1. DEDUPLICATION                                          ││
│  │    ├─ Remove duplicate trips                              ││
│  │    └─ TEST: test_deduplication_removes_exact_duplicates() ││
│  │                                                            ││
│  │ 2. DATA QUALITY FILTERS                                   ││
│  │    ├─ Remove negative fares                               ││
│  │    ├─ Remove zero distance trips                          ││
│  │    ├─ Remove trips < 1 min or > 5 hours                   ││
│  │    └─ TESTS:                                              ││
│  │       • test_negative_fares_are_filtered()                ││
│  │       • test_zero_distance_trips_filtered()               ││
│  │                                                            ││
│  │ 3. CALCULATED FIELDS                                      ││
│  │    ├─ trip_duration_minutes = (dropoff - pickup)          ││
│  │    ├─ tip_percentage = (tip / fare) * 100                 ││
│  │    └─ TEST: test_tip_percentage_calculated_correctly()    ││
│  │                                                            ││
│  │ 4. DATE PARTS                                             ││
│  │    ├─ Extract pickup_year, pickup_month, etc.             ││
│  │    └─ TEST: (covered in schema test)                      ││
│  │                                                            ││
│  │ 5. SCHEMA VALIDATION                                      ││
│  │    └─ TEST: test_silver_has_required_columns()            ││
│  └────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SILVER LAYER (Clean Data)                   │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Trip 1: fare=$10, distance=2.5, tip_pct=20%, duration=15 │ │
│  │ Trip 5: fare=$15, distance=3.2, tip_pct=18%, duration=20 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ✅ Only 2 valid trips (3 filtered out!)                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Test Breakdown: What Each Test Does

### Test 1: Deduplication
```python
test_deduplication_removes_exact_duplicates()
```

**WHAT WE'RE TESTING:**
- Does the deduplication logic work?

**TEST AGAINST:**
- Business Rule: No duplicate trips should exist

**HOW WE TEST:**
```
Input:  3 records (2 are exact duplicates)
        ├─ Record 1: pickup=10:00, distance=2.5, fare=$10
        ├─ Record 2: pickup=10:00, distance=2.5, fare=$10 (DUPLICATE)
        └─ Record 3: pickup=11:00, distance=3.0, fare=$12

Run:    transform_to_silver()

Assert: Output should have 2 records (duplicate removed)
```

**WHY THIS MATTERS:**
- Without this test, you might not notice if deduplication breaks
- You'd end up counting the same trip twice → inflated metrics

---

### Test 2: Negative Fares
```python
test_negative_fares_are_filtered()
```

**WHAT WE'RE TESTING:**
- Are negative fares filtered out?

**TEST AGAINST:**
- Data Quality Rule: fare_amount > 0

**HOW WE TEST:**
```
Input:  2 records
        ├─ Record 1: fare=$12.50 ✅ Valid
        └─ Record 2: fare=-$10.00 ❌ Invalid

Run:    transform_to_silver()

Assert: Output should have 1 record (negative fare removed)
        AND no records with fare_amount < 0
```

**WHY THIS MATTERS:**
- Negative fares are errors/test data
- They skew revenue calculations

---

### Test 3: Tip Percentage Calculation
```python
test_tip_percentage_calculated_correctly()
```

**WHAT WE'RE TESTING:**
- Is the tip_percentage formula correct?

**TEST AGAINST:**
- Mathematical Formula: (tip_amount / fare_amount) × 100

**HOW WE TEST:**
```
Input:  2 records with KNOWN values
        ├─ Record 1: fare=$10, tip=$2 → Should be 20%
        └─ Record 2: fare=$20, tip=$5 → Should be 25%

Run:    transform_to_silver()

Assert: Record 1 tip_percentage == 20.0
        Record 2 tip_percentage == 25.0
```

**WHY THIS MATTERS:**
- Tip percentage is a business metric
- If calculation is wrong, dashboards show incorrect data

---

### Test 4: Schema Validation
```python
test_silver_has_required_columns()
```

**WHAT WE'RE TESTING:**
- Does Silver table have all expected columns?

**TEST AGAINST:**
- Schema Specification (list of required columns)

**HOW WE TEST:**
```
Input:  Any valid record

Run:    transform_to_silver()

Assert: Output has these columns:
        ├─ pickup_datetime ✓
        ├─ dropoff_datetime ✓
        ├─ pickup_date ✓
        ├─ pickup_year ✓
        ├─ pickup_month ✓
        ├─ pickup_day ✓
        ├─ pickup_hour ✓
        ├─ passenger_count ✓
        ├─ trip_distance ✓
        ├─ trip_duration_minutes ✓
        ├─ fare_amount ✓
        ├─ tip_amount ✓
        ├─ total_amount ✓
        ├─ tip_percentage ✓
        ├─ payment_type ✓
        ├─ ingested_at ✓
        └─ source_file ✓
```

**WHY THIS MATTERS:**
- Gold layer depends on these columns
- If a column is missing, downstream queries break

---

### Test 5: Zero Distance Filtering
```python
test_zero_distance_trips_filtered()
```

**WHAT WE'RE TESTING:**
- Are zero-distance trips removed?

**TEST AGAINST:**
- Data Quality Rule: trip_distance > 0

**HOW WE TEST:**
```
Input:  2 records
        ├─ Record 1: distance=2.5 ✅ Valid
        └─ Record 2: distance=0.0 ❌ Invalid

Run:    transform_to_silver()

Assert: Output should have 1 record (zero distance removed)
        AND no records with trip_distance <= 0
```

**WHY THIS MATTERS:**
- Zero-distance trips are likely errors
- They skew average distance metrics

---

## 🎓 Understanding "Testing Against"

### What Does "Test Against" Mean?

When we test, we compare **actual result** with **expected result**.

The **expected result** comes from:

| Source                | Example                                    |
|-----------------------|--------------------------------------------|
| **Business Rules**    | "Fares must be positive"                   |
| **Mathematical Formula** | tip_percentage = (tip / fare) × 100     |
| **Schema Spec**       | "Silver must have 17 columns"              |
| **Requirements Doc**  | "Duplicates must be removed"               |
| **Known Values**      | fare=$10, tip=$2 → expect 20% tip          |

### Example: Testing Tip Percentage

```python
# Known Input (we control this)
fare = 10.00
tip = 2.00

# Expected Output (we calculate by hand)
expected_tip_percentage = (2.00 / 10.00) * 100  # = 20.0

# Run the function (actual result)
actual_result = calculate_tip_percentage(fare, tip)

# Test Against: Compare actual vs expected
assert actual_result == expected_tip_percentage
#      ↑ What the code produced
#                       ↑ What we expect based on math
```

---

## 📖 Real-World Example

### Scenario: Dashboard Shows Wrong Tip Average

**Without Tests:**
```
Dashboard: "Average tip: 250%"  ← Obviously wrong!

You: "Hmm, let me check the code..."
     *spends 2 hours debugging*
     "Oh, I forgot to divide before multiplying by 100!"
```

**With Tests:**
```
Running tests...

❌ FAILED: test_tip_percentage_calculated_correctly
   AssertionError: Expected 20.0 but got 200.0

You: "Ah, my formula is wrong! Let me fix it."
     *fixes in 5 minutes*
     
✅ ALL TESTS PASSED!
```

**Tests save time by catching bugs BEFORE deployment!**

---

## 🚀 Next Steps

1. **Read the tutorial:** `tests/TESTING_TUTORIAL.md`
2. **Study the simple example:** `tests/test_simple_example.py`
3. **Look at the real tests:** `tests/test_silver_transformations.py`
4. **Run the simple example:** `python tests/test_simple_example.py`
5. **Try running real tests:** `pytest tests/ -v` (after we fix the imports)

---

## 💡 Key Takeaways

✅ **Tests verify your code works as expected**
✅ **We test against: business rules, formulas, schemas, requirements**
✅ **Pattern: Arrange → Act → Assert**
✅ **Each test should be independent and focused**
✅ **Tests catch bugs early → save debugging time**

---

## 🎯 Summary Table

| Test                            | What It Tests                  | Tests Against             |
|---------------------------------|--------------------------------|---------------------------|
| `test_deduplication_...`        | Duplicates removed             | Business rule             |
| `test_negative_fares_...`       | Invalid fares filtered         | Data quality rule         |
| `test_tip_percentage_...`       | Calculation accuracy           | Math formula              |
| `test_silver_has_required_...`  | Schema structure               | Schema specification      |
| `test_zero_distance_...`        | Invalid distances filtered     | Data quality rule         |

Each test ensures a **specific piece of logic** works correctly! 🎉
