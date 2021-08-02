
from flask import Flask, jsonify, request
from scrp.tripadvisor import Tripadvisor
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"Message": "අපි තමයි හොදටම කරේ"})


@app.route('/init', methods=['GET'])
def init():
    uuid = request.args.get('uuid')
    query = request.args.get('query')
    tr = Tripadvisor(uuid, query)
    tr.get_search_list()
    return jsonify({"uuid": uuid, "query": query, "status": "started"})


@app.route('/get_data', methods=['GET'])
def get_data():
    uuid = request.args.get('uuid')
    try:
        with open('data/' + str(uuid) + '.json', encoding="utf8") as f:
            data = json.load(f)
        return jsonify({"status": "completed", "result": data})
    except Exception as e:
        print(uuid, e)
        return jsonify({"status": "in progress", "result": []})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
