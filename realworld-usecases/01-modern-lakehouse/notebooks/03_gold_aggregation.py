"""
Gold Layer: Business Aggregations
Creates business-ready aggregate tables for analytics.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg, min as spark_min, max as spark_max,
    round as spark_round, desc
)
from delta.tables import DeltaTable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_daily_summary(silver_df):
    """Aggregate daily trip metrics."""
    logger.info("Creating daily summary table")
    
    daily_summary = (silver_df
        .groupBy("pickup_date")
        .agg(
            count("*").alias("total_trips"),
            spark_sum("fare_amount").alias("total_revenue"),
            spark_sum("tip_amount").alias("total_tips"),
            spark_sum("total_amount").alias("total_amount"),
            avg("fare_amount").alias("avg_fare"),
            avg("trip_distance").alias("avg_distance"),
            avg("trip_duration_minutes").alias("avg_duration"),
            avg("tip_percentage").alias("avg_tip_pct"),
            spark_max("total_amount").alias("max_fare")
        )
        .withColumn("avg_fare", spark_round(col("avg_fare"), 2))
        .withColumn("avg_distance", spark_round(col("avg_distance"), 2))
        .withColumn("avg_duration", spark_round(col("avg_duration"), 2))
        .withColumn("avg_tip_pct", spark_round(col("avg_tip_pct"), 2))
        .orderBy("pickup_date")
    )
    
    return daily_summary


def create_hourly_patterns(silver_df):
    """Analyze trip patterns by hour."""
    logger.info("Creating hourly patterns table")
    
    hourly_patterns = (silver_df
        .groupBy("pickup_hour", "pickup_location_id")
        .agg(
            count("*").alias("trip_count"),
            avg("fare_amount").alias("avg_fare"),
            avg("trip_duration_minutes").alias("avg_duration")
        )
        .withColumn("avg_fare", spark_round(col("avg_fare"), 2))
        .withColumn("avg_duration", spark_round(col("avg_duration"), 2))
        .orderBy("pickup_hour", desc("trip_count"))
    )
    
    return hourly_patterns


def create_top_routes(silver_df):
    """Identify most popular routes."""
    logger.info("Creating top routes table")
    
    top_routes = (silver_df
        .groupBy("pickup_location_id", "dropoff_location_id")
        .agg(
            count("*").alias("trip_count"),
            avg("fare_amount").alias("avg_fare"),
            avg("trip_distance").alias("avg_distance"),
            avg("trip_duration_minutes").alias("avg_duration")
        )
        .withColumn("avg_fare", spark_round(col("avg_fare"), 2))
        .withColumn("avg_distance", spark_round(col("avg_distance"), 2))
        .withColumn("avg_duration", spark_round(col("avg_duration"), 2))
        .orderBy(desc("trip_count"))
        .limit(100)
    )
    
    return top_routes


def create_revenue_metrics(silver_df):
    """Calculate revenue-focused metrics."""
    logger.info("Creating revenue metrics table")
    
    revenue_metrics = (silver_df
        .groupBy("pickup_date", "payment_type")
        .agg(
            count("*").alias("trip_count"),
            spark_sum("fare_amount").alias("fare_revenue"),
            spark_sum("tip_amount").alias("tip_revenue"),
            spark_sum("total_amount").alias("total_revenue"),
            avg("tip_percentage").alias("avg_tip_pct")
        )
        .withColumn("fare_revenue", spark_round(col("fare_revenue"), 2))
        .withColumn("tip_revenue", spark_round(col("tip_revenue"), 2))
        .withColumn("total_revenue", spark_round(col("total_revenue"), 2))
        .withColumn("avg_tip_pct", spark_round(col("avg_tip_pct"), 2))
        .orderBy("pickup_date", "payment_type")
    )
    
    return revenue_metrics


def write_gold_table(df, table_name):
    """Write Gold table to Delta as managed table."""
    (df.write
     .format("delta")
     .mode("overwrite")
     .option("overwriteSchema", "true")
     .saveAsTable(table_name))
    
    logger.info(f"Gold table '{table_name}' written: {df.count():,} records")


def main():
    """
    Main function for standalone execution.
    Note: In Databricks notebooks, use spark.table() directly!
    """
    # Initialize Spark (only needed for local/standalone execution)
    spark = (SparkSession.builder
             .appName("Gold_Aggregation")
             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
             .getOrCreate())
    
    # Read Silver managed table
    silver_df = spark.table("silver_trips")
    logger.info(f"Silver records loaded: {silver_df.count():,}")
    
    # Create Gold aggregates
    daily_summary = create_daily_summary(silver_df)
    hourly_patterns = create_hourly_patterns(silver_df)
    top_routes = create_top_routes(silver_df)
    revenue_metrics = create_revenue_metrics(silver_df)
    
    # Write Gold tables (managed tables)
    write_gold_table(daily_summary, "gold_daily_summary")
    write_gold_table(hourly_patterns, "gold_hourly_patterns")
    write_gold_table(top_routes, "gold_top_routes")
    write_gold_table(revenue_metrics, "gold_revenue_metrics")
    
    # Display samples
    print("\n=== Daily Summary Sample ===")
    daily_summary.show(5, truncate=False)
    
    print("\n=== Top Routes Sample ===")
    top_routes.show(5, truncate=False)
    
    # Overall statistics
    print("\n=== Gold Layer Statistics ===")
    print(f"Total days: {daily_summary.count()}")
    print(f"Total hourly patterns: {hourly_patterns.count()}")
    print(f"Top routes tracked: {top_routes.count()}")
    
    spark.stop()


if __name__ == "__main__":
    main()


# ============================================================================
# FOR DATABRICKS NOTEBOOKS: Use this simplified version instead
# ============================================================================
# COMMAND ----------
# Read Silver table
# silver = spark.table("silver_trips")
# print(f"✅ Silver records loaded: {silver.count():,}")

# COMMAND ----------
# Create Gold aggregates
# daily_summary = create_daily_summary(silver)
# hourly_patterns = create_hourly_patterns(silver)
# top_routes = create_top_routes(silver)
# revenue_metrics = create_revenue_metrics(silver)

# COMMAND ----------
# Write Gold tables
# write_gold_table(daily_summary, "gold_daily_summary")
# write_gold_table(hourly_patterns, "gold_hourly_patterns")
# write_gold_table(top_routes, "gold_top_routes")
# write_gold_table(revenue_metrics, "gold_revenue_metrics")

# COMMAND ----------
# Preview results
# print("=== Daily Summary Sample ===")
# display(daily_summary.limit(10))
# 
# print("\n=== Top Routes Sample ===")
# display(top_routes.limit(10))
# 
# print(f"\n✅ Gold layer complete!")
# print(f"   - gold_daily_summary: {daily_summary.count():,} records")
# print(f"   - gold_hourly_patterns: {hourly_patterns.count():,} records")
# print(f"   - gold_top_routes: {top_routes.count():,} records")
# print(f"   - gold_revenue_metrics: {revenue_metrics.count():,} records")
