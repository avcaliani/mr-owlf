from os import environ as env
from _pickle import load
from flask import Blueprint, jsonify, make_response

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

CLF_FILE = env.get('MR_OWLF_CLF_FILE', '../.shared/clf.pkl')
Controller = Blueprint('Controller', __name__, template_folder='templates')


@Controller.route('/find', methods=['GET'])
def get_tasks():
    file = open(CLF_FILE, 'rb')
    data = load(file)
    file.close()
    return jsonify(list(data))
