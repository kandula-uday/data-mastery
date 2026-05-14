# 🎯 Testing Workflow Cheat Sheet

## 🚀 Quick Start: Run Your First Test

```bash
# 1. Navigate to project
cd /Users/udayshankar/Documents/ML\ Projects/data-mastery/realworld-usecases/01-modern-lakehouse

# 2. Run the simple example (no dependencies needed)
python tests/test_simple_example.py

# 3. Run all tests with pytest
pytest tests/ -v

# 4. Run specific test file
pytest tests/test_silver_transformations.py -v

# 5. Run one specific test
pytest tests/test_silver_transformations.py::test_negative_fares_are_filtered -v
```

---

## 📚 Files You Should Read (In Order)

### 1. **Start Here:** Simple Example
```
tests/test_simple_example.py
```
- ✅ No Spark/PySpark needed
- ✅ Simple Python functions
- ✅ Learn testing basics
- ✅ Run immediately: `python tests/test_simple_example.py`

**What You'll Learn:**
- Arrange-Act-Assert pattern
- How assertions work
- What "testing against" means
- Edge case testing

---

### 2. **Theory:** Testing Tutorial
```
tests/TESTING_TUTORIAL.md
```
- 📖 Comprehensive testing guide
- 📖 Explains all concepts
- 📖 Examples and patterns
- 📖 FAQ section

**Topics Covered:**
- Why we test data pipelines
- Types of tests (unit, integration, data quality)
- Testing pattern (AAA)
- Fixtures explained
- Running tests

---

### 3. **Visual:** Visual Guide
```
tests/VISUAL_GUIDE.md
```
- 🎨 Diagrams showing data flow
- 🎨 What each test does
- 🎨 Why each test matters
- 🎨 Real-world examples

**Best For:**
- Visual learners
- Understanding the big picture
- Seeing data transformations

---

### 4. **Real Tests:** Silver Transformations
```
tests/test_silver_transformations.py
```
- 🔬 Actual tests for your pipeline
- 🔬 Uses PySpark
- 🔬 Tests Bronze → Silver logic
- 🔬 Production-ready examples

**What It Tests:**
- Deduplication logic
- Data quality filters
- Calculation accuracy
- Schema validation

---

## 🧪 Test Execution Workflow

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Write Code                                     │
│  ├─ notebooks/02_silver_transformation.py               │
│  └─ Function: transform_to_silver(bronze_df)            │
└─────────────────────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 2: Write Tests                                    │
│  ├─ tests/test_silver_transformations.py                │
│  └─ Function: test_deduplication_removes_duplicates()   │
└─────────────────────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 3: Run Tests                                      │
│  └─ Command: pytest tests/ -v                           │
└─────────────────────────────────────────────────────────┘
                         ▼
                    ┌─────────┐
                    │ SUCCESS?│
                    └────┬────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   ┌──────────────┐             ┌──────────────┐
   │  ✅ PASSED   │             │  ❌ FAILED   │
   └──────────────┘             └──────────────┘
          │                             │
          ▼                             ▼
   ┌──────────────┐             ┌──────────────┐
   │ Deploy with  │             │ Fix the bug  │
   │ confidence!  │             │ in your code │
   └──────────────┘             └──────────────┘
                                        │
                                        ▼
                                 Run tests again
```

---

## 🎓 Understanding pytest Output

### Example: All Tests Pass

```bash
$ pytest tests/test_silver_transformations.py -v

tests/test_silver_transformations.py::test_deduplication_removes_exact_duplicates PASSED [ 20%]
tests/test_silver_transformations.py::test_negative_fares_are_filtered PASSED [ 40%]
tests/test_silver_transformations.py::test_tip_percentage_calculated_correctly PASSED [ 60%]
tests/test_silver_transformations.py::test_silver_has_required_columns PASSED [ 80%]
tests/test_silver_transformations.py::test_zero_distance_trips_filtered PASSED [100%]

