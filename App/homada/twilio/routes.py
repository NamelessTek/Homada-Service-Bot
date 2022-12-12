from flask import Blueprint, request, jsonify, render_template
from homada.ubicacion.utils import *
from homada.twilio.utils import *
from homada.ubicacion.utils import *
# from .models import *

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
        if ('phone_number' in json_data.keys() and isinstance(json_data['phone_number'], str) and json_data['phone_number'].startswith('whatsapp:+')
                and 'message' in json_data.keys() and isinstance(json_data['message'], int)):
            if 'ubicacion' in json_data.keys() and isinstance(json_data['ubicacion'], int):
                data.append(send_location_message(
                    json_data['phone_number'], json_data['message'], json_data['ubicacion']))
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


@ twilio.route('/incoming_message', methods=['GET', 'POST'])
def incoming_message_data() -> str:
    '''This endpoint is used to receive messages from the client and send a response'''
    if request.method == 'POST':
        response = {}
        error, message, code = False, '', ''
        message = incoming_message()
        response.update({'sucess': True, 'message': message, 'message': f'{message}', 'status_code': 200, 'error': None, 'code': f'{code}'} if message and message != [{}]else {
            'sucess': False,  'message': 'Message could not be sent', 'status_code': 400, 'error': f'{error}', 'code': f'{code}'})
        return message
