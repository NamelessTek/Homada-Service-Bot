from asyncio import wait_for
from multiprocessing.connection import wait
from urllib import response
from homada.models import Ubicacion, Client
from homada.ubicacion.utils import get_ubicacion
from homada.clientes.utils import get_client_reservation
from twilio.twiml.messaging_response import MessagingResponse
from homada import client as twilio_client
from homada.config import Config
from flask import Flask, request
import phonenumbers
import asyncio
import time


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
    messages = []
    client = Client.query.filter_by(phone=phone_number).first()
    reservation = get_client_reservation(client)

    # response = request.values.get('Body', '').lower()

    if incoming_message:
        match incoming_message:

            case 'hola':
                messages.append(
                    f'¡Hola {client.name}! Gracias por hacer tu reservación con nosotros 😃')
                if len(reservation) > 1:
                    messages = [f'{client.name} tienes {len(reservation)} reservaciones',
                                f'¿De qué ubicación quieres saber la informacion?']
                    messages.extend(
                        f'{index + 1}. {ubicacion["Ubicacion"]}' for index, ubicacion in enumerate(reservation))
                    time.sleep(1)
                elif len(reservation) == 1:
                    messages.append(
                        f'{client.name}, tu proxima reservacion es en {reservation[0]["Ubicacion"]}')
                else:
                    messages.append(
                        f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
            case 'adios':
                messages.append(
                    f'¡Adios {client.name}! Esperamos verte pronto 😃')
            case 'menu':
                messages.append(
                    f'¡Hola {client.name}! Estos son los servicios que ofrecemos: \n 1. Ubicacion \n 2. Reservacion \n 3. Cancelar reservacion \n 4. Salir')
                response = request.values.get('Body', '').lower()
            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.')
        if response:
            match response:
                case '1':
                    messages.clear()
                    messages.append(Menu(phone_number, 1))
                case _:
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.'
        else:
            pass
    else:
        pass
        # only send the message if the user typed menu

    return messages


def incoming_message() -> str:
    '''
    Receive incoming messages
    '''
    # Get the message the user sent our Twilio number
    incoming_message = request.values.get('Body', '').lower()
    # Get the phone number of the person sending the text message
    phone_number = request.values.get('From', None).replace('whatsapp:', '')
    resp = MessagingResponse()
    # if the phone number is valid
    if validate_phone_number(phone_number) and incoming_message:
        for message in conversations(phone_number, incoming_message):
            resp.message(message)

    else:
        resp.message(
            'Lo sentimos, no pudimos validar tu numero de telefono 😟')

    return str(resp)


def Menu(phone_number: str, option: int) -> str:
    '''
    Conversation response
    '''
    client = Client.query.filter_by(phone=phone_number).first()

    if option:
        match option:
            case 1:
                menu = f'¿De qué ubicación quieres saber la informacion?'
            case _:
                menu = f'Oops! Algo salio mal, por favor intente mas tarde'

    return menu


def send_location_data(option: int) -> str:
    '''
    Send location data
    '''
    option = int(request.values.get('Body', '').lower())
    if option:
        # get the location data
        location_data = get_ubicacion(
            Ubicacion.query.filter_by(id=option).first())
    else:
        pass

    return location_data["Ubicacion"]


def wait_for_user_response() -> int:
    '''
    Wait for user response
    '''
    # Wait for the user to select an option
    selected_option = request.values.get('Body', '').lower()

    return selected_option