========================= 5 passed in 12.45s ==========================
```

**What This Means:**
- ✅ All 5 tests ran successfully
- ✅ Your transformation logic is correct
- ✅ Safe to deploy!

---

### Example: A Test Fails

```bash
$ pytest tests/test_silver_transformations.py -v

tests/test_silver_transformations.py::test_deduplication_removes_exact_duplicates PASSED [ 20%]
tests/test_silver_transformations.py::test_negative_fares_are_filtered FAILED [ 40%]
tests/test_silver_transformations.py::test_tip_percentage_calculated_correctly PASSED [ 60%]
tests/test_silver_transformations.py::test_silver_has_required_columns PASSED [ 80%]
tests/test_silver_transformations.py::test_zero_distance_trips_filtered PASSED [100%]

============================== FAILURES ===============================
_____________ test_negative_fares_are_filtered _____________

    def test_negative_fares_are_filtered(spark):
        ...
        # ASSERT: Negative fare should be filtered out
>       assert silver_df.count() == 1, "Should have 1 valid record"
E       AssertionError: Should have 1 valid record
E       assert 2 == 1
E        +  where 2 = <bound method DataFrame.count of DataFrame[...]>()
E        +    where <bound method DataFrame.count of DataFrame[...]> = DataFrame[...].count

tests/test_silver_transformations.py:155: AssertionError
===================== 1 failed, 4 passed in 13.89s ====================
```

**What This Means:**
- ❌ Test expected 1 record but got 2
- ❌ The negative fare was NOT filtered
- ❌ Bug in the filtering logic!

**How to Fix:**
1. Open `notebooks/02_silver_transformation.py`
2. Check the filter condition: `.filter(col("fare_amount") > 0)`
3. Fix the bug
4. Run tests again: `pytest tests/ -v`

---

## 💡 Common Testing Scenarios

### Scenario 1: Adding New Logic

```
You add:    trip_duration_hours = trip_duration_minutes / 60
```

**Testing Steps:**
1. Write a test first (Test-Driven Development)
   ```python
   def test_trip_duration_hours():
       # Given: trip_duration_minutes = 120
       # When: Calculate trip_duration_hours
       # Then: Should be 2.0
       assert result["trip_duration_hours"] == 2.0
   ```

2. Run test (it should FAIL - logic not implemented yet)
   ```bash
   pytest tests/ -v
   # ❌ FAILED: KeyError: 'trip_duration_hours'
   ```

3. Add the logic to your transformation
   ```python
   .withColumn("trip_duration_hours", col("trip_duration_minutes") / 60)
   ```

4. Run test again (should PASS now)
   ```bash
   pytest tests/ -v
   # ✅ PASSED: test_trip_duration_hours
   ```

---

### Scenario 2: Refactoring Code

```
You want to:  Clean up your transformation logic
Risk:         Breaking existing functionality
```

**Testing Steps:**
1. Run tests BEFORE refactoring
   ```bash
   pytest tests/ -v
   # ✅ 5 passed - baseline established
   ```

2. Refactor your code

3. Run tests AFTER refactoring
   ```bash
   pytest tests/ -v
   # ✅ 5 passed - refactoring didn't break anything!
   ```

**Tests act as a safety net!**

---

### Scenario 3: Debugging a Production Issue

```
Dashboard reports: "Average fare is $0.00"
```

**Testing Steps:**
1. Write a test to reproduce the issue
   ```python
   def test_average_fare_not_zero():
       result = transform_to_silver(sample_data)
       avg_fare = result.select(avg("fare_amount")).collect()[0][0]
       assert avg_fare > 0, f"Average fare is {avg_fare} (should be > 0)"
   ```

2. Run test
   ```bash
   pytest tests/ -v
   # ❌ FAILED: Average fare is 0.0 (should be > 0)
   ```

3. Debug and fix

4. Run test again
   ```bash
   pytest tests/ -v
   # ✅ PASSED: test_average_fare_not_zero
   ```

---

## 🔧 Useful pytest Commands

```bash
# Run all tests
pytest tests/ -v

