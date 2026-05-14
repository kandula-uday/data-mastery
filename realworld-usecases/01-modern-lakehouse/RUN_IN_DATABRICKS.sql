-- =====================================================================
-- RUN THESE SQLs DIRECTLY IN DATABRICKS SQL EDITOR
-- =====================================================================
-- These are simplified versions of the dbt models
-- Just copy-paste into Databricks and execute!
-- =====================================================================

-- =====================================================================
-- 1. GOLD DAILY SUMMARY - Daily Business KPIs
-- =====================================================================
-- Run this first to create the daily summary table
-- =====================================================================

CREATE OR REPLACE TABLE gold_daily_summary AS
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
        
    FROM silver_trips
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
ORDER BY pickup_date DESC;

-- View the results
SELECT * FROM gold_daily_summary LIMIT 10;


-- =====================================================================
-- 2. GOLD HOURLY PATTERNS - Hourly Demand Analysis
-- =====================================================================

CREATE OR REPLACE TABLE gold_hourly_patterns AS
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
        
    FROM silver_trips
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
    
    -- Demand indicator
    ROUND(trip_count * 1.0 / SUM(trip_count) OVER (PARTITION BY pickup_date), 4) as pct_of_daily_trips,
    
    -- Metadata
    CURRENT_TIMESTAMP() as calculated_at
    
FROM hourly_stats
ORDER BY pickup_date DESC, pickup_hour;

-- View the results
SELECT * FROM gold_hourly_patterns WHERE pickup_date = (SELECT MAX(pickup_date) FROM gold_hourly_patterns) ORDER BY pickup_hour;


-- =====================================================================
-- 3. GOLD TOP ROUTES - Most Popular Routes
-- =====================================================================

CREATE OR REPLACE TABLE gold_top_routes AS
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
        
    FROM silver_trips
    WHERE pickup_location_id IS NOT NULL 
      AND dropoff_location_id IS NOT NULL
    GROUP BY pickup_location_id, dropoff_location_id
    HAVING COUNT(*) >= 10  -- Minimum threshold
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
    
    -- Route profitability score
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
WHERE trip_rank <= 500  -- Top 500 routes
ORDER BY total_trips DESC;

-- View top 20 routes
SELECT * FROM gold_top_routes LIMIT 20;


-- =====================================================================
-- 4. GOLD REVENUE BY PAYMENT - Payment Method Analysis
-- =====================================================================

CREATE OR REPLACE TABLE gold_revenue_by_payment AS
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
        
    FROM silver_trips
    WHERE payment_type IS NOT NULL
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
ORDER BY pickup_date DESC, transaction_count DESC;

-- View the results
SELECT * FROM gold_revenue_by_payment WHERE pickup_date = (SELECT MAX(pickup_date) FROM gold_revenue_by_payment);


-- =====================================================================
-- QUICK QUERIES TO ANALYZE YOUR GOLD TABLES
-- =====================================================================

-- Check table creation
SHOW TABLES LIKE 'gold_%';

-- Quick stats
SELECT 'gold_daily_summary' as table_name, COUNT(*) as row_count FROM gold_daily_summary
UNION ALL
SELECT 'gold_hourly_patterns', COUNT(*) FROM gold_hourly_patterns
UNION ALL
SELECT 'gold_top_routes', COUNT(*) FROM gold_top_routes
UNION ALL
SELECT 'gold_revenue_by_payment', COUNT(*) FROM gold_revenue_by_payment;

-- View sample data from each table
SELECT 'Daily Summary - Last 5 Days' as report;
SELECT * FROM gold_daily_summary ORDER BY pickup_date DESC LIMIT 5;

SELECT 'Hourly Patterns - Latest Day' as report;
SELECT * FROM gold_hourly_patterns WHERE pickup_date = (SELECT MAX(pickup_date) FROM gold_hourly_patterns) ORDER BY pickup_hour;

SELECT 'Top 10 Routes' as report;
SELECT * FROM gold_top_routes LIMIT 10;

SELECT 'Revenue by Payment - Latest Day' as report;
SELECT * FROM gold_revenue_by_payment WHERE pickup_date = (SELECT MAX(pickup_date) FROM gold_revenue_by_payment);
