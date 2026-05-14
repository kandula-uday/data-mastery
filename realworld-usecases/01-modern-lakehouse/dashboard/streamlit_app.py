"""
NYC Taxi Analytics Dashboard
Fetches data from Databricks Gold layer tables via SQL API
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from databricks import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🚕 NYC Taxi Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# DATABASE CONNECTION
# ============================================================================

@st.cache_resource
def get_databricks_connection():
    """Establish connection to Databricks SQL Warehouse."""
    try:
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        return connection
    except Exception as e:
        st.error(f"❌ Failed to connect to Databricks: {e}")
        st.info("💡 Make sure your .env file has correct credentials")
        return None


@st.cache_data(ttl=300)  # Cache for 5 minutes
def query_gold_table(query):
    """Execute SQL query and return pandas DataFrame."""
    connection = get_databricks_connection()
    if connection is None:
        return pd.DataFrame()
    
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        df = cursor.fetchall_arrow().to_pandas()
        cursor.close()
        return df
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        return pd.DataFrame()


# ============================================================================
# DATA FETCHING FUNCTIONS
# ============================================================================

def fetch_daily_summary():
    """Fetch daily trip summary from Gold layer."""
    query = """
    SELECT 
        pickup_date,
        total_trips,
        total_revenue,
        total_tips,
        avg_fare,
        avg_distance,
        avg_duration,
        avg_tip_pct
    FROM gold_daily_summary
    ORDER BY pickup_date DESC
    LIMIT 100
    """
    return query_gold_table(query)


def fetch_hourly_patterns():
    """Fetch hourly trip patterns."""
    query = """
    SELECT 
        pickup_hour,
        trip_count,
        avg_fare,
        avg_duration
    FROM gold_hourly_patterns
    ORDER BY pickup_hour
    """
    return query_gold_table(query)


def fetch_revenue_metrics():
    """Fetch revenue breakdown by payment type."""
    query = """
    SELECT 
        payment_type,
        SUM(trip_count) as total_trips,
        SUM(total_revenue) as total_revenue,
        AVG(avg_tip_pct) as avg_tip_percentage
    FROM gold_revenue_metrics
    GROUP BY payment_type
    ORDER BY total_revenue DESC
    """
    return query_gold_table(query)


# ============================================================================
# DASHBOARD LAYOUT
# ============================================================================

def main():
    # Header
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🚕 NYC Taxi Analytics Dashboard</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Real-time insights from the Databricks Data Lakehouse</p>", 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Test connection
    with st.spinner("🔗 Connecting to Databricks..."):
        connection = get_databricks_connection()
        if connection is None:
            st.stop()
        st.success("✅ Connected to Databricks!")
    
    # Fetch data
    with st.spinner("📊 Loading data from Gold layer..."):
        daily_summary = fetch_daily_summary()
        hourly_patterns = fetch_hourly_patterns()
        revenue_metrics = fetch_revenue_metrics()
    
    if daily_summary.empty:
        st.error("❌ No data found in Gold tables. Have you run the Gold aggregation pipeline?")
        st.stop()
    
    # ========================================================================
    # KEY METRICS (Top Row)
    # ========================================================================
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_trips = daily_summary['total_trips'].sum()
        st.metric(
            label="🚖 Total Trips",
            value=f"{total_trips:,.0f}",
            delta=f"{daily_summary['total_trips'].iloc[0]:,.0f} today"
        )
    
    with col2:
        total_revenue = daily_summary['total_revenue'].sum()
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.2f}",
            delta=f"${daily_summary['total_revenue'].iloc[0]:,.2f} today"
        )
    
    with col3:
        avg_fare = daily_summary['avg_fare'].mean()
        st.metric(
            label="💵 Avg Fare",
            value=f"${avg_fare:.2f}",
            delta=f"{((avg_fare - daily_summary['avg_fare'].iloc[-1]) / daily_summary['avg_fare'].iloc[-1] * 100):.1f}%"
        )
    
    with col4:
        avg_distance = daily_summary['avg_distance'].mean()
        st.metric(
            label="📏 Avg Distance",
            value=f"{avg_distance:.2f} mi",
            delta=f"{daily_summary['avg_distance'].iloc[0]:.2f} mi today"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # DAILY TRENDS (Second Row)
    # ========================================================================
    st.subheader("📅 Daily Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily trips chart
        fig_trips = px.line(
            daily_summary.sort_values('pickup_date'),
            x='pickup_date',
            y='total_trips',
            title='Daily Trip Volume',
            labels={'pickup_date': 'Date', 'total_trips': 'Number of Trips'},
            markers=True
        )
        fig_trips.update_traces(line_color='#1f77b4', line_width=3)
        st.plotly_chart(fig_trips, use_container_width=True)
    
    with col2:
        # Daily revenue chart
        fig_revenue = px.line(
            daily_summary.sort_values('pickup_date'),
            x='pickup_date',
            y='total_revenue',
            title='Daily Revenue',
            labels={'pickup_date': 'Date', 'total_revenue': 'Revenue ($)'},
            markers=True
        )
        fig_revenue.update_traces(line_color='#2ca02c', line_width=3)
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # HOURLY PATTERNS (Third Row)
    # ========================================================================
    st.subheader("⏰ Hourly Patterns")
    
    if not hourly_patterns.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Trips by hour
            fig_hourly = px.bar(
                hourly_patterns,
                x='pickup_hour',
                y='trip_count',
                title='Trip Volume by Hour of Day',
                labels={'pickup_hour': 'Hour', 'trip_count': 'Number of Trips'},
                color='trip_count',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
        
        with col2:
            # Avg fare by hour
            fig_fare_hourly = px.line(
                hourly_patterns,
                x='pickup_hour',
                y='avg_fare',
                title='Average Fare by Hour',
                labels={'pickup_hour': 'Hour', 'avg_fare': 'Average Fare ($)'},
                markers=True
            )
            fig_fare_hourly.update_traces(line_color='#ff7f0e', line_width=3)
            st.plotly_chart(fig_fare_hourly, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # TOP PATTERNS & REVENUE (Fourth Row)
    # ========================================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("� Trip Statistics")
        if not daily_summary.empty:
            # Show summary statistics
            stats_data = {
                'Metric': ['Total Trips', 'Total Revenue', 'Avg Trip Distance', 'Avg Trip Duration', 'Avg Tip %'],
                'Value': [
                    f"{daily_summary['total_trips'].sum():,.0f}",
                    f"${daily_summary['total_revenue'].sum():,.2f}",
                    f"{daily_summary['avg_distance'].mean():.2f} miles",
                    f"{daily_summary['avg_duration'].mean():.2f} min",
                    f"{daily_summary['avg_tip_pct'].mean():.2f}%"
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True, height=250)
            
            # Show daily breakdown table
            st.subheader("📅 Recent Daily Breakdown")
            recent_days = daily_summary.head(10)[['pickup_date', 'total_trips', 'total_revenue', 'avg_fare']]
            recent_days.columns = ['Date', 'Trips', 'Revenue ($)', 'Avg Fare ($)']
            st.dataframe(recent_days, use_container_width=True, hide_index=True)
        else:
            st.info("No statistics available")
    
    with col2:
        st.subheader("💳 Revenue by Payment Type")
        if not revenue_metrics.empty:
            # Payment type pie chart
            fig_payment = px.pie(
                revenue_metrics,
                values='total_revenue',
                names='payment_type',
                title='Revenue Distribution by Payment Type',
                hole=0.4
            )
            st.plotly_chart(fig_payment, use_container_width=True)
            
            # Payment metrics table
            st.dataframe(
                revenue_metrics[['payment_type', 'total_trips', 'total_revenue', 'avg_tip_percentage']].round(2),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No payment data available")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>📊 Data Source: Databricks Gold Layer | 🔄 Cache: 5 minutes | 🏗️ Architecture: Medallion (Bronze → Silver → Gold)</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
