# 🧪 Testing Tutorial for Data Engineers

## 📚 What is Testing?

**Testing** is writing code that verifies your main code works correctly. Think of it like a quality inspector checking products on an assembly line.

---

## 🎯 Why Do We Test Data Pipelines?

### Without Tests:
❌ "Did my deduplication work? Let me manually check..."  
❌ "Hmm, is this tip percentage right? I'll calculate it by hand..."  
❌ "Did I break something? I need to re-run the entire pipeline..."  

### With Tests:
✅ Run `pytest` → Get instant feedback  
✅ Confidence that code works before deploying  
✅ Catch bugs early (saves hours of debugging)  
✅ Document how your code should behave  

---

## 🔍 What Are We Testing?

### In Your Silver Transformation:

| **Logic**                     | **What We Test**                                  | **Why**                                    |
|-------------------------------|---------------------------------------------------|--------------------------------------------|
| **Deduplication**             | Duplicate records are removed                     | Don't count same trip twice                |
| **Fare Filtering**            | Negative fares are excluded                       | Invalid data should be cleaned             |
| **Distance Filtering**        | Zero-distance trips are excluded                  | Likely errors/test data                    |
| **Duration Filtering**        | Trips < 1 min or > 5 hours are excluded           | Unrealistic trips                          |
| **Tip Calculation**           | tip_percentage = (tip / fare) * 100               | Accuracy for business metrics              |
| **Duration Calculation**      | trip_duration_minutes = (dropoff - pickup)        | Correct time calculations                  |
| **Date Parts**                | pickup_year, pickup_month extracted correctly     | For date-based aggregations                |
| **Schema**                    | All expected columns exist with correct types     | Downstream systems depend on schema        |

---

## 🧩 Testing Pattern: Arrange-Act-Assert

Every test follows this 3-step pattern:

```python
def test_something():
    # 1. ARRANGE: Set up test data (GIVEN)
    test_data = [
        (datetime(2023, 1, 15, 10, 0), 10.00, 2.00),  # Valid record
        (datetime(2023, 1, 15, 11, 0), -5.00, 0.00),  # Invalid: negative fare
    ]
    
    # 2. ACT: Run the transformation (WHEN)
    result = transform_to_silver(test_data)
    
    # 3. ASSERT: Check the result (THEN)
    assert result.count() == 1  # Only valid record remains
```

### Real Example from Your Code:

```python
def test_negative_fares_are_filtered(spark):
    # ===== ARRANGE =====
    # Create 2 records: 1 valid, 1 with negative fare
    test_data = [
        # Valid: fare = $12.50
        (datetime(...), 12.50, 2.00, ...),
        
        # Invalid: fare = -$10.00 (should be removed)
        (datetime(...), -10.00, 0.00, ...),
    ]
    bronze_df = spark.createDataFrame(test_data, schema)
    
    # ===== ACT =====
    # Run your Silver transformation
    silver_df = transform_to_silver(bronze_df)
    
    # ===== ASSERT =====
    # Check: Should have 1 record (negative fare filtered out)
    assert silver_df.count() == 1
    # Check: Should have NO negative fares
    assert silver_df.filter("fare_amount < 0").count() == 0
```

---

## 📊 Types of Tests

### **1. Unit Tests** (What we're doing)
Test **individual functions** in isolation

```python
# Test ONE specific thing: deduplication
def test_deduplication():
    # Given: 3 records (2 are duplicates)
    # When: Run transform_to_silver()
    # Then: Should have 2 unique records
```

