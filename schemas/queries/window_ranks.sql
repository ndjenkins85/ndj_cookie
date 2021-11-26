-- Example of window ranking functions.
-- We show three different types of ranking;
-- ROW_NUMER() will always assign an increment; this may not be ideal
-- as it may not be fully deterministic given the data
-- RANK() goes from tied 1st to 3rd.
-- DENSE_RANK() goes from tied 1st to 2nd.
-- This example shows rank of who paid most, partitioned by fare class.
SELECT
    name,
    survived,
    pclass,
    fare,
    ROW_NUMBER() OVER(
        PARTITION BY pclass
        ORDER BY fare DESC
    ) AS row_num,
    RANK() OVER(
        PARTITION BY pclass
        ORDER BY fare DESC
    ) AS rank_example,
    DENSE_RANK() OVER(
        PARTITION BY pclass
        ORDER BY fare DESC
    ) AS dense_rank_example
FROM titanic
WHERE fare > 0
ORDER BY dense_rank_example
