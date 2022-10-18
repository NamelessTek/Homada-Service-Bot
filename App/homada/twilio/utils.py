from queue import Empty
from typing import List
from homada.models import Ubicacion, Client
from homada.ubicacion.utils import get_ubicacion
from twilio.twiml.messaging_response import MessagingResponse
from homada import client as twilio_client
from homada.config import Config
from flask import Flask, request
import phonenumbers


def send_location_message(phone_number: str, message: str, ubicacion: int = Ubicacion.id) -> dict:
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
            message = twilio_client.messages.create(
                to=phone_number,
                from_=Config.TWILIO_PHONE_NUMBER,
                body=message,
            )
        except Exception:
            return {'sucess': False, 'message': 'Message could not be sent', 'status_code': 400, 'error': True, 'code': '4'}

    else:
        pass


def validate_phone_number(phone_number: str) -> bool:
    '''
    Validate phone number
    '''
    try:
        phone = phonenumbers.parse(phone_number.strip(), None)
        client = Client.query.filter_by(phone=phone_number).first()
        return phonenumbers.is_valid_number(phone) and client is not None
    except Exception:
        return False


def conversations(phone_number: str, incoming_message: str) -> list:
    '''
    Conversations with the user
    '''
    messages = list()
    client = Client.query.filter_by(phone=phone_number).first()

    if incoming_message:
        match incoming_message:
            case 'hola':
                messages = [
                    f'¡Hola {client.name}! Gracias por hacer tu reservación con nosotros 😃', 'cómo podemos ayudarte?']

            case 'adios':
                messages.append(
                    f'¡Adios {client.name}! Esperamos verte pronto 😃')
            case 'menu':
                messages.append(
                    f'¡Hola {client.name}! Estos son los servicios que ofrecemos: \n 1. Ubicacion \n 2. Reservacion \n 3. Cancelar reservacion \n 4. Salir')
            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.')

        # return the list of messages in different messages

        return messages

    else:
        pass


def incoming_message() -> str:
    '''
    Receive incoming messages
    '''
    # Get the message the user sent our Twilio number
    incoming_message = request.values.get('Body', '').lower()
    # Get the phone number of the person sending the text message
    phone_number = request.values.get('From', None).replace('whatsapp:', '')
    if validate_phone_number(phone_number):

        # Get the message the user sent our Twilio number
        resp = MessagingResponse()
        # Determine the right reply for this message
        # msg = resp.message()
        # Query the database for the phone number
        if incoming_message:
            # deconcatenate the list of messages and send them as different messages
            for message in conversations(phone_number, incoming_message):
                msg = resp.message(message)

        else:
            pass
    else:
        msg.body("Lo sentimos, no se encuentra registrado en nuestro sistema. Por favor comuniquese con nosotros para poder ayudarlo.")

    return str(resp)
