import logging
import sys
import time
from logging.handlers import RotatingFileHandler

from flask import Flask, request, abort, jsonify

from service_chain import ServiceChain
from templates.input_request import InputRequest
from templates.serviceprofiles import ServiceProfiles

app = Flask(__name__)
app.debug = True
LOG_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - (%(lineno)d) - %(message)s')
LOG_FILE = "./logs/orchestrator.log"
LOG_HANDLER = RotatingFileHandler(LOG_FILE, mode='a', maxBytes=1024*1024,
                                  backupCount=9, encoding=None, delay=False)
LOG_HANDLER.setFormatter(LOG_FORMATTER)
LOG_HANDLER.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - (%(lineno)d) - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[
        LOG_HANDLER
    ]
)

LOG = logging.getLogger(__name__)


@app.route("/hello", methods=['GET'])
def hello():
    LOG.info(f"Calling Hello at Time: {time.time()}")
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} (default)".format(version)
    LOG.info(f"Returning Message: '{message}' at Time: {time.time()}")
    return message


@app.route('/getSquare', methods=['POST'])
def get_square():
    if not request.json or 'number' not in request.json:
        abort(400)
    num = request.json['number']

    return jsonify({'answer': num ** 2})


@app.route('/create-service-chain', methods=['POST'])
def create_service_chain():
    LOG.info(f"Create Service Chain Input Time: {time.time()}")
    params = request.json
    app.logger.debug(f"Create Service Chain {params}")
    bandwidth = 100
    max_link_delay = 100
    domain_name = "tu-chemnitz.de"
    if not params:
        abort(400)
    if 'name' not in params:
        abort(400)
    if 'service_profile' not in params:
        abort(400)
    if ServiceProfiles("FOUR_G_LTE_CORE") not in ServiceProfiles:
        abort(422)
    if 'domain_name' in params:
        domain_name = params["domain_name"]
    if 'bandwidth' in params:
        bandwidth = params["bandwidth"]
    if 'max_link_delay' in params:
        max_link_delay = params["max_link_delay"]

    input_request = InputRequest(params["name"], params["service_profile"], domain_name, bandwidth, max_link_delay)
    service_chain = ServiceChain(input_request)
    # service_chain.create_service_chain()
    return jsonify({"service-creation": "success"})


@app.route('/', methods=['GET'])
def main():
    LOG.info("Main Method")
    return jsonify({'name': 'Hanif Kukkalli', 'dob': "1984-11-01"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
