-- Example of a Chi squared test
-- Step 1: Calculate counts and form into a distinct table
WITH counts_table AS (
    SELECT DISTINCT
        embarked,
        sex,
        COUNT(*) OVER(
            PARTITION BY sex, embarked
        ) AS cell_count,
        COUNT(*) OVER(
            PARTITION BY embarked
        ) AS embarked_count,
        COUNT(*) OVER(
            PARTITION BY sex
        ) AS sex_count,
        COUNT(*) OVER() AS total_count
    FROM titanic
    ORDER BY embarked
),

-- Step 2: Calculate the expected values
expected AS (
    SELECT
        *,
        ((1.0 * cell_count / sex_count)
            * (1.0 * cell_count / embarked_count))
        * total_count
        AS expected
    FROM counts_table
),

-- Step 3: Calculate individual cell Chi values
chi_cell AS (
    SELECT
        *,
        POWER((cell_count - expected), 2) AS chi_cell
    FROM expected
)

-- Step 4: Calculate the total Chi squared value; compare to criticality table.
SELECT
    *,
    SUM(chi_cell) OVER() AS chi_total
FROM chi_cell
