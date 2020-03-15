from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin

from service import statistic, score
from util import log

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

app = Flask(__name__, static_url_path='', static_folder='static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
log.init()


@app.route('/')
@cross_origin()
def home():
    return app.send_static_file('index.html')


@app.route('/statistic', methods=['GET'])
@cross_origin()
def get_statistics():
    result = statistic.find_last()
    if result is None:
        abort(503)
    return jsonify(result)


@app.route('/score', methods=['POST'])
@cross_origin()
def get_score():
    if request.json is None or 'sentence' not in request.json:
        abort(400)
    else:
        if not score.is_ready():
            abort(503)
        return jsonify(score.get_score(request.json)), 200


if __name__ == '__main__':
    app.run(host='localhost', port=3030, debug=True)
