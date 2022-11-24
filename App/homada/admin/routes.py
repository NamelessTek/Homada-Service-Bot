from flask import Blueprint, request, jsonify, render_template
from homada.models import *

admin_homada = Blueprint('admin_homada', __name__)


@admin_homada.route('/', methods=['GET', 'POST'])
def status():
    # get status of the app
    message = {
        'status': 'ok',
        'message': 'App is running',
        'port': 5555,
        'app': 'homada',
    }
    return jsonify(message), 200
