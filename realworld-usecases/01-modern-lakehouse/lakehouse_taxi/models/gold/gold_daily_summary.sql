{{
  config(
    materialized='incremental',
    unique_key='pickup_date',
    file_format='delta',
    partition_by=['pickup_date'],
    incremental_strategy='merge'
  )
}}

/*
Gold Layer: Daily Trip Summary
================================
Business metrics aggregated by day for executive reporting

Metrics Tracked:
- Trip volume
- Revenue metrics
- Distance patterns
- Tip behavior
- Payment methods
*/

WITH daily_metrics AS (
    SELECT
        pickup_date,
        COUNT(*) as total_trips,
        COUNT(DISTINCT passenger_count) as unique_passenger_counts,
        
        -- Revenue metrics
        SUM(fare_amount) as total_revenue,
        AVG(fare_amount) as avg_fare,
        MIN(fare_amount) as min_fare,
        MAX(fare_amount) as max_fare,
        PERCENTILE(fare_amount, 0.5) as median_fare,
        
        -- Distance metrics
        SUM(trip_distance) as total_distance,
        AVG(trip_distance) as avg_distance,
        
        -- Duration metrics
        AVG(trip_duration_minutes) as avg_duration_minutes,
        
        -- Tip metrics
        SUM(tip_amount) as total_tips,
        AVG(tip_percentage) as avg_tip_percentage,
        SUM(CASE WHEN tip_percentage > 20 THEN 1 ELSE 0 END) as high_tip_trips,
        SUM(CASE WHEN tip_percentage = 0 THEN 1 ELSE 0 END) as no_tip_trips,
        
        -- Payment analysis
        COUNT(DISTINCT payment_type) as payment_types_used,
        
        -- Passenger analysis
        SUM(passenger_count) as total_passengers,
        AVG(passenger_count) as avg_passengers_per_trip
        
    FROM {{ source('silver', 'silver_trips') }}
    
    {% if is_incremental() %}
        -- Only process new data on incremental runs
        WHERE pickup_date > (SELECT MAX(pickup_date) FROM {{ this }})
    {% endif %}
    
    GROUP BY pickup_date
)

SELECT 
    pickup_date,
    total_trips,
    unique_passenger_counts,
    
    -- Revenue
    ROUND(total_revenue, 2) as total_revenue,
    ROUND(avg_fare, 2) as avg_fare,
    ROUND(min_fare, 2) as min_fare,
    ROUND(max_fare, 2) as max_fare,
    ROUND(median_fare, 2) as median_fare,
    
    -- Distance
    ROUND(total_distance, 2) as total_distance_miles,
    ROUND(avg_distance, 2) as avg_distance_miles,
    
    -- Duration
    ROUND(avg_duration_minutes, 2) as avg_duration_minutes,
    
    -- Tips
    ROUND(total_tips, 2) as total_tips,
    ROUND(avg_tip_percentage, 2) as avg_tip_percentage,
    high_tip_trips,
    no_tip_trips,
    ROUND(high_tip_trips * 100.0 / NULLIF(total_trips, 0), 2) as high_tip_percentage_of_total,
    ROUND(no_tip_trips * 100.0 / NULLIF(total_trips, 0), 2) as no_tip_percentage_of_total,
    
    -- Payment & Passengers
    payment_types_used,
    total_passengers,
    ROUND(avg_passengers_per_trip, 2) as avg_passengers_per_trip,
    
    -- Metadata
    CURRENT_TIMESTAMP() as calculated_at
    
FROM daily_metrics
ORDER BY pickup_date DESC
