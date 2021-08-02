from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def welcome():
    uuid = request.args.get('uuid')
    query = request.args.get('query')

    return jsonify({"uuid": uuid, "query": query})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
