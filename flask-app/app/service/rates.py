from typing import Dict, List
from flask import current_app
from app.db.queries import get_ports_from_region_query, get_average_rates_query
from app.db.database import get_rows

def is_region(slug: str) -> bool:
    """
    Determine if the given slug represents a region.

    Parameters:
    ----------
    slug : str
        The slug to check.

    Returns:
    -------
    bool
        True if the slug represents a region, False if it represents a port.
    """
    return not (len(slug) == 5 and slug.isupper())

def get_all_ports_in_region(region_slug: str) -> List[str]:
    """
    Retrieve all port codes within a specified region.

    Parameters:
    ----------
    region_slug : str
        The slug representing the region or port code.

    Returns:
    -------
    List[str]
        A list of port codes within the specified region or a list containing
        the port code if the slug represents a port.
    """
    ports = []
    if is_region(region_slug):
        params = {'region_slug': region_slug}
        db_rows = get_rows(get_ports_from_region_query, params)
        for row in db_rows:
            ports.append(row['port_code'])
    else:
        ports = [region_slug]
    return ports

def get_average_rates(date_from: str, date_to: str, origin: str, destination: str) -> List:
    """
    Calculate the average rates between ports or regions over a specified date range.

    Parameters:
    ----------
    date_from : str
        The start date for the rate query in YYYY-MM-DD format.
    date_to : str
        The end date for the rate query in YYYY-MM-DD format.
    origin : str
        The origin port code or region slug.
    destination : str
        The destination port code or region slug.

    Returns:
    -------
    List[dict]
        A list of dictionaries, each containing the day and the average rate for
        that day.
    """
    origin_ports = get_all_ports_in_region(origin)
    destination_ports = get_all_ports_in_region(destination)
    params = (date_from, date_to, origin_ports, destination_ports)
    db_rows = get_rows(get_average_rates_query, params)
    average_rates = []
    for row in db_rows:
        average_rates.append(convert_row_to_dict(row))
    return average_rates

def convert_row_to_dict(row: Dict) -> Dict:
    """
    Convert a database row to a dictionary with formatted date and average price.

    Parameters:
    ----------
    row : dict
        The database row to convert.

    Returns:
    -------
    dict
        A dictionary with the formatted day and average price.
    """
    date_format = current_app.config['DATE_FORMAT']
    result = {
        "day": row["day"].strftime(date_format),
        "average_price": round(row["avg_price"]) if row["avg_price"] is not None else None,
    }
    return result
