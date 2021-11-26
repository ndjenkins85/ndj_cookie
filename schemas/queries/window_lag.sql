-- Example of window lag function.
-- LAG can be used to offset rows.
-- LEAD similar just other direction; kinda useless cause we can use negatives!
-- Optional third argument to fill Null values
-- Often the order by will match to aid inspection that it's working
-- The Partition in this case is used to assist the offset by applying
-- Fare difference according to whether passenger survived or not
SELECT
    name,
    age,
    survived,
    fare,
    LAG(fare, 1, 0) OVER (
        PARTITION BY survived
        ORDER BY age, name
    ) AS fare_change
FROM titanic
WHERE age >= 18
ORDER BY age, name
