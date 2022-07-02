-- Example of window range function.
-- RANGE will do it by order by (acts like the partition)
-- ROWS will do it by rows, like row_number
-- can use UNBOUNDED unstead of a number
-- can use CURRENT ROW instead of PRECEDING or FOLLOWING
-- This example shows average survival of the age group +/- one year,
-- or more specifically, +/- age group (as there are some 0.5's)
SELECT
    name,
    age,
    survived,
    AVG(survived) OVER(
        ORDER BY age
        RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS average_similar_survival
FROM titanic
WHERE age >= 18
ORDER BY age, name
