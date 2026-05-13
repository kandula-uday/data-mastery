"""
Test Silver transformation logic locally with sample data
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, lit
from datetime import datetime

# Initialize Spark locally
spark = (SparkSession.builder
    .appName("Test_Silver_Local")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .master("local[*]")
    .getOrCreate())

print("✅ Local Spark session created")

# Create sample test data (mimicking Bronze layer structure)
sample_data = [
    ("2023-01-15 14:30:00", "2023-01-15 14:45:00", 1, 2.5, 12.50, 2.00, 15.50, 161, 237, 1, 1),
    ("2023-01-15 15:00:00", "2023-01-15 15:20:00", 1, 3.2, 15.00, 3.00, 19.00, 237, 161, 2, 1),
    ("2023-01-15 16:00:00", "2023-01-15 16:15:00", 1, 1.8, 8.50, 0.00, 9.50, 161, 170, 1, 2),
    # Duplicate for testing
    ("2023-01-15 14:30:00", "2023-01-15 14:45:00", 1, 2.5, 12.50, 2.00, 15.50, 161, 237, 1, 1),
    # Invalid record (negative fare)
    ("2023-01-15 17:00:00", "2023-01-15 17:30:00", 1, 5.0, -10.00, 0.00, -10.00, 161, 237, 1, 1),
]

columns = [
    "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count", 
    "trip_distance", "fare_amount", "tip_amount", "total_amount",
    "PULocationID", "DOLocationID", "payment_type", "RatecodeID"
]

# Create DataFrame
bronze_test = spark.createDataFrame(sample_data, columns)

# Add metadata columns to simulate Bronze layer
bronze_test = (bronze_test
    .withColumn("ingested_at", lit(datetime.now()))
    .withColumn("source_file", lit("test_data.csv"))
)

print(f"\n📊 Test Bronze Data: {bronze_test.count()} records")
print("\nBronze Schema:")
bronze_test.printSchema()
print("\nBronze Sample:")
bronze_test.show()

# Import the transformation function
import sys
sys.path.append('/Users/udayshankar/Documents/ML Projects/data-mastery/realworld-usecases/01-modern-lakehouse/notebooks')

from silver_transformation_02 import transform_to_silver

# Test the transformation
print("\n🔄 Running Silver transformation...")
try:
    silver_test = transform_to_silver(bronze_test)
    
    print(f"\n✅ Silver transformation successful!")
    print(f"Clean records: {silver_test.count()} (from {bronze_test.count()} bronze records)")
    
    print("\nSilver Schema:")
    silver_test.printSchema()
    
    print("\nSilver Sample:")
    silver_test.show(truncate=False)
    
    print("\n📈 Quality Checks:")
    print(f"Duplicates removed: {bronze_test.count() - silver_test.count()}")
    print(f"All fares > 0: {silver_test.filter('fare_amount > 0').count() == silver_test.count()}")
    print(f"All distances > 0: {silver_test.filter('trip_distance > 0').count() == silver_test.count()}")
    
except Exception as e:
    print(f"❌ Error during transformation: {e}")
    import traceback
    traceback.print_exc()

spark.stop()
print("\n✅ Test complete!")