**Characteristics:**
- Fast (runs in milliseconds)
- Isolated (doesn't touch real databases)
- Focused (tests one thing)

### **2. Integration Tests** (Future)
Test **full pipeline** end-to-end

```python
# Test Bronze → Silver → Gold entire flow
def test_full_pipeline():
    # Given: Raw CSV file
    # When: Run all transformations
    # Then: Gold tables should exist with correct aggregates
```

### **3. Data Quality Tests** (Future)
Test **business rules** on actual data

```python
# Test production data quality
def test_production_silver_has_no_nulls_in_key_fields():
    df = spark.read.table("silver_trips")
    assert df.filter("pickup_datetime IS NULL").count() == 0
```

---

## 🔬 What Are We Testing Against?

### 1. **Expected Behavior (Logic)**
```python
# WHAT: Deduplication should remove duplicates
# TEST AGAINST: Known input → Expected output

# Given: 3 records (1 duplicate)
input_count = 3

# When: Run deduplication
result = transform_to_silver(data)

# Then: Should have 2 unique records
assert result.count() == 2  # Testing against expected count
```

### 2. **Business Rules (Requirements)**
```python
# WHAT: Fares must be positive
# TEST AGAINST: Business requirement document

# Then: No fares should be <= 0
assert silver_df.filter("fare_amount <= 0").count() == 0
```

### 3. **Schema (Structure)**
```python
# WHAT: Silver must have specific columns
# TEST AGAINST: Schema specification

expected_columns = ["pickup_datetime", "fare_amount", "tip_percentage", ...]
actual_columns = silver_df.columns

for col in expected_columns:
    assert col in actual_columns  # Testing against schema spec
```

### 4. **Calculations (Math)**
```python
# WHAT: Tip percentage calculation
# TEST AGAINST: Known mathematical formula (tip/fare * 100)

# Given: fare=$10, tip=$2
# When: Calculate tip_percentage
# Then: Should be 20.0
assert result["tip_percentage"] == 20.0  # Testing against expected calculation
```

---

## 🎓 Understanding Fixtures

### What is a Fixture?

A **fixture** is a setup function that runs **before** your tests to prepare resources.

```python
@pytest.fixture(scope="session")
def spark():
    """This runs ONCE before all tests"""
    spark_session = SparkSession.builder.master("local[2]").getOrCreate()
    yield spark_session  # Provide to tests
    spark_session.stop()  # Clean up after all tests
```

**Without Fixture (Repetitive):**
```python
def test_1():
    spark = SparkSession.builder...  # Create Spark
    # ... test logic ...
    spark.stop()  # Clean up

def test_2():
    spark = SparkSession.builder...  # Create Spark AGAIN
    # ... test logic ...
    spark.stop()  # Clean up AGAIN
```

**With Fixture (Efficient):**
```python
def test_1(spark):  # Spark provided automatically
    # ... test logic ...

def test_2(spark):  # Same Spark session reused
    # ... test logic ...
```

### Fixture Scopes:

| Scope       | When It Runs                          | Use Case                           |
|-------------|---------------------------------------|------------------------------------|
| `function`  | Once per test (default)               | Test needs fresh data each time    |
| `session`   | Once for all tests                    | Expensive setup (Spark session)    |
| `module`    | Once per file                         | Shared setup for one test file     |

---

## 🚀 Running Tests

### Option 1: Run with pytest (Recommended)
```bash
cd /Users/udayshankar/Documents/ML\ Projects/data-mastery/realworld-usecases/01-modern-lakehouse

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_silver_transformations.py -v

# Run specific test function
pytest tests/test_silver_transformations.py::test_negative_fares_are_filtered -v
```

### Option 2: Run as Python script (For debugging)
```bash
python tests/test_silver_transformations.py
```

---

## 📖 Reading Test Output

### Success Output:
```
tests/test_silver_transformations.py::test_deduplication_removes_exact_duplicates PASSED
tests/test_silver_transformations.py::test_negative_fares_are_filtered PASSED
tests/test_silver_transformations.py::test_tip_percentage_calculated_correctly PASSED
tests/test_silver_transformations.py::test_silver_has_required_columns PASSED
tests/test_silver_transformations.py::test_zero_distance_trips_filtered PASSED

======================= 5 passed in 12.34s =======================
```

### Failure Output:
```
tests/test_silver_transformations.py::test_negative_fares_are_filtered FAILED

============================= FAILURES =============================
_________________________ test_negative_fares_are_filtered _________________________

    def test_negative_fares_are_filtered(spark):
        ...
>       assert silver_df.count() == 1, "Should have 1 valid record"
E       AssertionError: Should have 1 valid record
E       assert 2 == 1

tests/test_silver_transformations.py:155: AssertionError
```

This means: The filter didn't work! Negative fares weren't removed!

---

## 🎯 Key Testing Concepts

### 1. **Isolation**
Each test should be **independent** and not rely on other tests.

❌ **Bad:** test_2 depends on test_1's output
```python
def test_1():
    global data
    data = transform_to_silver(bronze)

def test_2():
    # Uses data from test_1 - BAD!
    assert data.count() > 0
```

✅ **Good:** Each test creates its own data
```python
def test_1():
    data = create_test_data()
    result = transform_to_silver(data)
    assert result.count() == 2

def test_2():
    data = create_test_data()  # Independent data
    result = transform_to_silver(data)
    assert "tip_percentage" in result.columns
```

### 2. **Small Scope**
Test **one thing** per test function.

❌ **Bad:** Testing multiple things
```python
def test_everything():
    assert deduplication_works()
    assert negative_fares_filtered()
    assert tip_percentage_correct()
    # If one fails, you don't know which!
```

✅ **Good:** Separate tests
```python
def test_deduplication():
    assert duplicates_removed()

def test_negative_fares():
    assert invalid_fares_filtered()

def test_tip_calculation():
    assert tip_percentage_correct()
```

### 3. **Known Values**
Use **predictable inputs** with **known outputs**.

```python
# Given: Known input
fare = 10.00
tip = 2.00

# When: Calculate
result = calculate_tip_percentage(fare, tip)

# Then: Known output (2/10 * 100 = 20.0)
assert result == 20.0
```

---

## 💡 What You're Testing in YOUR Pipeline

### Silver Transformation (`test_silver_transformations.py`):

```python
# Test 1: Deduplication Logic
# WHAT: Do duplicates get removed?
# AGAINST: Business rule (no duplicate trips)
test_deduplication_removes_exact_duplicates()

# Test 2: Data Quality (Negative Fares)
# WHAT: Are negative fares filtered?
# AGAINST: Requirement (fare_amount > 0)
test_negative_fares_are_filtered()

# Test 3: Calculation Accuracy
# WHAT: Is tip_percentage calculated correctly?
# AGAINST: Math formula (tip / fare * 100)
test_tip_percentage_calculated_correctly()

# Test 4: Schema Validation
# WHAT: Does output have required columns?
# AGAINST: Schema specification
test_silver_has_required_columns()

# Test 5: Data Quality (Zero Distance)
# WHAT: Are zero-distance trips filtered?
# AGAINST: Requirement (trip_distance > 0)
test_zero_distance_trips_filtered()
```

---

## 🔧 Next Steps

1. **Read the test file:** `tests/test_silver_transformations.py`
2. **Run the tests:** `pytest tests/ -v`
3. **Fix any failures:** Adjust your transformation logic
4. **Add more tests:** Trip duration bounds, NULL handling, etc.
5. **Document coverage:** What percentage of code is tested?

---

## ✅ Quick Summary

| **Concept**           | **What It Means**                                      |
|-----------------------|--------------------------------------------------------|
| **Unit Test**         | Test one function in isolation                         |
| **Arrange-Act-Assert**| Setup data → Run function → Check result               |
| **Fixture**           | Setup code that runs before tests                      |
| **Assertion**         | Check if result matches expectation (`assert x == y`)  |
| **Test Against**      | Expected behavior, business rules, schema, math        |
| **Isolation**         | Each test is independent                               |

---

Happy Testing! 🎉

Remember: **Good tests = Confidence to deploy!**
