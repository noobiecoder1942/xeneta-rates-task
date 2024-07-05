get_ports_from_region_query = """
    WITH RECURSIVE sub_region AS (
        -- anchor member
        SELECT r1.slug, r1.parent_slug as parent_slug 
        FROM regions r1 
        WHERE r1.slug = %(region_slug)s

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
"""

get_average_rates_query = """
    WITH day_series AS (
        SELECT day::date FROM generate_series(%s, %s, '1 day'::interval) AS day
    ),
    price_series AS (
        SELECT p1.price, p1.day
        FROM prices p1
        WHERE p1.orig_code = ANY(%s) AND p1.dest_code = ANY(%s)
    )
    SELECT ds1.day, 
    CASE WHEN COUNT(ps1.price) >= 3 THEN AVG(ps1.price) ELSE NULL END AS avg_price,
    COUNT(ps1.price) AS cnt
    FROM day_series ds1
    LEFT JOIN price_series ps1
    ON ds1.day = ps1.day
    GROUP BY ds1.day
"""