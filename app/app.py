from flask import Flask, request, jsonify
import logging
from service.rates import get_average_rates
from utils.data_validation import validate_request
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

logging.basicConfig(level = int(config['DEFAULT']['LOG_LEVEL']))
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = bool(config['DEFAULT']['PRETTY_PRINT'])
app.config['DATE_FORMAT'] = config['DEFAULT']['DATE_FORMAT']
app.config['DB_USER'] = config['DATABASE']['USER']
app.config['DB_PASSWORD'] = config['DATABASE']['PASSWORD']
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

    logger.info(f"Request params:\ndate_from: {date_from}\ndate_to: {date_to}\norigin: {origin}\ndestination: {destination}")
    
    validate_request(date_from, date_to, origin, destination)

    average_rates = get_average_rates(date_from, date_to, origin, destination)
    logger.info(f"Response: {average_rates}")
    return jsonify(average_rates)


if __name__ == "__main__":
    app.run()