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
    response = {}
    error, message, code = False, '', ''
    if json_data and all(json_data.values()):

        if 'id' in json_data.keys() and isinstance(json_data['id'], int):
            data.append(get_ubicacion(
                Ubicacion.query.filter_by(id=json_data['id']).first()))
            message, code = f'Ubicacion {json_data["id"]} found', 2

        elif 'ubicacion' in json_data.keys() and isinstance(json_data['ubicacion'], str):
            data.append(get_ubicacion(Ubicacion.query.filter_by(
                ubicacion=json_data['ubicacion']).first()))
            message, code = f'Ubicacion {json_data["ubicacion"]} found', 6

        elif 'filter_by' in json_data.keys():
            if json_data['filter_by'] == 'all':
                data = [get_ubicacion(
                    ubicacion) for ubicacion in Ubicacion.query.all()]
                message, code = f'{len(data)} ubicaciones found in database', 1
            else:
                error, code = 'Invalid filter_by value', 3
        else:
            error, code = 'Invalid request', 4

    else:
        error, code = 'No data received', 5

    response.update({'sucess': True, 'ubicacion': data, 'message': f'{message}', 'status_code': 200, 'error': None, 'code': f'{code}'} if data and data != [{}]else {
        'sucess': False,  'message': 'Ubicacion data could not be retrieved', 'status_code': 400, 'error': f'{error}', 'code': f'{code}'})

    return jsonify(response), response['status_code']
