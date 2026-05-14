{{
  config(
    materialized='incremental',
    unique_key=['pickup_date', 'pickup_hour'],
    file_format='delta',
    partition_by=['pickup_date'],
    incremental_strategy='merge'
  )
}}

/*
Gold Layer: Hourly Demand Patterns
===================================
Analyze trip patterns by hour of day for operational planning

Use Cases:
- Peak hour identification
- Driver supply optimization
- Pricing strategy
- Demand forecasting
*/

WITH hourly_stats AS (
    SELECT
        pickup_date,
        pickup_hour,
        
        -- Volume metrics
        COUNT(*) as trip_count,
        COUNT(DISTINCT pickup_location_id) as unique_pickup_locations,
        COUNT(DISTINCT dropoff_location_id) as unique_dropoff_locations,
        
        -- Revenue metrics
        SUM(fare_amount) as hourly_revenue,
        AVG(fare_amount) as avg_fare,
        
        -- Trip characteristics
        AVG(trip_distance) as avg_distance,
        AVG(trip_duration_minutes) as avg_duration,
        
        -- Tip behavior by hour
        AVG(tip_percentage) as avg_tip_pct,
        SUM(CASE WHEN tip_percentage > 15 THEN 1 ELSE 0 END) as good_tippers,
        
        -- Passenger patterns
        SUM(passenger_count) as total_passengers,
        AVG(passenger_count) as avg_passengers
        
    FROM {{ source('silver', 'silver_trips') }}
    
    {% if is_incremental() %}
        WHERE pickup_date > (SELECT MAX(pickup_date) FROM {{ this }})
    {% endif %}
    
    GROUP BY pickup_date, pickup_hour
)

SELECT
    pickup_date,
    pickup_hour,
    
    -- Time classification
    CASE 
        WHEN pickup_hour BETWEEN 6 AND 9 THEN 'Morning Rush'
        WHEN pickup_hour BETWEEN 10 AND 15 THEN 'Midday'
        WHEN pickup_hour BETWEEN 16 AND 19 THEN 'Evening Rush'
        WHEN pickup_hour BETWEEN 20 AND 23 THEN 'Evening'
        ELSE 'Late Night'
    END as time_period,
    
    -- Metrics
    trip_count,
    unique_pickup_locations,
    unique_dropoff_locations,
    ROUND(hourly_revenue, 2) as hourly_revenue,
    ROUND(avg_fare, 2) as avg_fare,
    ROUND(avg_distance, 2) as avg_distance_miles,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    ROUND(avg_tip_pct, 2) as avg_tip_percentage,
    good_tippers,
    ROUND(good_tippers * 100.0 / NULLIF(trip_count, 0), 2) as good_tipper_rate,
    total_passengers,
    ROUND(avg_passengers, 2) as avg_passengers_per_trip,
    
    -- Demand indicator (relative to daily average)
    ROUND(trip_count * 1.0 / SUM(trip_count) OVER (PARTITION BY pickup_date), 4) as pct_of_daily_trips,
    
    -- Metadata
    CURRENT_TIMESTAMP() as calculated_at
    
FROM hourly_stats
ORDER BY pickup_date DESC, pickup_hour
