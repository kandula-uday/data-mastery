"""
Silver Layer: Data Cleaning and Transformation
Transforms Bronze data into cleaned, validated Silver layer.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_timestamp, unix_timestamp, 
    date_format, year, month, dayofmonth, hour,
    round as spark_round, when
)
from delta.tables import DeltaTable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def transform_to_silver(bronze_df):
    """
    Clean and transform Bronze data to Silver layer.
    
    Business rules:
    - Remove duplicates
    - Filter invalid records (negative fares, zero distance)
    - Standardize datetime formats
    - Calculate derived fields
    - Handle nulls appropriately
    """
    logger.info("Starting Silver transformation")
    
    silver_df = (bronze_df
        # Remove duplicates
        .dropDuplicates(["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID"])
        
        # Parse datetime columns
        .withColumn("pickup_datetime", to_timestamp(col("tpep_pickup_datetime")))
        .withColumn("dropoff_datetime", to_timestamp(col("tpep_dropoff_datetime")))
        
        # Extract date parts
        .withColumn("pickup_date", date_format(col("pickup_datetime"), "yyyy-MM-dd"))
        .withColumn("pickup_year", year(col("pickup_datetime")))
        .withColumn("pickup_month", month(col("pickup_datetime")))
        .withColumn("pickup_day", dayofmonth(col("pickup_datetime")))
        .withColumn("pickup_hour", hour(col("pickup_datetime")))
        
        # Calculate trip duration in minutes
        .withColumn("trip_duration_minutes", 
                   spark_round(
                       (unix_timestamp("dropoff_datetime") - unix_timestamp("pickup_datetime")) / 60,
                       2
                   ))
        
        # Clean amounts (round to 2 decimals)
        .withColumn("fare_amount", spark_round(col("Fare_Amt"), 2))
        .withColumn("tip_amount", spark_round(col("Tip_Amt"), 2))
        .withColumn("total_amount", spark_round(col("Total_Amt"), 2))
        
        # Calculate tip percentage
        .withColumn("tip_percentage",
                   when(col("fare_amount") > 0,
                        spark_round((col("tip_amount") / col("fare_amount")) * 100, 2))
                   .otherwise(0))
        
        # Business rules: Filter invalid records
        .filter(col("fare_amount") > 0)
        .filter(col("trip_distance") > 0)
        .filter(col("trip_duration_minutes").between(1, 300))  # 1 min to 5 hours
        .filter(col("total_amount") > 0)
        .filter(col("pickup_datetime").isNotNull())
        .filter(col("dropoff_datetime").isNotNull())
        
        # Rename columns for clarity
        .withColumnRenamed("PULocationID", "pickup_location_id")
        .withColumnRenamed("DOLocationID", "dropoff_location_id")
        .withColumnRenamed("RatecodeID", "rate_code_id")
        
        # Select final columns
        .select(
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
        )
    )
    
    logger.info(f"Silver transformation complete. Records: {silver_df.count():,}")
    return silver_df


def write_silver_table(spark, silver_df, target_path):
    """Write Silver DataFrame to Delta table."""
    
    (silver_df.write
     .format("delta")
     .mode("overwrite")  # Change to "append" for incremental
     .partitionBy("pickup_date")
     .option("overwriteSchema", "true")
     .save(target_path))
    
    logger.info(f"Silver table written to {target_path}")


def main():
    """
    Main function for standalone execution.
    Note: In Databricks notebooks, you don't need this - use spark.table() directly!
    """
    # Initialize Spark (only needed for local/standalone execution)
    spark = (SparkSession.builder
             .appName("Silver_Transformation")
             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
             .getOrCreate())
    
    # Read Bronze managed table
    bronze = spark.table("bronze_raw_trips")
    logger.info(f"Bronze records read: {bronze.count():,}")
    
    # Transform to Silver
    silver = transform_to_silver(bronze)
    
    # Data quality summary
    print("\n=== Silver Layer Quality Summary ===")
    print(f"Total clean records: {silver.count():,}")
    print(f"Date range: {silver.agg({'pickup_date': 'min'}).collect()[0][0]} to {silver.agg({'pickup_date': 'max'}).collect()[0][0]}")
    print(f"Avg fare: ${silver.agg({'fare_amount': 'avg'}).collect()[0][0]:.2f}")
    print(f"Avg trip distance: {silver.agg({'trip_distance': 'avg'}).collect()[0][0]:.2f} miles")
    
    # Write to Silver managed table
    silver.write.format("delta").mode("overwrite").saveAsTable("silver_trips")
    logger.info("Silver table created: silver_trips")
    
    # Display sample
    silver.show(5, truncate=False)
    
    spark.stop()


if __name__ == "__main__":
    main()


# ============================================================================
# FOR DATABRICKS NOTEBOOKS: Use this simplified version instead
# ============================================================================
# COMMAND ----------
# Read Bronze table
# bronze = spark.table("bronze_raw_trips")
# print(f"✅ Bronze records read: {bronze.count():,}")

# COMMAND ----------
# Transform to Silver
# silver = transform_to_silver(bronze)

# COMMAND ----------
# Data quality summary
# print("\n=== Silver Layer Quality Summary ===")
# print(f"Total clean records: {silver.count():,}")
# display(silver.limit(5))

# COMMAND ----------
# Write to Silver table
# silver.write.format("delta").mode("overwrite").saveAsTable("silver_trips")
# print("✅ Silver table created: silver_trips")