# Run tests in a specific file
pytest tests/test_silver_transformations.py -v

# Run a specific test function
pytest tests/test_silver_transformations.py::test_negative_fares_are_filtered -v

# Run tests matching a pattern
pytest tests/ -k "fare" -v  # Runs all tests with "fare" in the name

# Stop at first failure
pytest tests/ -x

# Show print statements
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l

# Run tests in parallel (faster)
pytest tests/ -n auto

# Generate coverage report
pytest tests/ --cov=notebooks --cov-report=html
```

---

## 📊 Testing Best Practices

### ✅ DO:

1. **Write small, focused tests**
   ```python
   # Good: Tests one thing
   def test_deduplication():
       assert duplicates_removed()
   
   # Bad: Tests multiple things
   def test_everything():
       assert duplicates_removed()
       assert fares_positive()
       assert schema_correct()
   ```

2. **Use descriptive test names**
   ```python
   # Good
   def test_negative_fares_are_filtered():
       ...
   
   # Bad
   def test_fares():
       ...
   ```

3. **Keep tests independent**
   ```python
   # Good: Each test creates own data
   def test_1():
       data = create_test_data()
       ...
   
   def test_2():
       data = create_test_data()
       ...
   ```

4. **Test edge cases**
   ```python
   def test_zero_fare():
       ...
   
   def test_null_values():
       ...
   
   def test_very_large_numbers():
       ...
   ```

---

### ❌ DON'T:

1. **Don't test external APIs in unit tests**
   ```python
   # Bad: Unit test shouldn't call Databricks
   def test_read_from_databricks():
       df = spark.read.table("bronze_raw_trips")  # External dependency
       ...
   ```

2. **Don't make tests depend on each other**
   ```python
   # Bad: test_2 depends on test_1
   test_1_result = None
   
   def test_1():
       global test_1_result
       test_1_result = transform()
   
   def test_2():
       assert test_1_result.count() > 0
   ```

3. **Don't write tests without assertions**
   ```python
   # Bad: No assertion - test passes even if logic is wrong
   def test_transformation():
       result = transform_to_silver(data)
       print(result.count())  # Just printing, not asserting!
   ```

---

## 🎯 Your Testing Journey

### Phase 1: Learn Basics ✅ (You Are Here!)
- [x] Understand what testing is
- [x] Learn Arrange-Act-Assert pattern
- [x] Run simple example
- [x] Read testing tutorial

### Phase 2: Run Existing Tests
- [ ] Study `test_silver_transformations.py`
- [ ] Fix import issues (if any)
- [ ] Run tests: `pytest tests/ -v`
- [ ] Understand each test

### Phase 3: Write Your Own Tests
- [ ] Test Gold layer aggregations
- [ ] Test edge cases (NULL values, empty data)
- [ ] Test data quality on production data

### Phase 4: Automate Testing
- [ ] Set up GitHub Actions CI/CD
- [ ] Run tests on every commit
- [ ] Add test coverage reports

---

## 📖 Quick Reference

| Task                          | Command                                    |
|-------------------------------|--------------------------------------------|
| Run simple example            | `python tests/test_simple_example.py`      |
| Run all tests                 | `pytest tests/ -v`                         |
| Run specific test file        | `pytest tests/test_silver_transformations.py -v` |
| Run one test                  | `pytest tests/test_file.py::test_name -v` |
| Stop at first failure         | `pytest tests/ -x`                         |
| Show print statements         | `pytest tests/ -v -s`                      |
| Run tests matching pattern    | `pytest tests/ -k "pattern" -v`            |

---

## 🎓 Key Takeaways

✅ **Tests = Quality Assurance**  
✅ **Pattern: Arrange → Act → Assert**  
✅ **Each test should be focused and independent**  
✅ **Tests catch bugs before production**  
✅ **Good tests = Documentation of expected behavior**

---

Happy Testing! 🚀

Remember: **"Code without tests is broken by design."** - Jacob Kaplan-Moss
