"""
Fetch data from Databricks via SQL API and process locally
This allows you to develop/test transformations on your laptop!
"""

import os
import pandas as pd
from databricks import sql
from dotenv import load_dotenv

# Load credentials
load_dotenv()

def fetch_bronze_data(limit=1000):
    """
    Fetch Bronze data from Databricks via SQL API
    Returns: pandas DataFrame
    """
    print(f"🔗 Connecting to Databricks...")
    
    connection = sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )
    
    cursor = connection.cursor()
    
    # Query Bronze table (limit for local testing)
    query = f"""
    SELECT *
    FROM bronze_raw_trips
    LIMIT {limit}
    """
    
    print(f"📊 Fetching {limit} records from bronze_raw_trips...")
    cursor.execute(query)
    
    # Fetch results as pandas DataFrame
    df = cursor.fetchall_arrow().to_pandas()
    
    cursor.close()
    connection.close()
    
    print(f"✅ Fetched {len(df):,} records")
    return df


def transform_locally(bronze_df):
    """
    Apply Silver transformations using pandas (local processing)
    """
    print("\n🔄 Applying transformations locally...")
    
    # Convert to datetime
    bronze_df['pickup_datetime'] = pd.to_datetime(bronze_df['Trip_Pickup_DateTime'])
    bronze_df['dropoff_datetime'] = pd.to_datetime(bronze_df['Trip_Dropoff_DateTime'])
    
    # Remove duplicates
    initial_count = len(bronze_df)
    silver_df = bronze_df.drop_duplicates(
        subset=['Trip_Pickup_DateTime', 'Trip_Dropoff_DateTime', 'Passenger_Count', 'Trip_Distance']
    )
    print(f"   Removed {initial_count - len(silver_df)} duplicates")
    
    # Filter invalid records
    silver_df = silver_df[
        (silver_df['Fare_Amt'] > 0) &
        (silver_df['Trip_Distance'] > 0)
    ]
    
    # Calculate trip duration
    silver_df['trip_duration_minutes'] = (
        (silver_df['dropoff_datetime'] - silver_df['pickup_datetime']).dt.total_seconds() / 60
    ).round(2)
    
    # Calculate tip percentage
    silver_df['tip_percentage'] = (
        (silver_df['Tip_Amt'] / silver_df['Fare_Amt']) * 100
    ).round(2)
    
    # Extract date parts
    silver_df['pickup_date'] = silver_df['pickup_datetime'].dt.date
    silver_df['pickup_hour'] = silver_df['pickup_datetime'].dt.hour
    
    print(f"✅ Transformation complete: {len(silver_df):,} clean records")
    
    return silver_df


def save_locally(df, output_path="./data/processed/silver_sample.parquet"):
    """Save processed data locally"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    print(f"💾 Saved to: {output_path}")


def main():
    print("=" * 70)
    print("🚀 LOCAL DEVELOPMENT MODE")
    print("   Fetch data from Databricks → Process locally → Test transformations")
    print("=" * 70)
    
    # Step 1: Fetch sample data from Databricks
    bronze_df = fetch_bronze_data(limit=5000)  # Small sample for local testing
    
    print(f"\n📋 Bronze Data Info:")
    print(f"   Rows: {len(bronze_df):,}")
    print(f"   Columns: {len(bronze_df.columns)}")
    print(f"   Memory: {bronze_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Step 2: Transform locally (using pandas, not Spark!)
    silver_df = transform_locally(bronze_df)
    
    # Step 3: Explore results
    print(f"\n📊 Silver Data Summary:")
    print(silver_df[['pickup_date', 'pickup_hour', 'Fare_Amt', 'Trip_Distance', 'trip_duration_minutes']].describe())
    
    # Step 4: Save for further analysis
    save_locally(silver_df)
    
    print("\n" + "=" * 70)
    print("✅ LOCAL PROCESSING COMPLETE!")
    print("=" * 70)
    print("\n💡 You can now:")
    print("   1. Explore the data in Jupyter/pandas")
    print("   2. Test different transformation logic")
    print("   3. Once satisfied, apply to full dataset in Databricks")
    
    return silver_df


if __name__ == "__main__":
    df = main()
    print("\n🎉 Data available as 'df' variable for further exploration!")
