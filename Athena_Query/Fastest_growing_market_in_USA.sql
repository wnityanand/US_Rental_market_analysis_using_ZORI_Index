
WITH latest_dates AS (
 SELECT
   MAX(Date) AS latest_date
 FROM
   transformed_data
),
year_ago_dates AS (
 SELECT
   DATE_ADD('year', -1, latest_date) AS year_ago_date
 FROM
   latest_dates
),
latest_zori AS (
 SELECT
   RegionName,
   ZORI AS latest_zori
 FROM
   transformed_data
 WHERE
   Date = (SELECT latest_date FROM latest_dates)
),
year_ago_zori AS (
 SELECT
   RegionName,
   ZORI AS year_ago_zori
 FROM
   transformed_data
 WHERE
   Date = (SELECT year_ago_date FROM year_ago_dates)
)
SELECT
 l.RegionName AS "Region",
 l.latest_zori AS "Latest ZORI (Year 2025) ",
 y.year_ago_zori AS "Year Ago ZORI (Year 2024)",
 ROUND(100.0 * (l.latest_zori - y.year_ago_zori) / y.year_ago_zori, 2) AS "YoY Growth (%)"
FROM
 latest_zori l
 JOIN year_ago_zori y ON l.RegionName = y.RegionName
ORDER BY
 "YoY Growth (%)" DESC
LIMIT 10
