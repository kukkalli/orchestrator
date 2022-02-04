from flask import Flask, request, abort, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({'name': 'Hanif Kukkalli', 'dob': "1984-11-01"})


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
    app.run(host='127.0.0.1', port=8080, debug=True)
