"""
NYC Taxi Analytics Dashboard
Interactive Streamlit dashboard for exploring taxi trip data.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from databricks import sql
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="NYC Taxi Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_connection():
    """Establish connection to Databricks SQL Warehouse."""
    try:
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        return connection
    except Exception as e:
        st.error(f"Failed to connect to Databricks: {e}")
        return None


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_daily_summary():
    """Fetch data from gold_daily_summary table."""
    connection = get_connection(
            server_hostname=os.getenv("DATABRICKS_HOST", "").replace("https://", ""),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        return connection
    except Exception as e:
        st.error(f"Failed to connect to Databricks: {e}")
        return None


@st.cache_data(ttl=3600)
def load_daily_summary():
    """Load daily summary data from Gold layer."""
    connection = get_connection()
    if not connection:
        return pd.DataFrame()
    
    query = """
    SELECT 
        pickup_date,
        total_trips,
        total_revenue,
        total_tips,
        avg_fare,
        avg_distance,
        avg_duration
    FROM gold.daily_summary
    ORDER BY pickup_date DESC
    LIMIT 365
    """
    
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    df = pd.DataFrame(data, columns=columns)
    df['pickup_date'] = pd.to_datetime(df['pickup_date'])
    return df


def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<h1 class="main-header">🚕 NYC Taxi Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Real-time insights from the Modern Data Lakehouse")
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # Load data
    with st.spinner("Loading data from lakehouse..."):
        df = load_daily_summary()
    
    if df.empty:
        st.warning("⚠️ No data available. Please check your Databricks connection and ensure Gold tables exist.")
        st.info("💡 Follow the setup guide to populate data: `docs/setup-guide.md`")
        return
    
    # Date range filter
    min_date = df['pickup_date'].min()
    max_date = df['pickup_date'].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(max_date - timedelta(days=30), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    if len(date_range) == 2:
        mask = (df['pickup_date'] >= pd.Timestamp(date_range[0])) & \
               (df['pickup_date'] <= pd.Timestamp(date_range[1]))
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # KPI Cards
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_trips = filtered_df['total_trips'].sum()
        st.metric(
            label="🚕 Total Trips",
            value=f"{total_trips:,.0f}",
            delta=f"{total_trips/len(filtered_df):.0f} avg/day"
        )
    
    with col2:
        total_revenue = filtered_df['total_revenue'].sum()
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"${total_revenue/len(filtered_df):,.0f} avg/day"
        )
    
    with col3:
        avg_fare = filtered_df['avg_fare'].mean()
        st.metric(
            label="💵 Avg Fare",
            value=f"${avg_fare:.2f}",
            delta="per trip"
        )
    
    with col4:
        avg_distance = filtered_df['avg_distance'].mean()
        st.metric(
            label="📏 Avg Distance",
            value=f"{avg_distance:.2f} mi",
            delta="per trip"
        )
    
    st.markdown("---")
    
    # Charts
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺️ Routes", "💡 Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Trip volume over time
            fig1 = px.line(
                filtered_df,
                x='pickup_date',
                y='total_trips',
                title='Daily Trip Volume',
                labels={'pickup_date': 'Date', 'total_trips': 'Number of Trips'}
            )
            fig1.update_traces(line_color='#FFD700')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Revenue over time
            fig2 = px.area(
                filtered_df,
                x='pickup_date',
                y='total_revenue',
                title='Daily Revenue',
                labels={'pickup_date': 'Date', 'total_revenue': 'Revenue ($)'}
            )
            fig2.update_traces(line_color='#32CD32', fillcolor='rgba(50,205,50,0.3)')
            st.plotly_chart(fig2, use_container_width=True)
        
        # Average fare and distance
        col3, col4 = st.columns(2)
        
        with col3:
            fig3 = px.scatter(
                filtered_df,
                x='avg_distance',
                y='avg_fare',
                size='total_trips',
                color='total_trips',
                title='Fare vs Distance Analysis',
                labels={'avg_distance': 'Avg Distance (mi)', 'avg_fare': 'Avg Fare ($)'}
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            fig4 = px.line(
                filtered_df,
                x='pickup_date',
                y='avg_duration',
                title='Average Trip Duration',
                labels={'pickup_date': 'Date', 'avg_duration': 'Duration (min)'}
            )
            fig4.update_traces(line_color='#FF6347')
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab2:
        st.info("🗺️ Geographic analysis coming soon! Will include heatmaps and route visualization.")
        st.markdown("**Planned features:**")
        st.markdown("- Interactive map of pickup/dropoff locations")
        st.markdown("- Heatmap of popular zones")
        st.markdown("- Top routes visualization")
    
    with tab3:
        st.markdown("### 💡 Key Insights")
        
        # Calculate insights
        busiest_day = filtered_df.loc[filtered_df['total_trips'].idxmax()]
        highest_revenue_day = filtered_df.loc[filtered_df['total_revenue'].idxmax()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Performance Highlights")
            st.markdown(f"- **Busiest Day:** {busiest_day['pickup_date'].strftime('%Y-%m-%d')} "
                       f"({busiest_day['total_trips']:,.0f} trips)")
            st.markdown(f"- **Highest Revenue:** {highest_revenue_day['pickup_date'].strftime('%Y-%m-%d')} "
                       f"(${highest_revenue_day['total_revenue']:,.0f})")
            st.markdown(f"- **Average Trip:** {avg_distance:.2f} miles, {filtered_df['avg_duration'].mean():.1f} minutes")
        
        with col2:
            st.markdown("#### 📈 Trends")
            trip_trend = "📈 Increasing" if filtered_df['total_trips'].iloc[-1] > filtered_df['total_trips'].iloc[0] else "📉 Decreasing"
            st.markdown(f"- **Trip Volume:** {trip_trend}")
            st.markdown(f"- **Peak Performance:** {filtered_df['total_trips'].max():,.0f} trips/day")
            st.markdown(f"- **Average Performance:** {filtered_df['total_trips'].mean():,.0f} trips/day")
    
    # Footer
    st.markdown("---")
    st.markdown("**Data Source:** NYC Taxi & Limousine Commission | **Architecture:** Modern Data Lakehouse (Bronze → Silver → Gold)")
    st.markdown("*Dashboard built with Streamlit • Data processed with Databricks & Delta Lake*")


if __name__ == "__main__":
    main()
