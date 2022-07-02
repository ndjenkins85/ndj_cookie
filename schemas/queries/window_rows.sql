-- Example of window rows function.
-- RANGE will do it by order by (acts like the partition)
-- ROWS will do it by rows, like row_number
-- can use UNBOUNDED unstead of a number
-- can use CURRENT ROW instead of PRECEDING or FOLLOWING, zero works too
-- This example shows sum of survivability for a range between the
-- last 10 passengers and the futher two on the list
SELECT
    name,
    age,
    survived,
    SUM(survived) OVER(
        ORDER BY age, name
        -- Removing the rows line will behave like a cumsum
        ROWS BETWEEN 10 PRECEDING AND 2 FOLLOWING
    ) AS average_similar_survival
FROM titanic
WHERE age >= 18
ORDER BY age, name
