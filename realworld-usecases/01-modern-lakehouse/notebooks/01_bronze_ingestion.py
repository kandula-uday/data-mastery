"""
Bronze Layer: Raw Data Ingestion
Ingests NYC Taxi data from source and writes to Bronze Delta tables.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, lit
from delta.tables import DeltaTable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_bronze_table(spark, source_path, target_path, partition_col="pickup_date"):
    """
    Ingest raw data into Bronze layer with metadata.
    
    Args:
        spark: SparkSession
        source_path: Path to source data (CSV/Parquet)
        target_path: Delta table path in DBFS
        partition_col: Column to partition by
    """
    logger.info(f"Starting Bronze ingestion from {source_path}")
    
    # Read raw data
    df = (spark.read
          .format("parquet")  # Change to "csv" if using CSV files
          .option("header", "true")
          .option("inferSchema", "true")
          .load(source_path))
    
    # Add metadata columns
    df_with_metadata = (df
        .withColumn("ingested_at", current_timestamp())
        .withColumn("source_file", input_file_name())
        .withColumn("ingestion_batch", lit("batch_001"))
    )
    
    # Write to Delta table
    (df_with_metadata.write
     .format("delta")
     .mode("append")
     .partitionBy(partition_col)
     .option("mergeSchema", "true")
     .save(target_path))
    
    logger.info(f"Bronze ingestion complete. Records written: {df_with_metadata.count()}")
    
    return df_with_metadata


def main():
    # Initialize Spark with Delta Lake
    spark = (SparkSession.builder
             .appName("Bronze_Ingestion")
             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
             .getOrCreate())
    
    # Paths (update these for your environment)
    SOURCE_PATH = "dbfs:/FileStore/lakehouse/raw/yellow_tripdata_2023-*.parquet"
    BRONZE_PATH = "dbfs:/FileStore/lakehouse/bronze/raw_trips"
    
    # Ingest data
    bronze_df = create_bronze_table(
        spark=spark,
        source_path=SOURCE_PATH,
        target_path=BRONZE_PATH,
        partition_col="tpep_pickup_datetime"
    )
    
    # Display sample
    bronze_df.show(5)
    
    # Table statistics
    print(f"\n=== Bronze Table Statistics ===")
    print(f"Total records: {bronze_df.count():,}")
    print(f"Columns: {len(bronze_df.columns)}")
    bronze_df.printSchema()
    
    spark.stop()


if __name__ == "__main__":
    main()
