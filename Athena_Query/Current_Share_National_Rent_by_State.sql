WITH latest_zori AS
(
       SELECT regionname,
              statename,
              zori
       FROM   transformed_data
       WHERE  DATE IN
              (
                     SELECT Max(DATE)
                     FROM   transformed_data) ), state_avg AS
(
         SELECT   statename,
                  Avg(zori) AS avg_state_zori -- Unweighted average ZORI for each state
         FROM     latest_zori
         GROUP BY statename ), national_avg AS
(
       SELECT Avg(zori) AS avg_national_zori
       FROM   latest_zori )
SELECT   s.statename ,
         (s.avg_state_zori / n.avg_national_zori) * 100 AS state_share_of_national
FROM     state_avg s,
         national_avg n
WHERE    statename IS NOT NULL
ORDER BY state_share_of_national DESC limit 10;