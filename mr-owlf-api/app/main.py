from flask import Flask, jsonify

from service import statistic

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


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
