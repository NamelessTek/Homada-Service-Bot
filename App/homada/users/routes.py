from flask import Blueprint, request, jsonify, render_template

user = Blueprint('user', __name__)


@user.route('/', methods=['GET', 'POST'])
def status():
    # get status of the app
    message = {
        'status': 'ok',
        'message': 'App is running',
        'port': 5555,
        'app': 'homada'
    }
    return jsonify(message), 200
