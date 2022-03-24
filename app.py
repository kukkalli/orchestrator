import logging
import sys
import time

from flask import Flask, request, abort, jsonify

from service_chain import ServiceChain
from templates.input_request import InputRequest
from templates.serviceprofiles import ServiceProfiles

app = Flask(__name__)
app.debug = True
app.secret_key = '598-626-262'
logging.basicConfig(filename='orchestrator.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger(__name__)


@app.route("/hello", methods=['GET'])
def hello():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} (default)".format(version)
    return message


@app.route('/getSquare', methods=['POST'])
def get_square():
    if not request.json or 'number' not in request.json:
        abort(400)
    num = request.json['number']

    return jsonify({'answer': num ** 2})


@app.route('/create-service-chain', methods=['POST'])
def create_service_chain():
    log.info(f"Create Service Chain Input Time: {time.time()}")
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
    # service_chain = ServiceChain(input_request)
    # service_chain.create_service_chain()
    return jsonify({"service-creation": "success"})
    # service_chain.create_service_chain())


@app.route('/', methods=['GET'])
def main():
    log.info("Main Method")
    return jsonify({'name': 'Hanif Kukkalli', 'dob': "1984-11-01"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
