WITH growth
     AS (SELECT regionname,
                statename,
                Min(zori) AS start_zori,
                Max(zori) AS end_zori
         FROM   transformed_data
         WHERE  DATE BETWEEN DATE'2021-01-01' AND DATE'2025-03-31'
         GROUP  BY regionname,
                   statename)
SELECT ( ( end_zori - start_zori ) / start_zori ) * 100 AS growth_rate_percent
FROM   growth
WHERE  start_zori > 0 