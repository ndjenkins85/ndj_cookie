-- Use date of titanic sinking to help cast estimated DOB for passengers
-- Further, we can show as year, as start of month, and calculate datediffs
WITH titanic_dob AS (
    SELECT
        *,
        DATE("1912-04-15", "-" || CAST(age * 365 AS INT) || " days") AS dob
    FROM titanic
)

SELECT
    STRFTIME("%Y", dob) AS dob_year,
    DATE(STRFTIME("%Y-%m-01", dob)) AS start_of_month,
    DATE(DATE(STRFTIME("%Y-%m-01", dob), "+1 month"), "-1 day") AS end_of_month,
    (JULIANDAY('now') - JULIANDAY(dob)) / 365 AS born_years_ago
FROM titanic_dob
WHERE dob_year >= "1850"
    AND dob_year <= "1901"
