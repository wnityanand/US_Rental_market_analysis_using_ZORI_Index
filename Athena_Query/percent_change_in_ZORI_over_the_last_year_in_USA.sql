WITH dates
     AS (SELECT Max(DATE)                       AS latest,
                Date_add('year', -1, Max(DATE)) AS prev_year
         FROM   transformed_data)
SELECT ( Max(CASE
               WHEN DATE = d.latest THEN zori
             END) - Max(CASE
                          WHEN DATE = d.prev_year THEN zori
                        END) ) / Max(CASE
                                       WHEN DATE = d.prev_year THEN zori
                                     END) * 100 AS yoy_growth_pct
FROM   transformed_data,
       dates d
WHERE  regionname = 'United States'