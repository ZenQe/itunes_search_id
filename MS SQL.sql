SELECT TOP 5 value,
		 COUNT(value)
FROM 
	(SELECT *,
		 datediff(minute, lag_time, event_time) AS minutes
	FROM 
		(SELECT *,
		 lag(event_time, 1) OVER (order by user_id, event_time) AS lag_time,
         lag(value,1) OVER (order by user_id, event_time) AS lag_value,
			CASE
			WHEN lag(user_id) over(order by user_id) = user_id 
         		THEN	1
				ELSE 0
			END AS pr_user
		FROM log ) AS q
     	WHERE value = lag_value	AND
     		  datediff(minute, lag_time, event_time) < 5 ) AS q2
              
GROUP BY  user_id, value
HAVING COUNT(value) > 1
ORDER BY  COUNT(value) DESC