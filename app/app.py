from flask import Flask, request, jsonify
import logging
from werkzeug.exceptions import BadRequest
from datetime import datetime
from db.database import get_connection
from service.rates import get_average_rates

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

DATE_FORMAT = "%Y-%m-%d"

@app.route('/')
def hello_world():
    return "Hello World"

def is_date_valid(date_str: str) -> bool:
    try:
        flag = datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        flag = False
    return flag

@app.route('/rates', methods=["GET"])
def get_rates():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get("destination")

    app.logger.info(f"Request params:\ndate_from: {date_from}\ndate_to: {date_to}\norigin: {origin}\ndestination: {destination}")


    if not date_from or not is_date_valid(date_from):
        raise(BadRequest("Invalid date_from argument"))
    if not date_to or not is_date_valid(date_to):
        raise(BadRequest("Invalid date_to argument"))
    if not origin:
        raise(BadRequest("Invalid origin argument"))
    if not destination:
        raise(BadRequest("Invalid destination argument"))
    
    average_rates = get_average_rates(date_from, date_to, origin, destination, DATE_FORMAT)
    app.logger.info(average_rates)
    return jsonify(average_rates)


if __name__ == "__main__":
    app.run()