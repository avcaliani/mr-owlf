from _pickle import load
from os import environ as env

from flask import Blueprint, jsonify

CLF_FILE = env.get('APP_CLF_FILE', '../.dev/classifier.pkl')
VECTORIZER_FILE = env.get('APP_VECTORIZER_FILE', '../.dev/vectorizer.pkl')
controller = Blueprint('Controller', __name__, template_folder='templates')


@controller.route('/find', methods=['GET'])
def get_tasks():
    file = open(CLF_FILE, 'rb')
    data = load(file)
    file.close()
    return jsonify(list(data))
