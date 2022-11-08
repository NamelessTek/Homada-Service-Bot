from homada.models import *
from homada.ubicacion.utils import get_ubicacion
from homada.admin.utils import get_admin
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


def goodby_message() -> str:
    '''
    Goodbye message
    '''
    resp = MessagingResponse()
    resp.message('Adios 😃')
    return str(resp)


def conversations_client(phone_number: str, incoming_message: str) -> list:
    '''
    Conversations with the user
    '''
    response = MessagingResponse()
    messages = []
    client = Client.query.filter_by(phone=phone_number).first()
    booking = get_booking(
        Booking.query.filter_by(cliente_id=client.id).first())
    ubicacion = get_ubicacion(
        Ubicacion.query.filter_by(id=booking['Ubicacion_id']).first())

    if incoming_message:
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
            # case 'menu':
            #     messages.append(
            #         f'¡Hola {client.name}! Estos son los servicios que ofrecemos: \n 1. Ubicacion \n 2. Reservacion \n 3. Cancelar reservacion \n 4. Salir')
            case 'crear usuario':
                if 'question_id' in session:
                    pass
                    # Sent to conversation to get answer
                    # response.redirect(
                    #

            case _:
                messages.append(
                    f'No pude entender tu respuesta 😟 Inténtalo nuevamente 👇🏼 o escribe menu para desplegar las opciones con las que podemos apoyarte.')

    else:
        pass

    return messages


def conversations_homada(incoming_message: str) -> list:
    '''
    Conversations with the homada user
    '''
    response = MessagingResponse()
    messages = []

    if incoming_message:
        if 'question_id' in session:
            # Guardar respuesta en db

            next_id_question = int(session['question_id'])+1
            print("Siguiente pregunta", flush=True)
            next_question = Questions.query.filter_by(
                id=next_id_question).first()
            print("Pregunta siguiente " + next_question.question, flush=True)
            if next_question:
                session['question_id'] = next_question.id
                messages.append(next_question.question)
            else:
                messages.append(goodbye_twiml())
        else:
            print("Primera pregunta", flush=True)
            pregunta = redirect_to_first_question()
            print("Pregunta " + pregunta, flush=True)
            messages.append(pregunta)
            messages.append("primera preguntas")
    else:
        pass

    return messages


def redirect_to_first_question():
    first_question = Questions.query.order_by(Questions.id).first()
    session['question_id'] = first_question.id
    return first_question.question


def welcome_user(send_function):
    welcome_text = """Para la creación de una reservación es necesario crear el cliente con los siguientes datos:
                    - Nombre
                    - teléfono
                    - Email
                    - número de reservación
                    - día de llegada
                    - hora de llegada
                    - día de partida
                    - hora de partida
                    - ubicación
                    """
    # send_function(welcome_text)
    return welcome_text


def goodbye_twiml():
    response = MessagingResponse()
    response.message("Thank you for answering our survey. Good bye!")
    if 'question_id' in session:
        del session['question_id']
    return str(response)


def sms_twiml(question):
    response = MessagingResponse()
    response.message(question.content)
    return str(response)


def incoming_message() -> str:
    '''
    Receive incoming messages
    '''
    # Get the message the user sent our Twilio number
    incoming_message = request.values.get('Body', '').lower()
    # Get the phone number of the person sending the text message
    phone_number = request.values.get('From', None).replace('whatsapp:', '')
    resp = MessagingResponse()
    print(get_admin())
    # if the phone number is valid
    if phone_number != get_admin():
        # Client conversation
        if validate_phone_number(phone_number) and incoming_message:
            for message in conversations_client(phone_number, incoming_message):
                resp.message(message)
        else:
            resp.message(
                'Lo sentimos, no pudimos validar tu numero de telefono 😟')
    else:
        if 'question_id' not in session:
            resp.message("""Hola, bienvenido a Homada
            Para la creación de una reservación es necesario crear el cliente con los siguientes datos:
            - Nombre
            - teléfono
            - Email
            - número de reservación
            - día de llegada
            - hora de llegada
            - día de partida
            - hora de partida
            - ubicación
            """)
        for message in conversations_homada(incoming_message):
            resp.message(message)

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


def send_question(phone_number: str, question_id: int) -> list:
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
