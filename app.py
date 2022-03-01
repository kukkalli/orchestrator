import sys

from flask import Flask, request, abort, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({'name': 'Hanif Kukkalli', 'dob': "1984-11-01"})


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


@app.route('/create-vm', methods=['POST'])
def create_vm():
    if not request.json:
        abort(400)
    if 'request_id' not in request.json:
        abort(400)

    return jsonify({'vm-creation': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
