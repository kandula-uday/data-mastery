from pyspark.sql.functions import current_timestamp, input_file_name, lit, col, to_date
from delta.tables import DeltaTable

print("✅ Libraries imported successfully!")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 1: Load Sample Data
# MAGIC 
# MAGIC We'll use Databricks' built-in sample taxi data

# COMMAND ----------
# Read sample NYC taxi data (built into Databricks)
# This is similar to real NYC Taxi data but smaller for learning
raw_df = (spark.read
    .format("csv")
    .option("header", "true")  # First row is column names
    .option("inferSchema", "true")  # Auto-detect data types
    .option("compression", "gzip")  # Handle .gz compression
    .load("dbfs:/databricks-datasets/nyctaxi/tripdata/yellow/yellow_tripdata_2009-01.csv.gz"))

print(f"✅ Loaded {raw_df.count():,} records")
raw_df.printSchema()
display(raw_df.limit(10))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 2: Add Metadata Columns
# MAGIC 
# MAGIC Bronze layer should track:
# MAGIC - When data was ingested
# MAGIC - Source file information
# MAGIC - Batch ID for tracking

# COMMAND ----------
# Add metadata columns
bronze_df = (raw_df
    .withColumn("ingested_at", current_timestamp())
    .withColumn("source_file", lit("dbfs:/databricks-datasets/nyctaxi/tripdata/yellow/yellow_tripdata_2009-01.csv.gz"))
    .withColumn("ingestion_batch", lit("batch_001"))
    .withColumn("pickup_date", to_date(col("Trip_Pickup_DateTime")))  # For partitioning
)

print("✅ Metadata columns added:")
print("   - ingested_at: Current timestamp")
print("   - source_file: Source data path")
print("   - ingestion_batch: Batch identifier")
print("   - pickup_date: Partition key")

display(bronze_df.select("Trip_Pickup_DateTime", "pickup_date", "ingested_at", "source_file").limit(5))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 3: Write to Bronze Delta Table
# MAGIC 
# MAGIC Delta Lake provides:
# MAGIC - ACID transactions
# MAGIC - Time travel
# MAGIC - Schema evolution

# COMMAND ----------
# Define Bronze table path
#BRONZE_PATH = "/FileStore/lakehouse/bronze/raw_trips"

# Write to Delta table with partitioning
(bronze_df.write
    .format("delta")
    .mode("overwrite")  # Use "append" for incremental loads
    .partitionBy("pickup_date")
    .option("overwriteSchema", "true")
    .saveAsTable("bronze_raw_trips"))


print(f"   Records written: {bronze_df.count():,}")
print(f"   Partitioned by: pickup_date")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 4: Verify Bronze Table

# COMMAND ----------
# Read back the Bronze table to verify


bronze_table = spark.read.table("bronze_raw_trips")
display(bronze_table.limit(10))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 5: Query Bronze Table



# Query using SQL
query_result = spark.sql("""
    SELECT 
        pickup_date,
        COUNT(*) as trip_count,
        AVG(trip_distance) as avg_distance,
        AVG(Fare_Amt) as avg_fare
    FROM bronze_raw_trips
    GROUP BY pickup_date
    ORDER BY pickup_date
""")

display(query_result)

# COMMAND ----------
# MAGIC %md
# MAGIC ## ✅ Success!
# MAGIC 
# MAGIC You've created your first Bronze layer table with:
# MAGIC - Raw taxi trip data
# MAGIC - Metadata tracking
# MAGIC - Delta Lake format
# MAGIC - Date-based partitioning
# MAGIC 
# MAGIC **Next Step:** Move to `02_silver_transformation.py` to clean and transform this data!

# COMMAND ----------
print("🎉 Bronze Layer Ingestion Complete!")
print(f"\n📊 Summary:")
print(f"   Source: Databricks sample dataset")
print(f"   Records: {bronze_table.count():,}")
print(f"   Format: Delta Lake")
print(f"\n🚀 Ready for Silver layer transformation!")
