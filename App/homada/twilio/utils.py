from homada.models import Ubicacion, Client, Booking, Questions
from homada.ubicacion.utils import get_ubicacion
from homada.reservaciones.utils import get_booking
from twilio.twiml.messaging_response import MessagingResponse
from homada import client as twilio_client
from flask import Flask, request, url_for, session, redirect
import phonenumbers


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


def redirect_twiml(question: int) -> str:
    '''
    Answer the question
    '''
    resp = MessagingResponse()
    resp.redirect(url_for('twilio_conversations', question=question))
    return str(resp)


def goodby_message() -> str:
    '''
    Goodbye message
    '''
    resp = MessagingResponse()
    resp.message('Adios 😃')
    return str(resp)


def conversations(phone_number: str, incoming_message: str) -> list:
    '''
    Conversations with the user
    '''
    messages = []
    client = Client.query.filter_by(phone=phone_number).first()
    booking = get_booking(
        Booking.query.filter_by(cliente_id=client.id).first())
    ubicacion = get_ubicacion(
        Ubicacion.query.filter_by(id=booking['Ubicacion_id']).first())

    if incoming_message:
        response = request.values.get('Body', '').lower()
        match incoming_message:
            case 'hola':
                messages = [
                    f'¡Hola {client.name}! Hola bienvenido a Homada, muchas gracias por tu preferencia']
                # if len(booking) > 1:
                #     messages = [f'{client.name} tienes {len(booking)} reservaciones',
                #                 f'¿De qué ubicación quieres saber la informacion?']
                # messages.extend(
                #     f'{index + 1}. {ubicacion["Ubicacion"]}' for index, ubicacion in enumerate(booking))
                if booking:
                    messages.extend(
                        [f'{client.name}, para tu entradad el día {booking["Arrival"].strftime("%d/%m/%Y")}, queremos compartirte algunos datos. La hora de entrada es a las {booking["Arrival_time"].strftime("%H:%M")}. Sabemos que puedes necesitar conexión a internet, la red es {ubicacion["SSID"]} y el password es {ubicacion["Clave"]}.',
                         f'Para tu facilidad, el link de navegación es el siguiente: {ubicacion["URL"]}.',
                         'En caso de necesitar apoyo por favor escribe en el chat la palabra "menú"'])
                else:
                    messages.append(
                        f'{client.name}, no tienes reservaciones, por favor haz una reservacion')
            case 'adios':
                messages.append(
                    f'¡Adios {client.name}! Esperamos verte pronto 😃')
            case 'menu':
                messages.append(
                    f'¡Hola {client.name}! Estos son los servicios que ofrecemos: \n 1. Ubicacion \n 2. Reservacion \n 3. Cancelar reservacion \n 4. Salir')
            case 'crear usuario':
                messages = [message for message in create_user(phone_number)]

            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.')
        if response:
            # if the user selected an option from the ubication menu send the location data
            if response.isdigit() and int(response) <= len(booking):
                messages.clear()
                messages.append(
                    f'La ubicacion se encuentra en {booking[int(response) - 1]["Ubicacion"]}, aquí está el link del mapa {booking[int(response) - 1]["URL"]}')
            else:
                pass
        else:
            messages.append(
                f'Oops! Algo salio mal, por favor intente mas tarde')
    else:
        pass

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

        # resp.message(twilio_studio_flow(phone_number))

    else:
        resp.message(
            'Lo sentimos, no pudimos validar tu numero de telefono 😟')

    return str(resp)


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
                from_="whatsapp:+14155238886",
                body=message,
            )
        except Exception:
            return {'sucess': False, 'message': 'Message could not be sent', 'status_code': 400, 'error': True, 'code': '4'}

    else:
        pass


def create_user(phone_number: str, question_id: int) -> list:
    '''
    Send survey message
    '''
    messages = []
    if phone_number:
        question = Questions.query.filter_by(id=question_id).first()
        messages.append(question.question)
    else:
        pass

    return messages
