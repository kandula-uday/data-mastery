# 🔄 Code Refactoring for Testing: Before vs After

## 🎯 **The Problem You Identified**

> "The functions we have declared in tests are not used in the development script, right?"

**YOU'RE ABSOLUTELY CORRECT!** ✅

This is a common issue when starting with testing. Let me show you the problem and solution:

---

## ❌ **BEFORE: Notebook-Style Code (Not Testable)**

### **Your Current `02_silver_transformation.py`:**

```python
# ❌ Problem: All code is inline, no functions!

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, year, month, ...

# Get Spark session
spark = SparkSession.builder.getOrCreate()

# Read Bronze data
bronze_df = spark.read.table("bronze_raw_trips")

# Transformation logic is inline (NOT in a function)
silver_df = bronze_df.select(
    col("Trip_Pickup_DateTime").alias("pickup_datetime"),
    col("Trip_Dropoff_DateTime").alias("dropoff_datetime"),
    # ... more columns ...
)

# Deduplication
silver_df = silver_df.dropDuplicates([...])

# Calculated fields
silver_df = silver_df.withColumn("trip_duration_minutes", ...)
silver_df = silver_df.withColumn("tip_percentage", ...)

# Filters
silver_df = silver_df.filter(col("fare_amount") > 0)

# Write to table
silver_df.write.mode("overwrite").saveAsTable("silver_trips")
```

### **Your Test Trying to Import:**

```python
# ❌ This FAILS because there's no function to import!
from notebooks.silver_transformation_02 import transform_to_silver

def test_deduplication():
    result = transform_to_silver(bronze_df)  # Function doesn't exist!
    assert result.count() == 2
```

**Error:** `ImportError: cannot import name 'transform_to_silver'`

---

## ✅ **AFTER: Refactored Code (Testable)**

### **New `02_silver_transformation_refactored.py`:**

```python
# ✅ Solution: Extract logic into functions!

def transform_to_silver(bronze_df: DataFrame) -> DataFrame:
    """
    Transform Bronze data to Silver layer.
    
    This function is PURE LOGIC - no I/O!
    Takes a DataFrame, transforms it, returns a DataFrame.
    Perfect for testing!
    """
    
    # All transformation logic here
    silver_df = bronze_df.select(...)
    silver_df = silver_df.dropDuplicates([...])
    silver_df = silver_df.withColumn("tip_percentage", ...)
    silver_df = silver_df.filter(col("fare_amount") > 0)
    
    return silver_df


def main():
    """Main execution function for Databricks."""
    spark = SparkSession.builder.getOrCreate()
    
    # Read Bronze data (I/O operation)
    bronze_df = spark.read.table("bronze_raw_trips")
    
    # Transform using our function (logic operation)
    silver_df = transform_to_silver(bronze_df)
    
    # Write to Silver table (I/O operation)
    silver_df.write.mode("overwrite").saveAsTable("silver_trips")


if __name__ == "__main__":
    main()
```

### **Your Test Can Now Import and Use It:**

```python
# ✅ This WORKS! Function exists and can be imported!
from notebooks.silver_transformation_02_refactored import transform_to_silver

def test_deduplication():
    # Create test DataFrame
    test_df = spark.createDataFrame(test_data, schema)
    
    # Call the ACTUAL transformation function from production code!
    result = transform_to_silver(test_df)
    
    # Verify the result
    assert result.count() == 2  # ✅ Works!
```

---

## 💡 **The Connection Between Code and Tests**

```
┌────────────────────────────────────────────────────┐
│  PRODUCTION CODE                                   │
│  (notebooks/02_silver_transformation.py)           │
│                                                    │
│  def transform_to_silver(bronze_df):               │
│      """Transform Bronze to Silver"""              │
│      silver_df = bronze_df.filter(...)             │
│      return silver_df                              │
│                                                    │
│  def main():                                       │
│      bronze = spark.read.table("bronze")           │
│      silver = transform_to_silver(bronze) ◄────┐   │
│      silver.write.saveAsTable("silver")         │   │
└─────────────────────────────────────────────────┼───┘
                                                  │
          Tests import and call this function ────┘
                                                  │
┌─────────────────────────────────────────────────┼───┐
│  TEST CODE                                      │   │
│  (tests/test_silver_transformations.py)         │   │
│                                                 │   │
│  from notebooks.silver_transformation import ◄──┘   │
│      transform_to_silver                            │
│                                                     │
│  def test_negative_fares():                         │
│      test_df = create_test_data()                   │
│      result = transform_to_silver(test_df) ◄────────│
│      # Calling THE SAME function from production!   │
│      assert result.filter("fare < 0").count() == 0  │
└─────────────────────────────────────────────────────┘
```

**This is the connection you were asking about!** ✅

---

## 🎓 **Key Concept: Separation of Concerns**

### **Two Types of Code:**

```python
# TYPE 1: I/O Operations (Reading/Writing)
# - Hard to test (needs Databricks/database)
# - Keep in main() function

bronze_df = spark.read.table("bronze")     # I/O
silver_df.write.saveAsTable("silver")      # I/O


# TYPE 2: Transformation Logic (Pure functions)
# - Easy to test (DataFrame in, DataFrame out)
# - Extract into functions

def transform_to_silver(df):
    # Pure logic - no reading/writing!
    return df.filter(...).withColumn(...)
```

---

## ✅ **Summary: Your Question Answered**

### **Your Question:**
> "The functions we have declared in tests are not used in the development script, right?"

### **Answer:**

**YES, you're correct - that WAS the problem!** Here's the solution:

1. **Problem:** Notebook has inline code (no functions to import)
2. **Solution:** Refactor to extract logic into functions
3. **Result:** Tests can import and test those functions
4. **Benefit:** Same function runs in tests AND production!

```
Notebook (inline code) ─────❌ Can't import────── Tests fail

Notebook (with functions) ──✅ Can import────── Tests work!
                              ↓
                      Same function used in both!
```

---

## 🚀 **What You Need to Do**

I've created `02_silver_transformation_refactored.py` showing the proper structure.

**Next steps:**
1. Look at the refactored version
2. Compare with your current notebook structure
3. Apply the same pattern to your code
4. Update tests to import from the refactored version
5. Run tests and verify they work!

The key insight: **Tests and production code share the same functions!** 🎯
