"""
Unit Tests for Silver Layer Transformation
Tests the transform_to_silver() function from 02_silver_transformation.py

Run with: pytest tests/test_silver_transformations.py -v
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, 
    IntegerType, DoubleType, TimestampType
)
from datetime import datetime
import sys
import os

# Add notebooks directory to path
notebooks_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    'notebooks'
)
sys.path.insert(0, notebooks_path)

# Import the actual transformation function from your production code
# This imports from notebooks/02_silver_transformation.py
import importlib.util
spec = importlib.util.spec_from_file_location(
    "silver_transformation",
    os.path.join(notebooks_path, "02_silver_transformation.py")
)
silver_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(silver_module)
transform_to_silver = silver_module.transform_to_silver


# ============================================================================
# FIXTURE: Create Spark Session for Tests
# ============================================================================

@pytest.fixture(scope="session")
def spark():
    """
    Create a Spark session for testing.
    This runs ONCE for all tests (scope="session")
    """
    spark_session = (SparkSession.builder
        .appName("PyTest_Silver_Transformation")
        .master("local[2]")  # Run locally with 2 cores
        .config("spark.sql.shuffle.partitions", "2")  # Small for testing
        .getOrCreate())
    
    yield spark_session  # Provide to tests
    
    spark_session.stop()  # Clean up after all tests


# ============================================================================
# TEST 1: Deduplication Logic
# ============================================================================

def test_deduplication_removes_exact_duplicates(spark):
    """
    Test that exact duplicate records are removed.
    
    WHAT WE'RE TESTING: Deduplication logic in transform_to_silver()
    WHY: Ensure duplicate trips aren't counted twice
    HOW: Create data with duplicates, run transformation, count result
    """
    # ARRANGE: Create test data with duplicates
    # Schema matches your Bronze table columns
    schema = StructType([
        StructField("tpep_pickup_datetime", StringType(), True),
        StructField("tpep_dropoff_datetime", StringType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("RatecodeID", IntegerType(), True),
        StructField("Fare_Amt", DoubleType(), True),
        StructField("Tip_Amt", DoubleType(), True),
        StructField("Total_Amt", DoubleType(), True),
        StructField("payment_type", StringType(), True),
        StructField("ingested_at", TimestampType(), True),
        StructField("source_file", StringType(), True),
    ])
    
    test_data = [
        # Record 1: Original
        ("2023-01-15 10:00:00", "2023-01-15 10:15:00", 
         1, 2.5, 161, 237, 1,
         12.50, 2.00, 15.50, "Credit", datetime.now(), "test.csv"),
        
        # Record 2: EXACT DUPLICATE of Record 1
        ("2023-01-15 10:00:00", "2023-01-15 10:15:00",
         1, 2.5, 161, 237, 1,
         12.50, 2.00, 15.50, "Credit", datetime.now(), "test.csv"),
        
        # Record 3: Different trip
        ("2023-01-15 11:00:00", "2023-01-15 11:20:00",
         2, 3.2, 43, 142, 1,
         15.00, 3.00, 19.00, "Cash", datetime.now(), "test.csv"),
    ]
    
    bronze_df = spark.createDataFrame(test_data, schema)
    
    print("\n📊 Test Data:")
    print(f"   Bronze records (with duplicates): {bronze_df.count()}")
    
    # ACT: Run the transformation
    silver_df = transform_to_silver(bronze_df)
    
    print(f"   Silver records (after deduplication): {silver_df.count()}")
    
    # ASSERT: Check that duplicates were removed
    assert bronze_df.count() == 3, "Should have 3 bronze records (including duplicate)"
    assert silver_df.count() == 2, "Should have 2 silver records (duplicate removed)"
    
    print("   ✅ Deduplication working correctly!")


# ============================================================================
# TEST 2: Negative Fares Filtered
# ============================================================================

def test_negative_fares_are_filtered(spark):
    """
    Test that records with negative fares are removed.
    
    WHAT WE'RE TESTING: Data quality filter (fare_amount > 0)
    WHY: Negative fares are invalid/test data
    HOW: Create data with negative fare, verify it's filtered out
    """
    # ARRANGE: Create test data with negative fare
    schema = StructType([
        StructField("tpep_pickup_datetime", StringType(), True),
        StructField("tpep_dropoff_datetime", StringType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("RatecodeID", IntegerType(), True),
        StructField("Fare_Amt", DoubleType(), True),
        StructField("Tip_Amt", DoubleType(), True),
        StructField("Total_Amt", DoubleType(), True),
        StructField("payment_type", StringType(), True),
        StructField("ingested_at", TimestampType(), True),
        StructField("source_file", StringType(), True),
    ])
    
    test_data = [
        # Valid record
        ("2023-01-15 10:00:00", "2023-01-15 10:15:00",
         1, 2.5, 161, 237, 1,
         12.50, 2.00, 15.50, "Credit", datetime.now(), "test.csv"),
        
        # INVALID: Negative fare
        ("2023-01-15 11:00:00", "2023-01-15 11:20:00",
         1, 3.0, 43, 142, 1,
         -10.00, 0.00, -10.00, "Credit", datetime.now(), "test.csv"),
    ]
    
    bronze_df = spark.createDataFrame(test_data, schema)
    
    print("\n🚫 Test Data with Invalid Fare:")
    print(f"   Bronze records: {bronze_df.count()}")
    
    # ACT: Run transformation
    silver_df = transform_to_silver(bronze_df)
    
    print(f"   Silver records (after filtering): {silver_df.count()}")
    
    # ASSERT: Negative fare should be filtered out
    assert silver_df.count() == 1, "Should have 1 valid record (negative fare removed)"
    assert silver_df.filter("fare_amount < 0").count() == 0, "Should have NO negative fares"
    
    print("   ✅ Negative fare filtering working correctly!")


# ============================================================================
# TEST 3: Tip Percentage Calculation
# ============================================================================

def test_tip_percentage_calculated_correctly(spark):
    """
    Test that tip_percentage is calculated accurately.
    
    WHAT WE'RE TESTING: Calculation logic (tip / fare * 100)
    WHY: Ensure business metrics are accurate
    HOW: Create known values, verify calculation
    """
    # ARRANGE: Create test data with known tip percentages
    schema = StructType([
        StructField("tpep_pickup_datetime", StringType(), True),
        StructField("tpep_dropoff_datetime", StringType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("RatecodeID", IntegerType(), True),
        StructField("Fare_Amt", DoubleType(), True),
        StructField("Tip_Amt", DoubleType(), True),
        StructField("Total_Amt", DoubleType(), True),
        StructField("payment_type", StringType(), True),
        StructField("ingested_at", TimestampType(), True),
        StructField("source_file", StringType(), True),
    ])
    
    test_data = [
        # Fare: $10, Tip: $2 → Should be 20%
        ("2023-01-15 10:00:00", "2023-01-15 10:15:00",
         1, 2.5, 161, 237, 1,
         10.00, 2.00, 13.00, "Credit", datetime.now(), "test.csv"),
        
        # Fare: $20, Tip: $5 → Should be 25%
        ("2023-01-15 11:00:00", "2023-01-15 11:20:00",
         1, 3.0, 43, 142, 1,
         20.00, 5.00, 26.00, "Credit", datetime.now(), "test.csv"),
    ]
    
    bronze_df = spark.createDataFrame(test_data, schema)
    
    print("\n💯 Test Tip Percentage Calculation:")
    
    # ACT: Run transformation
    silver_df = transform_to_silver(bronze_df)
    
    # ASSERT: Check calculations
    results = silver_df.select("fare_amount", "tip_amount", "tip_percentage").collect()
    
    # First record: 2/10 * 100 = 20%
    assert results[0]["tip_percentage"] == 20.0, "First record should have 20% tip"
    print(f"   ✅ Record 1: ${results[0]['fare_amount']:.2f} fare, ${results[0]['tip_amount']:.2f} tip = {results[0]['tip_percentage']:.2f}%")
    
    # Second record: 5/20 * 100 = 25%
    assert results[1]["tip_percentage"] == 25.0, "Second record should have 25% tip"
    print(f"   ✅ Record 2: ${results[1]['fare_amount']:.2f} fare, ${results[1]['tip_amount']:.2f} tip = {results[1]['tip_percentage']:.2f}%")


# ============================================================================
# TEST 4: Schema Validation
# ============================================================================

def test_silver_has_required_columns(spark):
    """
    Test that Silver layer has all expected columns.
    
    WHAT WE'RE TESTING: Output schema structure
    WHY: Ensure downstream consumers get expected data
    HOW: Check column names and types
    """
    # ARRANGE: Create minimal valid data
    schema = StructType([
        StructField("tpep_pickup_datetime", StringType(), True),
        StructField("tpep_dropoff_datetime", StringType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("RatecodeID", IntegerType(), True),
        StructField("Fare_Amt", DoubleType(), True),
        StructField("Tip_Amt", DoubleType(), True),
        StructField("Total_Amt", DoubleType(), True),
        StructField("payment_type", StringType(), True),
        StructField("ingested_at", TimestampType(), True),
        StructField("source_file", StringType(), True),
    ])
    
    test_data = [
        ("2023-01-15 10:00:00", "2023-01-15 10:15:00",
         1, 2.5, 161, 237, 1,
         12.50, 2.00, 15.50, "Credit", datetime.now(), "test.csv"),
    ]
    
    bronze_df = spark.createDataFrame(test_data, schema)
    
    # ACT: Run transformation
    silver_df = transform_to_silver(bronze_df)
    
    # ASSERT: Check required columns exist
    expected_columns = [
        "pickup_datetime",
        "dropoff_datetime",
        "pickup_date",
        "pickup_year",
        "pickup_month",
        "pickup_day",
        "pickup_hour",
        "passenger_count",
        "trip_distance",
        "trip_duration_minutes",
        "fare_amount",
        "tip_amount",
        "total_amount",
        "tip_percentage",
        "payment_type",
        "ingested_at",
        "source_file"
    ]
    
    actual_columns = silver_df.columns
    
    print("\n📋 Schema Validation:")
    print(f"   Expected {len(expected_columns)} columns")
    print(f"   Found {len(actual_columns)} columns")
    
    for col in expected_columns:
        assert col in actual_columns, f"Missing column: {col}"
        print(f"   ✅ {col}")
    
    print("   ✅ Schema is correct!")


# ============================================================================
# TEST 5: Zero Distance Filtering
# ============================================================================

def test_zero_distance_trips_filtered(spark):
    """
    Test that trips with zero distance are removed.
    
    WHAT WE'RE TESTING: Data quality filter (trip_distance > 0)
    WHY: Zero distance trips are likely errors
    HOW: Create data with zero distance, verify filtering
    """
    # ARRANGE
    schema = StructType([
        StructField("tpep_pickup_datetime", StringType(), True),
        StructField("tpep_dropoff_datetime", StringType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("RatecodeID", IntegerType(), True),
        StructField("Fare_Amt", DoubleType(), True),
        StructField("Tip_Amt", DoubleType(), True),
        StructField("Total_Amt", DoubleType(), True),
        StructField("payment_type", StringType(), True),
        StructField("ingested_at", TimestampType(), True),
        StructField("source_file", StringType(), True),
    ])
    
    test_data = [
        # Valid trip
        ("2023-01-15 10:00:00", "2023-01-15 10:15:00",
         1, 2.5, 161, 237, 1,
         12.50, 2.00, 15.50, "Credit", datetime.now(), "test.csv"),
        
        # INVALID: Zero distance
        ("2023-01-15 11:00:00", "2023-01-15 11:05:00",
         1, 0.0, 161, 161, 1,
         5.00, 0.00, 5.00, "Cash", datetime.now(), "test.csv"),
    ]
    
    bronze_df = spark.createDataFrame(test_data, schema)
    
    # ACT
    silver_df = transform_to_silver(bronze_df)
    
    # ASSERT
    assert silver_df.count() == 1, "Should have 1 valid record (zero distance removed)"
    assert silver_df.filter("trip_distance <= 0").count() == 0, "No zero distance trips"
    
    print("\n🚫 Zero Distance Filtering:")
    print("   ✅ Zero distance trips filtered correctly!")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    """
    Run all tests manually (without pytest command).
    Useful for debugging individual tests.
    """
    print("=" * 70)
    print("🧪 RUNNING SILVER TRANSFORMATION TESTS")
    print("=" * 70)
    
    # Create Spark session
    spark = (SparkSession.builder
        .appName("Manual_Test_Run")
        .master("local[2]")
        .getOrCreate())
    
    try:
        # Run each test
        test_deduplication_removes_exact_duplicates(spark)
        test_negative_fares_are_filtered(spark)
        test_tip_percentage_calculated_correctly(spark)
        test_silver_has_required_columns(spark)
        test_zero_distance_trips_filtered(spark)
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        spark.stop()
