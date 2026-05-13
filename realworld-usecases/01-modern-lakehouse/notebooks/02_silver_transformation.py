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
        .withColumn("fare_amount", spark_round(col("fare_amount"), 2))
        .withColumn("tip_amount", spark_round(col("tip_amount"), 2))
        .withColumn("total_amount", spark_round(col("total_amount"), 2))
        
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
            "pickup_location_id",
            "dropoff_location_id",
            "passenger_count",
            "trip_distance",
            "trip_duration_minutes",
            "rate_code_id",
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
    # Initialize Spark
    spark = (SparkSession.builder
             .appName("Silver_Transformation")
             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
             .getOrCreate())
    
    # Paths
    BRONZE_PATH = "dbfs:/FileStore/lakehouse/bronze/raw_trips"
    SILVER_PATH = "dbfs:/FileStore/lakehouse/silver/trips"
    
    # Read Bronze table
    bronze_df = spark.read.format("delta").load(BRONZE_PATH)
    logger.info(f"Bronze records read: {bronze_df.count():,}")
    
    # Transform to Silver
    silver_df = transform_to_silver(bronze_df)
    
    # Data quality summary
    print("\n=== Silver Layer Quality Summary ===")
    print(f"Total clean records: {silver_df.count():,}")
    print(f"Date range: {silver_df.agg({'pickup_date': 'min'}).collect()[0][0]} to {silver_df.agg({'pickup_date': 'max'}).collect()[0][0]}")
    print(f"Avg fare: ${silver_df.agg({'fare_amount': 'avg'}).collect()[0][0]:.2f}")
    print(f"Avg trip distance: {silver_df.agg({'trip_distance': 'avg'}).collect()[0][0]:.2f} miles")
    
    # Write to Silver
    write_silver_table(spark, silver_df, SILVER_PATH)
    
    # Display sample
    silver_df.show(5, truncate=False)
    
    spark.stop()


if __name__ == "__main__":
    main()
