from datetime import datetime
from werkzeug.exceptions import BadRequest
from flask import current_app

def is_date_valid(date_str: str) -> bool:
    """
    Check if the provided date string is valid according to the application's date format.

    Parameters:
    ----------
    date_str : str
        The date string to validate.

    Returns:
    -------
    bool
        True if the date string is valid according to the application's date format,
        False otherwise.
    """
    try:
        flag = datetime.strptime(date_str, current_app.config['DATE_FORMAT'])
    except ValueError:
        flag = False
    return flag

def validate_request(date_from: str, date_to: str, origin: str, destination: str):
    """
    Validate the request parameters for querying average rates.

    Parameters:
    ----------
    date_from : str
        The start date for the rate query.
    date_to : str
        The end date for the rate query.
    origin : str
        The origin port code or region slug.
    destination : str
        The destination port code or region slug.

    Raises:
    ------
    BadRequest
        If any of the request parameters are invalid.
    """
    if not date_from or not is_date_valid(date_from):
        raise BadRequest("Invalid date_from argument")
    if not date_to or not is_date_valid(date_to):
        raise BadRequest("Invalid date_to argument")
    if not origin:
        raise BadRequest("Invalid origin argument")
    if not destination:
        raise BadRequest("Invalid destination argument")
