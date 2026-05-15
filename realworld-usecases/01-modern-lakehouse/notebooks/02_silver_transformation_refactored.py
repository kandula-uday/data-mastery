"""
Silver Layer Transformation - REFACTORED FOR TESTING
====================================================

This version extracts transformation logic into functions
so they can be imported and tested!

Key Changes:
1. Extract transformation logic into transform_to_silver() function
2. Main execution code is separate
3. Functions can be imported by tests
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, 
    lit,
    unix_timestamp,
    when,
    year,
    month,
    dayofmonth,
    hour,
    to_date
)
from datetime import datetime


# ============================================================================
# TRANSFORMATION FUNCTIONS (Testable!)
# ============================================================================

def transform_to_silver(bronze_df: DataFrame) -> DataFrame:
    """
    Transform Bronze data to Silver layer.
    
    This function contains ALL transformation logic.
    It can be tested independently!
    
    Steps:
    1. Deduplication
    2. Data quality filters
    3. Calculate derived fields
    4. Extract date parts
    
    Args:
        bronze_df: Bronze layer DataFrame
        
    Returns:
        Silver layer DataFrame
    """
    
    # Step 1: Rename columns to lowercase/snake_case (if needed)
    silver_df = bronze_df.select(
        col("Trip_Pickup_DateTime").alias("pickup_datetime"),
        col("Trip_Dropoff_DateTime").alias("dropoff_datetime"),
        col("Passenger_Count").alias("passenger_count"),
        col("Trip_Distance").alias("trip_distance"),
        col("Start_Lat").alias("start_lat"),
        col("Start_Lon").alias("start_lon"),
        col("End_Lat").alias("end_lat"),
        col("End_Lon").alias("end_lon"),
        col("Fare_Amt").alias("fare_amount"),
        col("Tip_Amt").alias("tip_amount"),
        col("Total_Amt").alias("total_amount"),
        col("Payment_Type").alias("payment_type"),
        col("ingested_at"),
        col("source_file")
    )
    
    # Step 2: Deduplication
    # Remove exact duplicates based on business key
    dedup_columns = [
        "pickup_datetime",
        "dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "start_lat",
        "start_lon",
        "end_lat",
        "end_lon"
    ]
    silver_df = silver_df.dropDuplicates(dedup_columns)
    
    # Step 3: Calculate derived fields
    silver_df = silver_df.withColumn(
        "trip_duration_minutes",
        (unix_timestamp("dropoff_datetime") - unix_timestamp("pickup_datetime")) / 60
    )
    
    silver_df = silver_df.withColumn(
        "tip_percentage",
        when(col("fare_amount") > 0, 
             (col("tip_amount") / col("fare_amount")) * 100
        ).otherwise(0)
    )
    
    # Step 4: Extract date parts
    silver_df = (silver_df
        .withColumn("pickup_date", to_date("pickup_datetime"))
        .withColumn("pickup_year", year("pickup_datetime"))
        .withColumn("pickup_month", month("pickup_datetime"))
        .withColumn("pickup_day", dayofmonth("pickup_datetime"))
        .withColumn("pickup_hour", hour("pickup_datetime"))
    )
    
    # Step 5: Data quality filters
    silver_df = (silver_df
        .filter(col("fare_amount") > 0)              # Positive fares only
        .filter(col("trip_distance") > 0)            # Positive distance only
        .filter(col("trip_duration_minutes") >= 1)   # At least 1 minute
        .filter(col("trip_duration_minutes") <= 300) # Max 5 hours
    )
    
    return silver_df


def validate_silver_data(silver_df: DataFrame) -> dict:
    """
    Run validation checks on Silver data.
    Returns a dictionary with validation results.
    
    This function can also be tested!
    """
    validation_results = {
        "total_records": silver_df.count(),
        "negative_fares": silver_df.filter(col("fare_amount") < 0).count(),
        "zero_distance": silver_df.filter(col("trip_distance") <= 0).count(),
        "null_pickups": silver_df.filter(col("pickup_datetime").isNull()).count(),
        "invalid_durations": silver_df.filter(
            (col("trip_duration_minutes") < 1) | 
            (col("trip_duration_minutes") > 300)
        ).count()
    }
    
    return validation_results


# ============================================================================
# MAIN EXECUTION (Runs in Databricks)
# ============================================================================

def main():
    """
    Main execution function for Databricks.
    This runs when the notebook is executed.
    """
    
    # Get Spark session (available in Databricks)
    spark = SparkSession.builder.getOrCreate()
    
    print("=" * 70)
    print("SILVER LAYER TRANSFORMATION")
    print("=" * 70)
    
    # Read Bronze data
    print("\n1. Reading Bronze data...")
    bronze_df = spark.read.table("bronze_raw_trips")
    bronze_count = bronze_df.count()
    print(f"   Bronze records: {bronze_count:,}")
    
    # Transform to Silver
    print("\n2. Transforming to Silver layer...")
    silver_df = transform_to_silver(bronze_df)
    silver_count = silver_df.count()
    print(f"   Silver records: {silver_count:,}")
    print(f"   Filtered out: {bronze_count - silver_count:,} records")
    
    # Validate Silver data
    print("\n3. Validating Silver data...")
    validation = validate_silver_data(silver_df)
    for check, count in validation.items():
        status = "✅" if count == 0 or check == "total_records" else "❌"
        print(f"   {status} {check}: {count:,}")
    
    # Write to Silver table
    print("\n4. Writing to Silver table...")
    (silver_df
        .write
        .mode("overwrite")
        .format("delta")
        .saveAsTable("silver_trips")
    )
    print("   ✅ Silver table created!")
    
    # Show sample
    print("\n5. Sample Silver records:")
    silver_df.select(
        "pickup_datetime",
        "fare_amount",
        "trip_distance",
        "trip_duration_minutes",
        "tip_percentage"
    ).show(5, truncate=False)
    
    print("\n" + "=" * 70)
    print("✅ SILVER TRANSFORMATION COMPLETE!")
    print("=" * 70)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # This runs when executed as a script
    main()
```
