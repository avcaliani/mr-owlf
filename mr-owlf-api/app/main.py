from flask import Flask, jsonify, abort, request

from service import statistic, score

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/statistic', methods=['GET'])
def get_tasks():
    return jsonify(statistic.find_last())


@app.route('/score', methods=['POST'])
def create_task():
    if request.json is None or 'sentence' not in request.json:
        abort(400)
    else:
        if not score.is_ready():
            abort(503)
        return jsonify(score.get_score(request.json)), 200


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
