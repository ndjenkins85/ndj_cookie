-- Example of multiple with, and random sampling
-- in sqlite, can use RANDOM() line below to get a float between 0-1.
-- NOTE! The column will continue to be random with subsequent calculations
-- THUS the results will not match final output (note the WHERE > 0.3)
-- This looks to create a stratified sample of 2x3 choices, age and pclass
-- And returns 5 candidates from each
WITH base AS (
    SELECT
        *,
        ABS(RANDOM()) / 9223372036854775808 AS random_num
    FROM titanic
),

stratify AS (
    SELECT
        *,
        ROW_NUMBER() OVER(
            PARTITION BY sex, pclass
            ORDER BY random_num DESC
        ) AS row_rank
    FROM base
    WHERE random_num < 0.3
)

SELECT
    name,
    sex,
    pclass,
    row_rank,
    random_num
FROM stratify
WHERE row_rank <= 5
ORDER BY sex, pclass, row_rank
