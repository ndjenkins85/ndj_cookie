-- Example of a Chi squared test
-- Step 1: Calculate counts and form into a distinct table
WITH aggs_table_1 AS (
    SELECT DISTINCT
        sex,
        AVG(fare) OVER(
            PARTITION BY sex
        ) AS sex_fare_avg,
        AVG(fare * fare) OVER(
            PARTITION BY sex
        ) AS var_1,
        COUNT(*) OVER(
            PARTITION BY sex
        ) AS sex_counts
    FROM titanic
),

aggs_table_2 AS (
    SELECT
        *,
        POWER(var_1 - (sex_fare_avg * sex_fare_avg), 0.5) AS std
    FROM aggs_table_1
)

SELECT
    *
FROM aggs_table_2
