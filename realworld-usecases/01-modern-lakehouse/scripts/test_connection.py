"""
Test Databricks connection
"""

import os
from dotenv import load_dotenv

def test_connection():
    """Test connection to Databricks."""
    load_dotenv()
    
    print("🔍 Testing Databricks connection...\n")
    
    # Check environment variables
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")
    cluster_id = os.getenv("DATABRICKS_CLUSTER_ID")
    
    if not host:
        print("❌ DATABRICKS_HOST not set in .env")
        return False
    
    if not token:
        print("❌ DATABRICKS_TOKEN not set in .env")
        return False
    
    print(f"✅ Environment variables loaded")
    print(f"   Host: {host}")
    print(f"   Token: {token[:10]}...")
    print(f"   Cluster: {cluster_id}\n")
    
    try:
        from databricks import sql
        
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        server_hostname = host.replace("https://", "").replace("http://", "")
        
        print("🔗 Attempting connection...")
        print(f"   Server: {server_hostname}")
        print(f"   HTTP Path: {http_path}\n")
        
        connection = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=token
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 'Connection successful!' as message")
        result = cursor.fetchone()
        
        print(f"✅ Connection successful!")
        print(f"   Response: {result[0]}\n")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"\n🔍 Debug Information:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Details: {str(e)}")
        print(f"\n💡 Common Issues:")
        print(f"   1. Check if SQL Warehouse is running in Databricks")
        print(f"   2. Verify HTTP Path is correct: {os.getenv('DATABRICKS_HTTP_PATH')}")
        print(f"   3. Verify token is valid and not expired")
        print(f"   4. Check server hostname: {host.replace('https://', '')}")
        return False


if __name__ == "__main__":
    success = test_connection()
    exit(0 if success else 1)
