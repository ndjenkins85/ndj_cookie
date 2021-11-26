-- Example of window function. With the distinct, this behaves
-- Very similar to a group by. Without the DISTICT, this would
-- Add the info into every cell
SELECT DISTINCT
    sex,
    embarked,
    COUNT(sex) OVER(
        PARTITION BY sex, embarked
        ORDER BY embarked
    ) AS count_of_sex
FROM titanic
