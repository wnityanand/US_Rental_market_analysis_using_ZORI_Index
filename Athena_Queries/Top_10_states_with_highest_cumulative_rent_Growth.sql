WITH first_last AS
(
         SELECT   statename,
                  Min(DATE) AS first_date,
                  Max(DATE) AS last_date
         FROM     transformed_data
         WHERE    DATE BETWEEN DATE'2021-01-01' AND      DATE '2025-03-01'
         GROUP BY statename ), first_zori AS
(
         SELECT   f.statename,
                  Avg(zori) AS first_zori
         FROM     (
                         SELECT *
                         FROM   transformed_data
                         WHERE  DATE BETWEEN DATE'2021-01-01' AND    DATE '2025-03-01') t
         join     first_last f
         ON       t.statename = f.statename
         AND      t.DATE = f.first_date
         GROUP BY f.statename ), last_zori AS
(
         SELECT   f.statename,
                  Avg(zori) AS last_zori
         FROM     (
                         SELECT *
                         FROM   transformed_data
                         WHERE  DATE BETWEEN DATE'2021-01-01' AND    DATE '2025-03-01') t
         join     first_last f
         ON       t.statename = f.statename
         AND      t.DATE = f.last_date
         GROUP BY f.statename )
SELECT   f.statename,
         Round(100.0 * (l.last_zori - f.first_zori) / f.first_zori, 2) AS cumulative_growth_pct
FROM     first_zori f
join     last_zori l
ON       f.statename = l.statename
ORDER BY cumulative_growth_pct DESC limit 10;