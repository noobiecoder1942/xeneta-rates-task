from datetime import datetime
from werkzeug.exceptions import BadRequest
from flask import current_app

def is_date_valid(date_str: str) -> bool:
    try:
        flag = datetime.strptime(date_str, current_app.config['DATE_FORMAT'])
    except ValueError:
        flag = False
    return flag

def validate_request(date_from, date_to, origin, destination):
    if not date_from or not is_date_valid(date_from):
        raise(BadRequest("Invalid date_from argument"))
    if not date_to or not is_date_valid(date_to):
        raise(BadRequest("Invalid date_to argument"))
    if not origin:
        raise(BadRequest("Invalid origin argument"))
    if not destination:
        raise(BadRequest("Invalid destination argument"))