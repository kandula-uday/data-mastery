{{
  config(
    materialized='incremental',
    unique_key=['pickup_date', 'payment_type'],
    file_format='delta',
    partition_by=['pickup_date'],
    incremental_strategy='merge'
  )
}}

/*
Gold Layer: Revenue Metrics by Payment Type
============================================
Financial analytics for business intelligence and reporting

Insights:
- Payment method trends
- Cash vs card behavior
- Revenue optimization opportunities
- Customer payment preferences
*/

WITH payment_analysis AS (
    SELECT
        pickup_date,
        payment_type,
        
        -- Volume metrics
        COUNT(*) as transaction_count,
        COUNT(DISTINCT pickup_location_id) as locations_served,
        
        -- Revenue breakdown
        SUM(fare_amount) as total_fares,
        SUM(tip_amount) as total_tips,
        SUM(total_amount) as total_revenue,
        
        AVG(fare_amount) as avg_fare,
        AVG(tip_amount) as avg_tip,
        AVG(total_amount) as avg_total,
        
        -- Tip behavior by payment type
        AVG(tip_percentage) as avg_tip_pct,
        SUM(CASE WHEN tip_amount > 0 THEN 1 ELSE 0 END) as trips_with_tips,
        
        -- Trip characteristics
        AVG(trip_distance) as avg_distance,
        AVG(trip_duration_minutes) as avg_duration,
        AVG(passenger_count) as avg_passengers
        
    FROM {{ source('silver', 'silver_trips') }}
    
    WHERE payment_type IS NOT NULL
    
    {% if is_incremental() %}
        AND pickup_date > (SELECT MAX(pickup_date) FROM {{ this }})
    {% endif %}
    
    GROUP BY pickup_date, payment_type
)

SELECT
    pickup_date,
    payment_type,
    
    -- Volume
    transaction_count,
    locations_served,
    
    -- Daily share
    ROUND(
        transaction_count * 100.0 / 
        SUM(transaction_count) OVER (PARTITION BY pickup_date),
        2
    ) as pct_of_daily_transactions,
    
    -- Revenue metrics
    ROUND(total_fares, 2) as total_fares,
    ROUND(total_tips, 2) as total_tips,
    ROUND(total_revenue, 2) as total_revenue,
    
    ROUND(avg_fare, 2) as avg_fare,
    ROUND(avg_tip, 2) as avg_tip,
    ROUND(avg_total, 2) as avg_transaction_amount,
    
    -- Revenue share
    ROUND(
        total_revenue * 100.0 / 
        SUM(total_revenue) OVER (PARTITION BY pickup_date),
        2
    ) as pct_of_daily_revenue,
    
    -- Tip analysis
    ROUND(avg_tip_pct, 2) as avg_tip_percentage,
    trips_with_tips,
    ROUND(trips_with_tips * 100.0 / NULLIF(transaction_count, 0), 2) as tip_rate,
    
    -- Trip characteristics
    ROUND(avg_distance, 2) as avg_distance_miles,
    ROUND(avg_duration, 2) as avg_duration_minutes,
    ROUND(avg_passengers, 2) as avg_passengers_per_trip,
    
    -- Performance indicators
    CASE 
        WHEN avg_tip_pct > 15 THEN 'High Tip Rate'
        WHEN avg_tip_pct > 10 THEN 'Medium Tip Rate'
        WHEN avg_tip_pct > 0 THEN 'Low Tip Rate'
        ELSE 'No Tips'
    END as tip_category,
    
    CASE
        WHEN avg_fare > 20 THEN 'Premium'
        WHEN avg_fare > 10 THEN 'Standard'
        ELSE 'Economy'
    END as fare_tier,
    
    -- Metadata
    CURRENT_TIMESTAMP() as calculated_at
    
FROM payment_analysis
ORDER BY pickup_date DESC, transaction_count DESC
