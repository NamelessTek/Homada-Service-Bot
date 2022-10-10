import json
from homada.models import Ubicacion, Option
from flask import Blueprint, request, jsonify
from homada.ubicacion.utils import *

location = Blueprint('location', __name__)


@location.route('/get_ubicacion', methods=['GET', 'POST'])
def get_ubicacion_data() -> dict:
    '''
    Get ubicacion data from database and return it as a dictionary
    '''
    json_data = request.get_json()
    data = []
    message = {}
    error = ''

    if json_data:
        if 'id' in json_data.keys():
            data.append(get_ubicacion(
                Ubicacion.query.filter_by(id=json_data['id']).first()))
        elif 'filter_by' in json_data.keys():
            if json_data['filter_by'] == 'all':
                data = [get_ubicacion(
                    ubicacion) for ubicacion in Ubicacion.query.all() if ubicacion.status == 1]
            else:
                error = 'Invalid filter_by value'
        else:
            error = 'Invalid request'
    else:
        error = 'No data received'

    try:
        message.update({'sucess': True, 'ubicacion': data, 'message': 'Ubicacion data retrieved ', 'status_code': 200, 'error': None, } if data else {
            'sucess': False,  'message': 'Ubicacion data could not be retrieved', 'status_code': 400, 'error': f'{error}', })
    except Exception:
        raise Exception('Error retrieving ubicacion data')

    return jsonify(message), message['status_code']
