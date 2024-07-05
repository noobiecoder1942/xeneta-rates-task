from typing import List
from flask import current_app
from db.queries import get_ports_from_region_query, get_average_rates_query
from db.database import get_rows

def isRegion(slug):
    return not (len(slug) == 5 and slug.isupper())

def get_all_ports_in_region(region_slug: str) -> List[str]:
    ports = []
    if isRegion(region_slug):
        params = {'region_slug': region_slug}
        db_rows = get_rows(get_ports_from_region_query, params)
        for row in db_rows:
            ports.append(row['port_code'])
    else:
        ports = [region_slug]
    return ports

def get_average_rates(date_from, date_to, origin, destination):
    origin_ports = get_all_ports_in_region(origin)
    destination_ports = get_all_ports_in_region(destination)
    params = (date_from, date_to, origin_ports, destination_ports)
    db_rows = get_rows(get_average_rates_query, params)
    average_rates = []
    for row in db_rows:
        average_rates.append(convert_row_to_dict(row))
    return average_rates

def convert_row_to_dict(row):
    date_format = current_app.config['DATE_FORMAT']
    result = {
        "day": row["day"].strftime(date_format),
        "average_price": round(row["avg_price"]) if row["avg_price"] is not None else None,
    }
    return result

