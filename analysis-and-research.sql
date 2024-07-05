-- STEPWISE BUILDING THE RECURSIVE CTE QUERIES

-- REFERENCE: https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-recursive-query/

-- REGION can consist of ports or other regions

-- GET ALL slugs IN A REGION
WITH RECURSIVE sub_region AS (
	-- anchor member
	SELECT r1.slug, r1.parent_slug as parent_slug 
	FROM regions r1 
	WHERE r1.slug = 'northern_europe'

	UNION

	-- recursive member
	SELECT r2.slug as slug, r2.parent_slug as parent_slug 
	FROM regions r2 
	INNER JOIN sub_region sr1 ON sr1.slug = r2.parent_slug
)
SELECT * FROM sub_region;


-- GET ALL port codes IN A REGION (and also their sub-regions too)
WITH RECURSIVE sub_region AS (
	-- anchor member
	SELECT r1.slug, r1.parent_slug as parent_slug 
	FROM regions r1 
	WHERE r1.slug = 'scandinavia'

	UNION

	-- recursive member
	SELECT r2.slug as slug, r2.parent_slug as parent_slug 
	FROM regions r2 
	INNER JOIN sub_region sr1 ON sr1.slug = r2.parent_slug
),
regional_ports AS (
	SELECT p1.code AS port_code, p1.name AS port_name
	FROM ports p1
	JOIN sub_region sr2 ON p1.parent_slug = sr2.slug
)
SELECT port_code, port_name FROM regional_ports;


-- KEEPING THIS QUERY SEPARATE
-- I CAN USE THE ABOVE QUERY TO COMPUTE SOURCE PORTS AND DESTINATION PORTS
-- (if regions were passed, if not we directly have the single port)
-- CALL THE FOLLOWING AGGREGATOR QUERY


-- GET ONE LANE SHIPPING PRICES
WITH date_series AS (
    -- Generate a series of dates from start_date to end_date
    SELECT generate_series('2016-01-01'::date, '2016-01-31'::date, '1 day'::interval) AS day
),
daily_prices AS (
    -- Select and group by date, origin and destination ports
    SELECT ds1.day, p1.orig_code, p1.dest_code, AVG(p1.price) AS avg_price, COUNT(*) AS price_count
    FROM date_series ds1
    LEFT JOIN prices p1 ON ds1.day = p1.day AND p1.orig_code = 'CNGGZ' AND p1.dest_code = 'EETLL'
    GROUP BY ds1.day, p1.orig_code, p1.dest_code
)
-- Filter to only include dates with 3 or more records
SELECT
    day,
    CASE WHEN price_count >= 3 THEN avg_price ELSE NULL END AS avg_price
FROM daily_prices
ORDER BY day;



-- EXPAND TO USE AN ARRAY OF SOURCE AND DESTINATION PORTS
WITH date_series AS (
    -- Generate a series of dates from start_date to end_date
    SELECT generate_series('2016-01-01'::date, '2016-01-31'::date, '1 day'::interval) AS day
),
daily_prices AS (
    -- Select and group by date, origin and destination ports
    SELECT ds1.day, p1.orig_code, p1.dest_code, AVG(p1.price) AS avg_price, COUNT(*) AS price_count
    FROM date_series ds1
    LEFT JOIN prices p1 ON ds1.day = p1.day AND p1.orig_code = ANY('NOOSL') AND p1.dest_code = ANY('EETLL')
    GROUP BY ds1.day, p1.orig_code, p1.dest_code
)
-- Filter to only include dates with 3 or more records
SELECT
    day,
    CASE WHEN price_count >= 3 THEN avg_price ELSE NULL END AS avg_price
FROM daily_prices
ORDER BY day;