import logging
from configparser import ConfigParser
from flask import Flask, request, jsonify
from app.service.rates import get_average_rates
from app.utils.data_validation import validate_request

config = ConfigParser()
config.read('config.ini')

logging.basicConfig(level = int(config['DEFAULT']['LOG_LEVEL']))
logger = logging.getLogger(__name__)

def create_app():
    """
    Creates and configures the Flask application.

    Routes:
    - `/`: A simple route that returns a welcome message.
    - `/healthcheck`: A route to check the health status of the service.
    - `/rates`: A route to get average rates between given dates for specified origin 
      and destination ports/regions. Accepts `GET` requests with the following query parameters:
        - `date_from`: The start date for the rate query.
        - `date_to`: The end date for the rate query.
        - `origin`: The origin port code or region slug.
        - `destination`: The destination port code or region slug.

    Returns:
    -------
    app : Flask
        The configured Flask application.
    """
    app = Flask(__name__)
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = bool(config['DEFAULT']['PRETTY_PRINT'])
    app.config['DATE_FORMAT'] = config['DEFAULT']['DATE_FORMAT']
    app.config['DB_USER'] = config['DATABASE']['USER']
    app.config['DB_PASSWORD'] = config['DATABASE']['PASSWORD']
    app.config['DB_HOST'] = config['DATABASE']['HOST']
    app.config['DB_PORT'] = config['DATABASE']['PORT']
    app.config['DB_NAME'] = config['DATABASE']['NAME']

    @app.route('/')
    def index():
        return "Hello!"

    @app.route('/healthcheck')
    def healthcheck():
        return "Service is up and running!"

    @app.route('/rates', methods=["GET"])
    def get_rates():
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        origin = request.args.get('origin')
        destination = request.args.get("destination")

        logger.info(
            f"Request params:\ndate_from: {date_from}\n"
            f"date_to: {date_to}\n"
            f"origin: {origin}\n"
            f"destination: {destination}"
        )
        validate_request(date_from, date_to, origin, destination)

        average_rates = get_average_rates(date_from, date_to, origin, destination)
        logger.info(f"Response: {average_rates}")
        return jsonify(average_rates)
    return app
