import json
from flask import Blueprint, request, jsonify
from homada.ubicacion.utils import *
from homada.twilio.utils import *
from homada.ubicacion.utils import *

twilio = Blueprint('twilio', __name__)


@twilio.route('/send_message', methods=['GET', 'POST'])
def send_message_data() -> dict:
    '''
    send a message with twilio to a given phone number
    '''

    json_data = request.get_json()
    data = []
    response = {}
    error, message, code = False, '', ''
    if json_data and all(json_data.values()):
        if 'phone_number' in json_data.keys() and isinstance(json_data['phone_number'], str):
            if 'send_message' in json_data.keys():
                # get ubicacion data
                ubicacion = get_ubicacion(Ubicacion.query.filter_by(
                    id=json_data['send_message']).first())
                mensaje = f'Su próxima reserva es en {ubicacion["Ubicacion"]}, {ubicacion["Direccion"]}. En esta ubicación el modem es {ubicacion["Modem"]}, la clave es {ubicacion["SSID"]} y esta es la ubicación en el mapa {ubicacion["URL"]} .'
                data.append(send_message(
                    json_data['phone_number'], mensaje))
            message, code = f'Message sent to {json_data["phone_number"]}', 2
        else:
            error, code = 'Invalid request', 4
    else:
        error, code = 'No data received', 5

    response.update({'sucess': True, 'message': data, 'message': f'{message}', 'status_code': 200, 'error': None, 'code': f'{code}'} if data and data != [{}]else {
        'sucess': False,  'message': 'Message could not be sent', 'status_code': 400, 'error': f'{error}', 'code': f'{code}'})

    return jsonify(response), response['status_code']

    '''
    Send message to a phone 
    '''


@twilio.route('/incoming_message', methods=['GET', 'POST'])
def incoming_message_data() -> dict:
    '''
    Receive incoming messages
    '''
    return incoming_message()
