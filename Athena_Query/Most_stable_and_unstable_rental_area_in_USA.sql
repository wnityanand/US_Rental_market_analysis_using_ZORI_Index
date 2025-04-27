WITH monthly_change AS
(
         SELECT   regionname,
                  statename,
                  DATE,
                  zori,
                  Lag(zori) over (PARTITION BY regionname, statename ORDER BY DATE) AS prev_zori
         FROM     transformed_data
         WHERE    DATE BETWEEN DATE'2023-01-01' AND      DATE'2024-12-31' ), change_stats AS
(
         SELECT   regionname,
                  statename,
                  STDDEV(zori - prev_zori) AS change_volatility,
                  Count(*)                 AS periods
         FROM     monthly_change
         WHERE    prev_zori IS NOT NULL
         GROUP BY regionname,
                  statename
         HAVING   Count(*) > 2 )
SELECT   regionname,
         statename,
         change_volatility
FROM     change_stats
ORDER BY change_volatility ASC limit 10;