from flask import Flask

from controller.controller import controller

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

app = Flask(__name__, static_url_path='', static_folder='static')
app.register_blueprint(controller)


@app.route('/')
def home():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
