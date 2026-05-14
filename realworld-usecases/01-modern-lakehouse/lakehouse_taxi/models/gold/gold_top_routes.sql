{{
  config(
    materialized='table',
    file_format='delta'
  )
}}

/*
Gold Layer: Top Routes Analysis
================================
Identify most popular pickup/dropoff location pairs

Business Value:
- Route optimization
- Surge pricing zones
- Driver positioning strategy
- Infrastructure planning
*/

WITH route_metrics AS (
    SELECT
        pickup_location_id,
        dropoff_location_id,
        
        -- Volume metrics
        COUNT(*) as total_trips,
        COUNT(DISTINCT pickup_date) as days_active,
        
        -- Revenue metrics
        SUM(fare_amount) as total_revenue,
        AVG(fare_amount) as avg_fare,
        
        -- Trip characteristics
        AVG(trip_distance) as avg_distance,
        AVG(trip_duration_minutes) as avg_duration,
        
        -- Profitability indicators
        AVG(tip_percentage) as avg_tip_pct,
        SUM(tip_amount) as total_tips,
        
        -- Most recent activity
        MAX(pickup_date) as last_trip_date,
        MIN(pickup_date) as first_trip_date
        
    FROM {{ source('silver', 'silver_trips') }}
    
    WHERE pickup_location_id IS NOT NULL 
      AND dropoff_location_id IS NOT NULL
    
    GROUP BY pickup_location_id, dropoff_location_id
    
    -- Only keep routes with meaningful volume
    HAVING COUNT(*) >= 10
),

route_rankings AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY total_trips DESC) as trip_rank,
        ROW_NUMBER() OVER (ORDER BY total_revenue DESC) as revenue_rank,
        ROW_NUMBER() OVER (ORDER BY avg_tip_pct DESC) as tip_rank
    FROM route_metrics
)

SELECT
    pickup_location_id,
    dropoff_location_id,
    
    -- Volume
    total_trips,
    days_active,
    ROUND(total_trips * 1.0 / days_active, 2) as avg_trips_per_day,
    
    -- Rankings
    trip_rank,
    revenue_rank,
    tip_rank,
    
    -- Revenue
    ROUND(total_revenue, 2) as total_revenue,
    ROUND(avg_fare, 2) as avg_fare,
    ROUND(total_revenue / days_active, 2) as avg_daily_revenue,
    
    -- Trip characteristics
    ROUND(avg_distance, 2) as avg_distance_miles,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    
    -- Profitability
    ROUND(avg_tip_pct, 2) as avg_tip_percentage,
    ROUND(total_tips, 2) as total_tips,
    ROUND(total_tips / total_trips, 2) as avg_tip_per_trip,
    
    -- Route profitability score (weighted metric)
    ROUND(
        (avg_fare * 0.4) + 
        (avg_tip_pct * 0.3) + 
        (total_trips * 0.3),
        2
    ) as profitability_score,
    
    -- Time range
    first_trip_date,
    last_trip_date,
    DATEDIFF(last_trip_date, first_trip_date) as route_lifetime_days,
    
    -- Metadata
    CURRENT_TIMESTAMP() as calculated_at
    
FROM route_rankings

-- Return top 500 routes by trip volume
WHERE trip_rank <= 500

ORDER BY total_trips DESC
