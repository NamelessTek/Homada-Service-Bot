from homada.models import Ubicacion
from homada.ubicacion.utils import get_ubicacion
from twilio.twiml.messaging_response import MessagingResponse
from homada import client
from homada.config import Config
from flask import request


def send_message(phone_number: str, message: str, ubicacion: int = Ubicacion.id) -> dict:
    '''
    Send message to a phone
    '''
    ubicacion_data = get_ubicacion(
        Ubicacion.query.filter_by(id=ubicacion).first())
    if phone_number and message:
        match message:
            case 1:
                message = f'La ubicacion se encuentra en {ubicacion_data["Ubicacion"]}'
            case _:
                message = f'Oops! Algo salio mal, por favor intente mas tarde'
        try:
            message = client.messages.create(
                to=phone_number,
                from_=Config.TWILIO_PHONE_NUMBER,
                body=message,
            )
        except Exception:
            return {'sucess': False, 'message': 'Message could not be sent', 'status_code': 400, 'error': True, 'code': '4'}

    else:
        pass


def incoming_message() -> dict:
    '''
    Receive incoming messages
    '''

    resp = MessagingResponse()

    # Add a text message
    msg = resp.message("Me debes un helado")

    # Add a picture message
    msg.media(
        "https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg"
    )

    return str(resp)
