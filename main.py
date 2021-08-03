from flask import Flask, jsonify, request
from scrp.tripadvisor import Tripadvisor
import json
import glob
import multiprocessing

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def init_job(uuid, query):
    tr = Tripadvisor(uuid, query)
    tr.get_search_list()


@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"Message": "අපි තමයි හොදටම කරේ"})


@app.route('/init', methods=['GET'])
def init():
    print("dfd")
    uuid = request.args.get('uuid')
    query = request.args.get('query')
    p = multiprocessing.Process(target=init_job, args=(uuid, query,))
    p.start()
    return jsonify({"uuid": uuid, "query": query, "status": "started"})


@app.route('/get_data', methods=['GET'])
def get_data():
    uuid = request.args.get('uuid')
    file_list = glob.glob("data/" + uuid + '*.json')
    data = []
    for file in file_list:
        try:
            with open(file, encoding="utf8") as f:
                data.append(json.load(f))
        except Exception as e:
            print("exception on loading files", e)
            pass

    if len(data) == 1:
        return jsonify({"status": "completed", "result": data})
    else:
        return jsonify({"status": "in progress", "result": []})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
